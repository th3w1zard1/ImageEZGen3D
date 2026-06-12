"""Resize mesh op (Meshy Resize parity, local implementation).

Mirrors Meshy's parameter contract: exactly one of resize_height,
resize_longest_side, or auto_size must be provided. auto_size here is an
honest heuristic (longest side scaled to 1.0 m) — not AI vision estimation.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .backends import MeshOpsError, load_mesh, mesh_metrics, save_mesh

# glTF convention: +Y is up. OBJ exports from this repo follow the same axis.
HEIGHT_AXIS = 1
AUTO_SIZE_LONGEST_SIDE_M = 1.0
AUTO_SIZE_NOTE = (
    "auto_size used a heuristic default (longest side = 1.0 m); "
    "AI vision size estimation is not part of the local toolset."
)

VALID_ORIGINS = ("bottom", "center", "unchanged")


@dataclass(frozen=True)
class ResizeReport:
    op: str
    input_path: str
    output_path: str
    mode: str
    scale_factor: float
    origin_at: str
    extents_before: list[float]
    extents_after: list[float]
    metrics: dict[str, Any] = field(default_factory=dict)
    notes: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "op": self.op,
            "input_path": self.input_path,
            "output_path": self.output_path,
            "mode": self.mode,
            "scale_factor": self.scale_factor,
            "origin_at": self.origin_at,
            "extents_before": self.extents_before,
            "extents_after": self.extents_after,
            "metrics": self.metrics,
            "notes": self.notes,
        }


def resize_mesh(
    input_path: Path,
    output_path: Path,
    *,
    resize_height: float | None = None,
    resize_longest_side: float | None = None,
    auto_size: bool = False,
    origin_at: str = "bottom",
) -> ResizeReport:
    modes_set = [
        resize_height is not None,
        resize_longest_side is not None,
        bool(auto_size),
    ]
    if sum(modes_set) == 0:
        raise MeshOpsError(
            "Exactly one resize mode is required: resize_height, "
            "resize_longest_side, or auto_size."
        )
    if sum(modes_set) > 1:
        raise MeshOpsError(
            "resize_height, resize_longest_side, and auto_size are mutually "
            "exclusive."
        )
    if origin_at not in VALID_ORIGINS:
        raise MeshOpsError(
            f"Invalid origin_at '{origin_at}'. Choose one of: {', '.join(VALID_ORIGINS)}"
        )

    mesh = load_mesh(Path(input_path))
    extents_before = [float(value) for value in mesh.extents]
    notes = ""

    if resize_height is not None:
        if resize_height <= 0:
            raise MeshOpsError("resize_height must be positive.")
        current = extents_before[HEIGHT_AXIS]
        mode = "height"
        target = float(resize_height)
    elif resize_longest_side is not None:
        if resize_longest_side <= 0:
            raise MeshOpsError("resize_longest_side must be positive.")
        current = max(extents_before)
        mode = "longest_side"
        target = float(resize_longest_side)
    else:
        current = max(extents_before)
        mode = "auto"
        target = AUTO_SIZE_LONGEST_SIDE_M
        notes = AUTO_SIZE_NOTE

    if current <= 0:
        raise MeshOpsError("Mesh has zero extent along the requested axis.")

    scale = target / current
    mesh.apply_scale(scale)

    if origin_at == "bottom":
        bounds_min = mesh.bounds[0]
        translation = [0.0, 0.0, 0.0]
        translation[HEIGHT_AXIS] = -float(bounds_min[HEIGHT_AXIS])
        mesh.apply_translation(translation)
    elif origin_at == "center":
        mesh.apply_translation([-float(value) for value in mesh.bounds.mean(axis=0)])

    out = Path(output_path)
    save_mesh(mesh, out)
    return ResizeReport(
        op="resize",
        input_path=str(input_path),
        output_path=str(out),
        mode=mode,
        scale_factor=round(scale, 9),
        origin_at=origin_at,
        extents_before=[round(value, 6) for value in extents_before],
        extents_after=[round(float(value), 6) for value in mesh.extents],
        metrics=mesh_metrics(mesh),
        notes=notes,
    )
