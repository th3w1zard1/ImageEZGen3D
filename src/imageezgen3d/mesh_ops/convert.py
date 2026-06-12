from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .backends import (
    SAVE_FORMATS,
    load_mesh,
    mesh_metrics,
    normalized_format,
    save_mesh,
)


@dataclass(frozen=True)
class ConvertReport:
    op: str
    input_path: str
    output_path: str
    input_format: str
    output_format: str
    writer: str
    metrics: dict[str, Any] = field(default_factory=dict)
    notes: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "op": self.op,
            "input_path": self.input_path,
            "output_path": self.output_path,
            "input_format": self.input_format,
            "output_format": self.output_format,
            "writer": self.writer,
            "metrics": self.metrics,
            "notes": self.notes,
        }


def convert_mesh(input_path: Path, output_path: Path) -> ConvertReport:
    """Convert a mesh file to the format implied by output_path's suffix."""
    mesh = load_mesh(Path(input_path))
    out = Path(output_path)
    write_info = save_mesh(mesh, out)
    notes = ""
    if write_info["writer"] == "delivery_exports":
        notes = (
            "Converted via geometry-only delivery writer; material/texture "
            "payloads are not carried into this format."
        )
    return ConvertReport(
        op="convert",
        input_path=str(input_path),
        output_path=str(out),
        input_format=normalized_format(Path(input_path)),
        output_format=write_info["format"],
        writer=write_info["writer"],
        metrics=mesh_metrics(mesh),
        notes=notes,
    )


def supported_convert_formats() -> tuple[str, ...]:
    return SAVE_FORMATS
