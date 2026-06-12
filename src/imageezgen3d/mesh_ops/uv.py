from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .backends import (
    MeshOpsBackendError,
    MeshOpsError,
    load_mesh,
    require_trimesh,
    xatlas_available,
)

UV_OUTPUT_FORMATS = ("obj", "glb")


@dataclass(frozen=True)
class UnwrapReport:
    op: str
    backend: str
    input_path: str
    output_path: str
    uv_vertex_count: int
    face_count: int
    metrics: dict[str, Any] = field(default_factory=dict)
    notes: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "op": self.op,
            "backend": self.backend,
            "input_path": self.input_path,
            "output_path": self.output_path,
            "uv_vertex_count": self.uv_vertex_count,
            "face_count": self.face_count,
            "metrics": self.metrics,
            "notes": self.notes,
        }


def unwrap_uv(input_path: Path, output_path: Path) -> UnwrapReport:
    out = Path(output_path)
    fmt = out.suffix.lower().lstrip(".")
    if fmt not in UV_OUTPUT_FORMATS:
        raise MeshOpsError(
            f"UV unwrap output must be one of: {', '.join(UV_OUTPUT_FORMATS)}"
        )
    if not xatlas_available():
        raise MeshOpsBackendError(
            "UV unwrap needs the xatlas backend (pip install xatlas). "
            "A Blender (bpy) smart-projection path is documented but not bundled."
        )
    import numpy as np
    import xatlas

    trimesh = require_trimesh()
    mesh = load_mesh(Path(input_path))
    vmapping, indices, uvs = xatlas.parametrize(
        np.asarray(mesh.vertices, dtype=np.float64),
        np.asarray(mesh.faces, dtype=np.uint32),
    )
    unwrapped = trimesh.Trimesh(
        vertices=np.asarray(mesh.vertices)[vmapping],
        faces=indices,
        process=False,
    )
    unwrapped.visual = trimesh.visual.TextureVisuals(uv=uvs)
    out.parent.mkdir(parents=True, exist_ok=True)
    unwrapped.export(str(out))
    return UnwrapReport(
        op="unwrap_uv",
        backend="xatlas",
        input_path=str(input_path),
        output_path=str(out),
        uv_vertex_count=int(uvs.shape[0]),
        face_count=int(indices.shape[0]),
        metrics={
            "vertex_count": int(unwrapped.vertices.shape[0]),
            "face_count": int(unwrapped.faces.shape[0]),
        },
    )
