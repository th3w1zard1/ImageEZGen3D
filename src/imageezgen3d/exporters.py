from __future__ import annotations

import json
import math
import struct
from dataclasses import dataclass
from pathlib import Path

from .storage import atomic_write_bytes, atomic_write_text


@dataclass(frozen=True)
class SimpleMesh:
    vertices: tuple[tuple[float, float, float], ...]
    faces: tuple[tuple[int, int, int], ...]
    color: tuple[float, float, float, float]


def make_box_mesh(width: float, depth: float, height: float, color: tuple[float, float, float, float]) -> SimpleMesh:
    w, d, h = width / 2, depth / 2, height / 2
    vertices = (
        (-w, -d, -h), (w, -d, -h), (w, d, -h), (-w, d, -h),
        (-w, -d, h), (w, -d, h), (w, d, h), (-w, d, h),
    )
    faces = (
        (0, 1, 2), (0, 2, 3), (4, 6, 5), (4, 7, 6),
        (0, 4, 5), (0, 5, 1), (1, 5, 6), (1, 6, 2),
        (2, 6, 7), (2, 7, 3), (3, 7, 4), (3, 4, 0),
    )
    return SimpleMesh(vertices=vertices, faces=faces, color=color)


def write_obj(mesh: SimpleMesh, path: Path) -> None:
    lines = ["# ImageEZGen3D CPU demo mesh"]
    lines.extend(f"v {x:.6f} {y:.6f} {z:.6f}" for x, y, z in mesh.vertices)
    lines.extend(f"f {a + 1} {b + 1} {c + 1}" for a, b, c in mesh.faces)
    atomic_write_text(path, "\n".join(lines) + "\n")


def write_ply(mesh: SimpleMesh, path: Path) -> None:
    red, green, blue = [int(max(0, min(1, channel)) * 255) for channel in mesh.color[:3]]
    header = [
        "ply", "format ascii 1.0", f"element vertex {len(mesh.vertices)}",
        "property float x", "property float y", "property float z",
        "property uchar red", "property uchar green", "property uchar blue",
        f"element face {len(mesh.faces)}", "property list uchar int vertex_indices", "end_header",
    ]
    body = [f"{x:.6f} {y:.6f} {z:.6f} {red} {green} {blue}" for x, y, z in mesh.vertices]
    body.extend(f"3 {a} {b} {c}" for a, b, c in mesh.faces)
    atomic_write_text(path, "\n".join(header + body) + "\n")


def _normal(v1: tuple[float, float, float], v2: tuple[float, float, float], v3: tuple[float, float, float]) -> tuple[float, float, float]:
    ax, ay, az = (v2[i] - v1[i] for i in range(3))
    bx, by, bz = (v3[i] - v1[i] for i in range(3))
    nx, ny, nz = ay * bz - az * by, az * bx - ax * bz, ax * by - ay * bx
    length = math.sqrt(nx * nx + ny * ny + nz * nz) or 1.0
    return nx / length, ny / length, nz / length


def write_stl(mesh: SimpleMesh, path: Path) -> None:
    lines = ["solid imageezgen3d"]
    for face in mesh.faces:
        verts = [mesh.vertices[index] for index in face]
        nx, ny, nz = _normal(*verts)
        lines.append(f"  facet normal {nx:.6f} {ny:.6f} {nz:.6f}")
        lines.append("    outer loop")
        lines.extend(f"      vertex {x:.6f} {y:.6f} {z:.6f}" for x, y, z in verts)
        lines.append("    endloop")
        lines.append("  endfacet")
    lines.append("endsolid imageezgen3d")
    atomic_write_text(path, "\n".join(lines) + "\n")


def _pad4(data: bytes, pad_byte: bytes) -> bytes:
    return data + pad_byte * ((4 - (len(data) % 4)) % 4)


def write_glb(mesh: SimpleMesh, path: Path) -> None:
    positions = b"".join(struct.pack("<3f", *vertex) for vertex in mesh.vertices)
    indices = b"".join(struct.pack("<H", index) for face in mesh.faces for index in face)
    positions_padded = _pad4(positions, b"\x00")
    indices_offset = len(positions_padded)
    bin_blob = _pad4(positions_padded + indices, b"\x00")
    mins = [min(vertex[i] for vertex in mesh.vertices) for i in range(3)]
    maxs = [max(vertex[i] for vertex in mesh.vertices) for i in range(3)]
    gltf = {
        "asset": {"version": "2.0", "generator": "ImageEZGen3D CPU demo"},
        "scene": 0,
        "scenes": [{"nodes": [0]}],
        "nodes": [{"mesh": 0, "name": "ImageEZGen3D Draft"}],
        "materials": [{"pbrMetallicRoughness": {"baseColorFactor": list(mesh.color), "metallicFactor": 0.0, "roughnessFactor": 0.72}}],
        "meshes": [{"primitives": [{"attributes": {"POSITION": 0}, "indices": 1, "material": 0}]}],
        "buffers": [{"byteLength": len(bin_blob)}],
        "bufferViews": [
            {"buffer": 0, "byteOffset": 0, "byteLength": len(positions), "target": 34962},
            {"buffer": 0, "byteOffset": indices_offset, "byteLength": len(indices), "target": 34963},
        ],
        "accessors": [
            {"bufferView": 0, "componentType": 5126, "count": len(mesh.vertices), "type": "VEC3", "min": mins, "max": maxs},
            {"bufferView": 1, "componentType": 5123, "count": len(mesh.faces) * 3, "type": "SCALAR"},
        ],
    }
    json_blob = _pad4(json.dumps(gltf, separators=(",", ":")).encode("utf-8"), b" ")
    total_length = 12 + 8 + len(json_blob) + 8 + len(bin_blob)
    header = struct.pack("<4sII", b"glTF", 2, total_length)
    json_header = struct.pack("<I4s", len(json_blob), b"JSON")
    bin_header = struct.pack("<I4s", len(bin_blob), b"BIN\x00")
    atomic_write_bytes(path, header + json_header + json_blob + bin_header + bin_blob)


def export_all(mesh: SimpleMesh, directory: Path, stem: str = "draft_mesh") -> dict[str, Path]:
    directory.mkdir(parents=True, exist_ok=True)
    paths = {
        "glb": directory / f"{stem}.glb",
        "obj": directory / f"{stem}.obj",
        "ply": directory / f"{stem}.ply",
        "stl": directory / f"{stem}.stl",
    }
    write_glb(mesh, paths["glb"])
    write_obj(mesh, paths["obj"])
    write_ply(mesh, paths["ply"])
    write_stl(mesh, paths["stl"])
    return paths
