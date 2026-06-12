"""Backend probes and mesh IO helpers for the mesh_ops toolset.

trimesh is the core backend. Optional backends (manifold3d, xatlas, bpy,
a Blender executable) unlock booleans, UV unwrap, and quad remeshing; every
probe is runtime-checked so hosted deployments degrade honestly instead of
failing at import time.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path
from typing import Any

from ..exporters import SimpleMesh
from ..tencent_mesh_convert import simple_mesh_from_trimesh_like

LOAD_FORMATS: tuple[str, ...] = ("glb", "gltf", "obj", "ply", "stl", "off", "3mf")
NATIVE_SAVE_FORMATS: tuple[str, ...] = ("glb", "gltf", "obj", "ply", "stl")
DELIVERY_SAVE_FORMATS: tuple[str, ...] = ("fbx", "usdz", "3mf")
SAVE_FORMATS: tuple[str, ...] = NATIVE_SAVE_FORMATS + DELIVERY_SAVE_FORMATS


class MeshOpsError(ValueError):
    """Invalid mesh-op input (bad params, unsupported format, bad mesh)."""


class MeshOpsBackendError(RuntimeError):
    """A required optional backend is not available in this environment."""


def module_available(name: str) -> bool:
    try:
        return importlib.util.find_spec(name) is not None
    except (ImportError, ValueError):
        return False


def trimesh_available() -> bool:
    return module_available("trimesh")


def bpy_available() -> bool:
    return module_available("bpy")


def xatlas_available() -> bool:
    return module_available("xatlas")


def manifold_available() -> bool:
    return module_available("manifold3d")


def blender_executable_available() -> bool:
    if not trimesh_available():
        return False
    try:
        from trimesh.interfaces import blender

        return bool(blender.exists)
    except Exception:
        return False


def boolean_engine() -> str | None:
    """Best available trimesh boolean engine, or None."""
    if manifold_available():
        return "manifold"
    if blender_executable_available():
        return "blender"
    return None


def backend_summary() -> dict[str, Any]:
    return {
        "trimesh": trimesh_available(),
        "bpy": bpy_available(),
        "xatlas": xatlas_available(),
        "manifold3d": manifold_available(),
        "blender_executable": blender_executable_available(),
        "boolean_engine": boolean_engine(),
    }


def require_trimesh() -> Any:
    try:
        import trimesh
    except ImportError as exc:  # pragma: no cover - mesh extra is installed in CI
        raise MeshOpsBackendError(
            "mesh_ops requires trimesh. Install with: pip install 'imageezgen3d[mesh]'"
        ) from exc
    return trimesh


def normalized_format(path: Path) -> str:
    suffix = path.suffix.lower().lstrip(".")
    if not suffix:
        raise MeshOpsError(f"Cannot infer mesh format from path without suffix: {path}")
    return suffix


def load_mesh(path: Path) -> Any:
    """Load a mesh file into a single trimesh.Trimesh."""
    trimesh = require_trimesh()
    mesh_path = Path(path)
    if not mesh_path.is_file():
        raise MeshOpsError(f"Mesh file not found: {mesh_path}")
    fmt = normalized_format(mesh_path)
    if fmt not in LOAD_FORMATS:
        raise MeshOpsError(
            f"Unsupported input mesh format '{fmt}'. Supported: {', '.join(LOAD_FORMATS)}"
        )
    loaded = trimesh.load(str(mesh_path), force="mesh")
    if isinstance(loaded, trimesh.Scene):  # pragma: no cover - force="mesh" flattens
        loaded = loaded.to_mesh()
    if loaded.vertices.shape[0] == 0 or loaded.faces.shape[0] == 0:
        raise MeshOpsError(f"Mesh at {mesh_path} has no vertices or faces.")
    return loaded


def save_mesh(mesh: Any, path: Path) -> dict[str, Any]:
    """Save a trimesh.Trimesh to path; format inferred from suffix.

    Native trimesh formats export directly. FBX/USDZ/3MF reuse the repo's
    delivery writers via the SimpleMesh contract (geometry-only).
    """
    out_path = Path(path)
    fmt = normalized_format(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    if fmt in NATIVE_SAVE_FORMATS:
        mesh.export(str(out_path))
        return {"format": fmt, "writer": "trimesh"}
    if fmt in DELIVERY_SAVE_FORMATS:
        from ..delivery_exports import write_3mf, write_fbx, write_usdz

        simple = to_simple_mesh(mesh)
        writer = {"fbx": write_fbx, "usdz": write_usdz, "3mf": write_3mf}[fmt]
        writer(simple, out_path)
        return {"format": fmt, "writer": "delivery_exports"}
    if fmt == "blend":
        raise MeshOpsBackendError(
            "BLEND output requires a Blender (bpy) backend, which is not bundled. "
            "Export GLB and import it in Blender instead."
        )
    raise MeshOpsError(
        f"Unsupported output mesh format '{fmt}'. Supported: {', '.join(SAVE_FORMATS)}"
    )


def to_simple_mesh(mesh: Any) -> SimpleMesh:
    return simple_mesh_from_trimesh_like(mesh)


def mesh_metrics(mesh: Any) -> dict[str, Any]:
    return {
        "vertex_count": int(mesh.vertices.shape[0]),
        "face_count": int(mesh.faces.shape[0]),
        "extents": [round(float(value), 6) for value in mesh.extents],
    }
