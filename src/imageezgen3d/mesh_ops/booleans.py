"""Boolean mesh ops (Blender-parity extra; not part of the Meshy surface).

Requires a boolean engine: manifold3d (pip install manifold3d) or a Blender
executable on PATH. Degrades with an explicit backend error otherwise.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .backends import (
    MeshOpsBackendError,
    MeshOpsError,
    boolean_engine,
    load_mesh,
    mesh_metrics,
    require_trimesh,
    save_mesh,
)

VALID_OPERATIONS = ("union", "difference", "intersection")


@dataclass(frozen=True)
class BooleanReport:
    op: str
    operation: str
    engine: str
    input_paths: list[str]
    output_path: str
    metrics: dict[str, Any] = field(default_factory=dict)
    notes: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "op": self.op,
            "operation": self.operation,
            "engine": self.engine,
            "input_paths": self.input_paths,
            "output_path": self.output_path,
            "metrics": self.metrics,
            "notes": self.notes,
        }


def boolean_mesh(
    first_path: Path,
    second_path: Path,
    output_path: Path,
    *,
    operation: str = "union",
) -> BooleanReport:
    if operation not in VALID_OPERATIONS:
        raise MeshOpsError(
            f"Invalid boolean operation '{operation}'. "
            f"Choose one of: {', '.join(VALID_OPERATIONS)}"
        )
    engine = boolean_engine()
    if engine is None:
        raise MeshOpsBackendError(
            "Boolean operations need an engine. Install manifold3d "
            "(pip install manifold3d) or make a Blender executable available "
            "on PATH."
        )
    trimesh = require_trimesh()
    first = load_mesh(Path(first_path))
    second = load_mesh(Path(second_path))
    result = getattr(trimesh.boolean, operation)([first, second], engine=engine)
    if result.is_empty or result.faces.shape[0] == 0:
        raise MeshOpsError(
            f"Boolean {operation} produced an empty mesh; check that the "
            "inputs overlap as expected."
        )
    out = Path(output_path)
    save_mesh(result, out)
    return BooleanReport(
        op="boolean",
        operation=operation,
        engine=engine,
        input_paths=[str(first_path), str(second_path)],
        output_path=str(out),
        metrics=mesh_metrics(result),
    )
