from __future__ import annotations

import tempfile
from pathlib import Path
from typing import Any, TYPE_CHECKING

from .storage import atomic_write_text

if TYPE_CHECKING:
    from .exporters import SimpleMesh

DEFAULT_CORE_FORMATS: tuple[str, ...] = ("glb", "obj", "ply", "stl")
DELIVERY_FORMATS: tuple[str, ...] = ("fbx", "usdz")

FBX_GEOMETRY_NOTES = (
    "Static triangle mesh in FBX 7.4 ASCII. Factor colors may be embedded; "
    "separate PBR map files are not packaged in FBX for this adapter."
)
USDZ_GEOMETRY_NOTES = (
    "Geometry-first USDZ for AR Quick Look. Separate PBR texture maps are "
    "not packaged in USDZ when pbr_available is false."
)
USDZ_UNAVAILABLE_NOTES = (
    "USDZ export skipped because usd-core is not installed. "
    "Install the mesh-delivery optional extra to enable USDZ."
)


def usd_core_available() -> bool:
    try:
        from pxr import Usd  # noqa: F401

        return True
    except ImportError:
        return False


def resolve_export_formats(formats: tuple[str, ...] | None) -> tuple[str, ...]:
    if formats is None:
        return DEFAULT_CORE_FORMATS
    normalized = tuple(fmt.strip().lower() for fmt in formats if fmt.strip())
    return normalized or DEFAULT_CORE_FORMATS


def write_fbx(mesh: SimpleMesh, path: Path) -> None:
    """Write a static mesh as FBX 7.4 ASCII (geometry-only delivery tier)."""
    vertex_lines: list[str] = []
    for x, y, z in mesh.vertices:
        vertex_lines.append(f"{x:.6f},{y:.6f},{z:.6f}")

    polygon_indices: list[str] = []
    for face in mesh.faces:
        a, b, c = face
        polygon_indices.append(f"{a},{b},{-c - 1}")

    vertices_blob = ",".join(vertex_lines)
    indices_blob = ",".join(polygon_indices)
    vertex_count = len(mesh.vertices)
    index_count = len(polygon_indices)

    content = f"""; FBX 7.4.0 project file
; Created by ImageEZGen3D delivery export

FBXHeaderExtension:  {{
    FBXHeaderVersion: 1003
    FBXVersion: 7400
    Creator: "ImageEZGen3D"
}}

GlobalSettings:  {{
    Version: 1000
}}

Documents:  {{
    Count: 1
    Document: 0, "", "Scene" {{
        Properties70:  {{
        }}
        RootNode: 0
    }}
}}

Definitions:  {{
    Version: 100
    Count: 2
    ObjectType: "Geometry" {{
        Count: 1
    }}
    ObjectType: "Model" {{
        Count: 1
    }}
}}

Objects:  {{
    Geometry: 1, "Geometry::", "Mesh" {{
        Vertices: *{vertex_count * 3} {{
            a: {vertices_blob}
        }}
        PolygonVertexIndex: *{index_count} {{
            a: {indices_blob}
        }}
        GeometryVersion: 124
    }}
    Model: 2, "Model::Mesh", "Mesh" {{
        Version: 232
        Properties70:  {{
            P: "DefaultAttributeIndex", "int", "Integer", "",0
            P: "Lcl Translation", "Lcl Translation", "", "A",0,0,0
            P: "Lcl Rotation", "Lcl Rotation", "", "A",0,0,0
            P: "Lcl Scaling", "Lcl Scaling", "", "A",1,1,1
        }}
        Shading: Y
        Culling: "CullingOff"
    }}
}}

Connections:  {{
    C: "OO",2,1
}}
"""
    atomic_write_text(path, content)


def write_usdz(mesh: SimpleMesh, path: Path) -> None:
    if not usd_core_available():
        raise RuntimeError(USDZ_UNAVAILABLE_NOTES)

    from pxr import Gf, Usd, UsdGeom, UsdUtils

    points = [Gf.Vec3f(float(x), float(y), float(z)) for x, y, z in mesh.vertices]
    face_vertex_counts = [3] * len(mesh.faces)
    face_vertex_indices = [index for face in mesh.faces for index in face]

    with tempfile.TemporaryDirectory() as directory:
        usda_path = Path(directory) / "mesh.usda"
        stage = Usd.Stage.CreateNew(str(usda_path))
        usd_mesh = UsdGeom.Mesh.Define(stage, "/Mesh")
        usd_mesh.CreatePointsAttr(points)
        usd_mesh.CreateFaceVertexCountsAttr(face_vertex_counts)
        usd_mesh.CreateFaceVertexIndicesAttr(face_vertex_indices)
        stage.GetRootLayer().Save()
        UsdUtils.CreateNewUsdzPackage(str(usda_path), str(path))

    if not path.exists() or path.stat().st_size == 0:
        raise RuntimeError("USDZ export produced an empty artifact.")
    with path.open("rb") as handle:
        if handle.read(2) != b"PK":
            raise RuntimeError("USDZ export did not produce a ZIP-based package.")


def build_delivery_formats_block(
    *,
    adapter: str,
    exported_keys: set[str],
    requested_formats: tuple[str, ...],
) -> dict[str, Any]:
    blocks: dict[str, Any] = {}
    for fmt in DELIVERY_FORMATS:
        if fmt not in requested_formats:
            continue
        if fmt == "usdz" and not usd_core_available():
            blocks[fmt] = {
                "available": False,
                "exported": False,
                "notes": USDZ_UNAVAILABLE_NOTES,
            }
            continue
        exported = fmt in exported_keys
        notes = FBX_GEOMETRY_NOTES if fmt == "fbx" else USDZ_GEOMETRY_NOTES
        blocks[fmt] = {
            "available": True,
            "exported": exported,
            "notes": notes if exported else f"{fmt.upper()} export requested but not written for adapter {adapter!r}.",
        }
    return blocks
