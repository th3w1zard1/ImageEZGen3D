from __future__ import annotations

from pathlib import Path
from typing import Any

from .exporters import SimpleMesh

_DEFAULT_MESH_COLOR = (0.72, 0.72, 0.72, 1.0)


def simple_mesh_from_trimesh_like(
    mesh: Any,
    *,
    color: tuple[float, float, float, float] = _DEFAULT_MESH_COLOR,
    b64_image: str | None = None,
) -> SimpleMesh:
    """Convert an upstream trimesh object into the export `SimpleMesh` contract."""
    vertices = tuple(
        tuple(float(value) for value in row) for row in mesh.vertices
    )
    faces = tuple(tuple(int(index) for index in face) for face in mesh.faces)
    return SimpleMesh(
        vertices=vertices,
        faces=faces,
        color=color,
        b64_image=b64_image,
    )


def simple_mesh_from_obj(
    path: Path,
    *,
    color: tuple[float, float, float, float] = _DEFAULT_MESH_COLOR,
    b64_image: str | None = None,
) -> SimpleMesh:
    """Load a minimal Wavefront OBJ mesh into `SimpleMesh`."""
    vertices: list[tuple[float, float, float]] = []
    faces: list[tuple[int, int, int]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped.startswith("v "):
            _, xs, ys, zs = stripped.split(maxsplit=3)
            vertices.append((float(xs), float(ys), float(zs)))
        elif stripped.startswith("f "):
            parts = stripped.split()[1:4]
            indices = tuple(int(part.split("/")[0]) - 1 for part in parts)
            faces.append(indices)
    if not vertices or not faces:
        msg = f"OBJ mesh at {path} has no vertices or faces"
        raise ValueError(msg)
    return SimpleMesh(
        vertices=tuple(vertices),
        faces=tuple(faces),
        color=color,
        b64_image=b64_image,
    )
