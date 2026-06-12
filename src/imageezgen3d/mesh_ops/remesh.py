"""Remesh mesh op (Meshy Remesh parity, local implementation).

Triangle remeshing to a target polycount is real on CPU: subdivision to
densify when the target exceeds the current count, quadric decimation
(fast-simplification via trimesh) to reduce. Quad topology requires a
Blender (bpy) backend; without it the op falls back to triangles and says so.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .backends import (
    MeshOpsError,
    bpy_available,
    load_mesh,
    mesh_metrics,
    save_mesh,
)

VALID_TOPOLOGIES = ("triangle", "quad")
DEFAULT_TARGET_POLYCOUNT = 30_000
QUAD_FALLBACK_NOTE = (
    "Quad topology requires a Blender (bpy) backend, which is not available; "
    "exported triangle topology instead."
)
MAX_SUBDIVISION_ROUNDS = 6


@dataclass(frozen=True)
class RemeshReport:
    op: str
    input_path: str
    output_path: str
    topology_requested: str
    topology_applied: str
    target_polycount: int
    faces_before: int
    faces_after: int
    subdivision_rounds: int
    decimation_applied: bool
    metrics: dict[str, Any] = field(default_factory=dict)
    notes: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "op": self.op,
            "input_path": self.input_path,
            "output_path": self.output_path,
            "topology_requested": self.topology_requested,
            "topology_applied": self.topology_applied,
            "target_polycount": self.target_polycount,
            "faces_before": self.faces_before,
            "faces_after": self.faces_after,
            "subdivision_rounds": self.subdivision_rounds,
            "decimation_applied": self.decimation_applied,
            "metrics": self.metrics,
            "notes": self.notes,
        }


def remesh_mesh(
    input_path: Path,
    output_path: Path,
    *,
    target_polycount: int = DEFAULT_TARGET_POLYCOUNT,
    topology: str = "triangle",
) -> RemeshReport:
    if topology not in VALID_TOPOLOGIES:
        raise MeshOpsError(
            f"Invalid topology '{topology}'. Choose one of: {', '.join(VALID_TOPOLOGIES)}"
        )
    if target_polycount < 4:
        raise MeshOpsError("target_polycount must be at least 4.")

    mesh = load_mesh(Path(input_path))
    faces_before = int(mesh.faces.shape[0])
    notes = ""
    topology_applied = topology
    if topology == "quad" and not bpy_available():
        topology_applied = "triangle"
        notes = QUAD_FALLBACK_NOTE

    subdivision_rounds = 0
    while (
        mesh.faces.shape[0] < target_polycount
        and subdivision_rounds < MAX_SUBDIVISION_ROUNDS
    ):
        mesh = mesh.subdivide()
        subdivision_rounds += 1

    decimation_applied = False
    if mesh.faces.shape[0] > target_polycount:
        mesh = mesh.simplify_quadric_decimation(face_count=target_polycount)
        decimation_applied = True

    out = Path(output_path)
    save_mesh(mesh, out)
    return RemeshReport(
        op="remesh",
        input_path=str(input_path),
        output_path=str(out),
        topology_requested=topology,
        topology_applied=topology_applied,
        target_polycount=target_polycount,
        faces_before=faces_before,
        faces_after=int(mesh.faces.shape[0]),
        subdivision_rounds=subdivision_rounds,
        decimation_applied=decimation_applied,
        metrics=mesh_metrics(mesh),
        notes=notes,
    )
