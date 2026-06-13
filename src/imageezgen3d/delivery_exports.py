from __future__ import annotations

import tempfile
import zipfile
from pathlib import Path
from typing import Any, Mapping, TYPE_CHECKING
from xml.etree.ElementTree import Element, SubElement, tostring

from .storage import atomic_write_text

if TYPE_CHECKING:
    from .exporters import SimpleMesh

DEFAULT_CORE_FORMATS: tuple[str, ...] = ("glb", "obj", "ply", "stl")
DELIVERY_FORMATS: tuple[str, ...] = ("fbx", "usdz", "3mf", "blend")
KNOWN_EXPORT_FORMATS: frozenset[str] = frozenset(
    (*DEFAULT_CORE_FORMATS, *DELIVERY_FORMATS)
)
_THREEMF_NS = "http://schemas.microsoft.com/3dmanufacturing/core/2015/02"
_THREEMF_MATERIAL_NS = "http://schemas.microsoft.com/3dmanufacturing/material/2015/02"
_XML_NS = "http://www.w3.org/XML/1998/namespace"

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
THREEMF_GEOMETRY_NOTES = (
    "Triangle mesh packaged as 3MF for modern slicers. Geometry-first; "
    "separate PBR map files are not embedded when pbr_available is false."
)
BLEND_UNAVAILABLE_NOTES = (
    "BLEND export requires a Blender runtime (bpy). "
    "Not available in this deployment; use GLB or FBX for DCC interchange."
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


def resolve_target_export_formats(
    target_formats: tuple[str, ...] | list[str] | None,
    configured_formats: tuple[str, ...],
) -> tuple[str, ...]:
    """Resolve Meshy-style target_formats against deployment export config."""
    if not target_formats:
        return configured_formats

    normalized: list[str] = []
    seen: set[str] = set()
    for fmt in target_formats:
        token = str(fmt).strip().lower()
        if not token:
            continue
        if token not in KNOWN_EXPORT_FORMATS:
            known = ", ".join(sorted(KNOWN_EXPORT_FORMATS))
            raise ValueError(
                f"Unknown export format {token!r}. Known formats: {known}."
            )
        if token not in seen:
            normalized.append(token)
            seen.add(token)

    if not normalized:
        raise ValueError("target_formats must include at least one format.")

    configured = {fmt.strip().lower() for fmt in configured_formats if fmt.strip()}
    disabled = [fmt for fmt in normalized if fmt not in configured]
    if disabled:
        raise ValueError(
            "target_formats not enabled in this deployment: "
            f"{disabled}. Configured formats: {sorted(configured)}."
        )
    return tuple(normalized)


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


def write_3mf(mesh: SimpleMesh, path: Path) -> None:
    """Write a triangle mesh as a 3MF ZIP package (geometry-first delivery tier)."""
    model = Element(
        f"{{{_THREEMF_NS}}}model",
        attrib={
            "unit": "millimeter",
            f"{{{_XML_NS}}}lang": "en-US",
        },
    )
    resources = SubElement(model, f"{{{_THREEMF_NS}}}resources")
    obj = SubElement(
        resources,
        f"{{{_THREEMF_NS}}}object",
        attrib={"id": "1", "type": "model"},
    )
    mesh_element = SubElement(obj, f"{{{_THREEMF_NS}}}mesh")
    vertices_element = SubElement(mesh_element, f"{{{_THREEMF_NS}}}vertices")
    for x, y, z in mesh.vertices:
        SubElement(
            vertices_element,
            f"{{{_THREEMF_NS}}}vertex",
            attrib={"x": f"{x:.6f}", "y": f"{y:.6f}", "z": f"{z:.6f}"},
        )
    triangles_element = SubElement(mesh_element, f"{{{_THREEMF_NS}}}triangles")
    for a, b, c in mesh.faces:
        SubElement(
            triangles_element,
            f"{{{_THREEMF_NS}}}triangle",
            attrib={"v1": str(a), "v2": str(b), "v3": str(c)},
        )
    build = SubElement(model, f"{{{_THREEMF_NS}}}build")
    SubElement(build, f"{{{_THREEMF_NS}}}item", attrib={"objectid": "1"})
    model_xml = tostring(model, encoding="utf-8", xml_declaration=True)
    content_types = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
        '<Default Extension="rels" '
        'ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
        '<Default Extension="model" '
        'ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/>'
        "</Types>"
    )
    relationships = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Target="/3D/3dmodel.model" Id="rel0" '
        'Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/>'
        "</Relationships>"
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("[Content_Types].xml", content_types)
        archive.writestr("_rels/.rels", relationships)
        archive.writestr("3D/3dmodel.model", model_xml)
    if not path.exists() or path.stat().st_size == 0:
        raise RuntimeError("3MF export produced an empty artifact.")
    with path.open("rb") as handle:
        if handle.read(2) != b"PK":
            raise RuntimeError("3MF export did not produce a ZIP-based package.")


def _color_to_display_hex(color: tuple[float, float, float, float]) -> str:
    r, g, b, a = color
    return (
        f"#{int(round(r * 255)):02X}"
        f"{int(round(g * 255)):02X}"
        f"{int(round(b * 255)):02X}"
        f"{int(round(a * 255)):02X}"
    )


def write_multi_color_3mf(
    mesh: SimpleMesh,
    path: Path,
    *,
    face_material_indices: list[int],
    palette: list[tuple[float, float, float, float]],
) -> None:
    """Write a multi-material 3MF ZIP package for slicer multi-color workflows."""
    if len(mesh.faces) != len(face_material_indices):
        raise ValueError("face_material_indices length must match triangle count.")
    if not palette:
        raise ValueError("palette must include at least one color.")

    model = Element(
        f"{{{_THREEMF_NS}}}model",
        attrib={
            "unit": "millimeter",
            f"{{{_XML_NS}}}lang": "en-US",
        },
    )
    resources = SubElement(model, f"{{{_THREEMF_NS}}}resources")
    materials_id = "2"
    basematerials = SubElement(
        resources,
        f"{{{_THREEMF_MATERIAL_NS}}}basematerials",
        attrib={"id": materials_id},
    )
    for index, color in enumerate(palette):
        SubElement(
            basematerials,
            f"{{{_THREEMF_MATERIAL_NS}}}base",
            attrib={
                "name": f"Color{index + 1}",
                "displaycolor": _color_to_display_hex(color),
            },
        )
    obj = SubElement(
        resources,
        f"{{{_THREEMF_NS}}}object",
        attrib={"id": "1", "type": "model"},
    )
    mesh_element = SubElement(obj, f"{{{_THREEMF_NS}}}mesh")
    vertices_element = SubElement(mesh_element, f"{{{_THREEMF_NS}}}vertices")
    for x, y, z in mesh.vertices:
        SubElement(
            vertices_element,
            f"{{{_THREEMF_NS}}}vertex",
            attrib={"x": f"{x:.6f}", "y": f"{y:.6f}", "z": f"{z:.6f}"},
        )
    triangles_element = SubElement(mesh_element, f"{{{_THREEMF_NS}}}triangles")
    for face_index, (a, b, c) in enumerate(mesh.faces):
        material_index = face_material_indices[face_index]
        if material_index < 0 or material_index >= len(palette):
            raise ValueError(
                f"face material index {material_index} out of range for palette."
            )
        SubElement(
            triangles_element,
            f"{{{_THREEMF_NS}}}triangle",
            attrib={
                "v1": str(a),
                "v2": str(b),
                "v3": str(c),
                "pid": materials_id,
                "p1": str(material_index),
            },
        )
    build = SubElement(model, f"{{{_THREEMF_NS}}}build")
    SubElement(build, f"{{{_THREEMF_NS}}}item", attrib={"objectid": "1"})
    model_xml = tostring(model, encoding="utf-8", xml_declaration=True)
    content_types = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
        '<Default Extension="rels" '
        'ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
        '<Default Extension="model" '
        'ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/>'
        "</Types>"
    )
    relationships = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Target="/3D/3dmodel.model" Id="rel0" '
        'Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/>'
        "</Relationships>"
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("[Content_Types].xml", content_types)
        archive.writestr("_rels/.rels", relationships)
        archive.writestr("3D/3dmodel.model", model_xml)
    if not path.exists() or path.stat().st_size == 0:
        raise RuntimeError("Multi-color 3MF export produced an empty artifact.")
    with path.open("rb") as handle:
        if handle.read(2) != b"PK":
            raise RuntimeError("Multi-color 3MF export did not produce a ZIP package.")


def _delivery_format_notes(fmt: str) -> str:
    if fmt == "fbx":
        return FBX_GEOMETRY_NOTES
    if fmt == "usdz":
        return USDZ_GEOMETRY_NOTES
    if fmt == "3mf":
        return THREEMF_GEOMETRY_NOTES
    return BLEND_UNAVAILABLE_NOTES


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
        if fmt == "blend":
            blocks[fmt] = {
                "available": False,
                "exported": False,
                "notes": BLEND_UNAVAILABLE_NOTES,
            }
            continue
        exported = fmt in exported_keys
        notes = _delivery_format_notes(fmt)
        blocks[fmt] = {
            "available": True,
            "exported": exported,
            "notes": notes if exported else f"{fmt.upper()} export requested but not written for adapter {adapter!r}.",
        }
    return blocks


def validate_delivery_formats_manifest(
    artifacts: Mapping[str, Any],
    sidecar: Mapping[str, Any],
) -> list[str]:
    """Cross-check optional FBX/USDZ manifest keys against sidecar delivery_formats."""
    issues: list[str] = []
    delivery = sidecar.get("delivery_formats")
    if not isinstance(delivery, dict):
        return issues

    for fmt in DELIVERY_FORMATS:
        block = delivery.get(fmt)
        if not isinstance(block, dict):
            continue
        exported = block.get("exported") is True
        has_key = fmt in artifacts
        if exported and not has_key:
            issues.append(
                f"delivery_formats.{fmt}.exported=true but manifest artifacts missing {fmt}"
            )
        if not exported and has_key:
            issues.append(
                f"Manifest lists {fmt} but delivery_formats.{fmt}.exported is false"
            )
        if exported and has_key:
            artifact_path = artifacts.get(fmt)
            if artifact_path in (None, ""):
                issues.append(f"Manifest {fmt} artifact path is empty")
            else:
                path = Path(str(artifact_path))
                if not path.is_file():
                    if str(artifact_path).startswith("/app/"):
                        continue
                    issues.append(f"Manifest {fmt} artifact path missing on disk: {path}")
                elif path.stat().st_size == 0:
                    issues.append(f"Manifest {fmt} artifact is empty")
    return issues
