from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import numpy as np

from ..delivery_exports import write_multi_color_3mf
from ..tencent_mesh_convert import simple_mesh_from_trimesh_like
from .backends import load_mesh, require_trimesh

DEFAULT_MAX_COLORS = 4
DEFAULT_MAX_DEPTH = 4
MIN_MAX_COLORS = 1
MAX_MAX_COLORS = 16
MIN_MAX_DEPTH = 3
MAX_MAX_DEPTH = 6


@dataclass(frozen=True)
class MultiColorPrintReport:
    op: str
    input_path: str
    output_path: str
    max_colors: int
    max_depth: int
    colors_used: int
    palette: list[tuple[float, float, float, float]] = field(default_factory=list)
    notes: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "op": self.op,
            "input_path": self.input_path,
            "output_path": self.output_path,
            "max_colors": self.max_colors,
            "max_depth": self.max_depth,
            "colors_used": self.colors_used,
            "palette": [list(color) for color in self.palette],
            "notes": self.notes,
        }


def validate_max_colors(value: int | None) -> int:
    resolved = DEFAULT_MAX_COLORS if value is None else int(value)
    if resolved < MIN_MAX_COLORS or resolved > MAX_MAX_COLORS:
        raise ValueError(
            f"max_colors must be between {MIN_MAX_COLORS} and {MAX_MAX_COLORS}."
        )
    return resolved


def validate_max_depth(value: int | None) -> int:
    resolved = DEFAULT_MAX_DEPTH if value is None else int(value)
    if resolved < MIN_MAX_DEPTH or resolved > MAX_MAX_DEPTH:
        raise ValueError(
            f"max_depth must be between {MIN_MAX_DEPTH} and {MAX_MAX_DEPTH}."
        )
    return resolved


def multi_color_print(
    input_path: Path,
    output_path: Path,
    *,
    max_colors: int | None = None,
    max_depth: int | None = None,
) -> MultiColorPrintReport:
    require_trimesh()
    resolved_colors = validate_max_colors(max_colors)
    resolved_depth = validate_max_depth(max_depth)
    mesh = load_mesh(input_path)
    face_indices, palette = _assign_face_palette(mesh, resolved_colors, resolved_depth)
    simple_mesh = simple_mesh_from_trimesh_like(mesh)
    write_multi_color_3mf(
        simple_mesh,
        output_path,
        face_material_indices=face_indices,
        palette=palette,
    )
    return MultiColorPrintReport(
        op="multi-color-print",
        input_path=str(input_path),
        output_path=str(output_path),
        max_colors=resolved_colors,
        max_depth=resolved_depth,
        colors_used=len(palette),
        palette=palette,
        notes=(
            "Demo multi-color 3MF: spatial palette quantization for slicer-ready "
            "geometry when vertex colors are unavailable."
        ),
    )


def _assign_face_palette(
    mesh: Any,
    max_colors: int,
    max_depth: int,
) -> tuple[list[int], list[tuple[float, float, float, float]]]:
    face_colors = _face_colors(mesh)
    bucket_ids = _spatial_bucket_ids(mesh, max_depth)
    palette, index_by_bucket = _build_palette(
        face_colors,
        bucket_ids,
        max_colors=max_colors,
    )
    face_indices = [index_by_bucket[bucket] for bucket in bucket_ids]
    return face_indices, palette


def _face_colors(mesh: Any) -> np.ndarray:
    visual = getattr(mesh, "visual", None)
    vertex_colors = getattr(visual, "vertex_colors", None) if visual is not None else None
    if vertex_colors is not None and len(vertex_colors):
        colors = np.asarray(vertex_colors, dtype=np.float64)
        if colors.max() > 1.0:
            colors = colors / 255.0
        return colors[mesh.faces].mean(axis=1)[:, :3]

    centroids = np.asarray(mesh.triangles_center, dtype=np.float64)
    bounds = np.asarray(mesh.bounds, dtype=np.float64)
    spans = bounds[1] - bounds[0]
    spans[spans == 0.0] = 1.0
    normalized = (centroids - bounds[0]) / spans
    return np.clip(normalized, 0.0, 1.0)


def _spatial_bucket_ids(mesh: Any, max_depth: int) -> np.ndarray:
    centroids = np.asarray(mesh.triangles_center, dtype=np.float64)
    bounds = np.asarray(mesh.bounds, dtype=np.float64)
    spans = bounds[1] - bounds[0]
    spans[spans == 0.0] = 1.0
    normalized = (centroids - bounds[0]) / spans
    grid = max(2, min(2**max_depth, 64))
    cells = np.clip((normalized * (grid - 1)).astype(np.int64), 0, grid - 1)
    return cells[:, 0] * grid * grid + cells[:, 1] * grid + cells[:, 2]


def _build_palette(
    face_colors: np.ndarray,
    bucket_ids: np.ndarray,
    *,
    max_colors: int,
) -> tuple[list[tuple[float, float, float, float]], dict[int, int]]:
    unique_buckets, inverse = np.unique(bucket_ids, return_inverse=True)
    bucket_means: dict[int, np.ndarray] = {}
    for bucket in unique_buckets:
        mask = bucket_ids == bucket
        bucket_means[int(bucket)] = face_colors[mask].mean(axis=0)

    ranked = sorted(
        bucket_means.items(),
        key=lambda item: int(np.sum(bucket_ids == item[0])),
        reverse=True,
    )
    selected = ranked[:max_colors]
    palette: list[tuple[float, float, float, float]] = []
    index_by_bucket: dict[int, int] = {}
    for index, (bucket, rgb) in enumerate(selected):
        r, g, b = (float(np.clip(channel, 0.0, 1.0)) for channel in rgb[:3])
        palette.append((r, g, b, 1.0))
        index_by_bucket[bucket] = index

    fallback = palette[-1] if palette else (0.5, 0.5, 0.5, 1.0)
    if not palette:
        palette.append(fallback)
        index_by_bucket = {int(bucket): 0 for bucket in unique_buckets}
    else:
        default_index = 0
        for bucket in unique_buckets:
            bucket_int = int(bucket)
            if bucket_int not in index_by_bucket:
                index_by_bucket[bucket_int] = default_index

    _ = inverse  # bucket assignment already encoded in index_by_bucket lookup
    return palette, index_by_bucket
