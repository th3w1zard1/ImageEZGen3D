"""Printability analyze/repair mesh ops (Meshy 3D-print parity, local).

Analysis mirrors Meshy's report fields: is_watertight, volume,
non_manifold_edges, degenerate_faces, holes, plus error/warning rollups.
Repair fixes what trimesh can fix deterministically on CPU: merge vertices,
drop degenerate/duplicate faces, fill simple holes, fix winding and normals.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .backends import load_mesh, mesh_metrics, require_trimesh, save_mesh

DEGENERATE_AREA_EPSILON = 1e-12


@dataclass(frozen=True)
class PrintabilityAnalysis:
    is_watertight: bool
    volume: float
    non_manifold_edges: int
    degenerate_faces: int
    holes: int
    error_count: int
    warning_count: int
    metrics: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "is_watertight": self.is_watertight,
            "volume": self.volume,
            "non_manifold_edges": self.non_manifold_edges,
            "degenerate_faces": self.degenerate_faces,
            "holes": self.holes,
            "error_count": self.error_count,
            "warning_count": self.warning_count,
            "metrics": self.metrics,
        }


@dataclass(frozen=True)
class PrintabilityRepairReport:
    op: str
    input_path: str
    output_path: str
    before: PrintabilityAnalysis
    after: PrintabilityAnalysis
    actions: list[str] = field(default_factory=list)
    notes: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "op": self.op,
            "input_path": self.input_path,
            "output_path": self.output_path,
            "before": self.before.to_dict(),
            "after": self.after.to_dict(),
            "actions": self.actions,
            "notes": self.notes,
        }


def _count_boundary_loops(boundary_edges: list[tuple[int, int]]) -> int:
    """Count connected components of boundary edges via union-find."""
    parent: dict[int, int] = {}

    def find(item: int) -> int:
        root = item
        while parent.setdefault(root, root) != root:
            root = parent[root]
        while parent[item] != root:
            parent[item], item = root, parent[item]
        return root

    for first, second in boundary_edges:
        parent[find(first)] = find(second)
    return len({find(vertex) for vertex in parent})


def _edge_face_counts(mesh: Any) -> dict[str, int]:
    import numpy as np

    edges = np.sort(mesh.edges, axis=1)
    unique_edges, edge_counts = np.unique(edges, axis=0, return_counts=True)
    boundary = unique_edges[edge_counts == 1]
    non_manifold = int((edge_counts > 2).sum())
    boundary_edges = [(int(edge[0]), int(edge[1])) for edge in boundary]
    return {
        "non_manifold_edges": non_manifold,
        "holes": _count_boundary_loops(boundary_edges),
    }


def _analyze(mesh: Any) -> PrintabilityAnalysis:
    import numpy as np

    edge_info = _edge_face_counts(mesh)
    degenerate = int((mesh.area_faces <= DEGENERATE_AREA_EPSILON).sum())
    is_watertight = bool(mesh.is_watertight)
    volume = float(mesh.volume) if mesh.is_volume else float(abs(mesh.volume))
    errors = 0
    if not is_watertight:
        errors += 1
    if volume <= 0 or not np.isfinite(volume):
        errors += 1
    if edge_info["non_manifold_edges"] > 0:
        errors += 1
    warnings = 0
    if degenerate > 0:
        warnings += 1
    if edge_info["holes"] > 0:
        warnings += 1
    return PrintabilityAnalysis(
        is_watertight=is_watertight,
        volume=round(volume, 9),
        non_manifold_edges=edge_info["non_manifold_edges"],
        degenerate_faces=degenerate,
        holes=edge_info["holes"],
        error_count=errors,
        warning_count=warnings,
        metrics=mesh_metrics(mesh),
    )


def analyze_printability(input_path: Path) -> PrintabilityAnalysis:
    mesh = load_mesh(Path(input_path))
    return _analyze(mesh)


def repair_printability(
    input_path: Path, output_path: Path
) -> PrintabilityRepairReport:
    trimesh = require_trimesh()
    mesh = load_mesh(Path(input_path))
    before = _analyze(mesh)
    actions: list[str] = []

    mesh.merge_vertices()
    actions.append("merge_vertices")
    nondegenerate = mesh.nondegenerate_faces()
    if int((~nondegenerate).sum()) > 0:
        mesh.update_faces(nondegenerate)
        actions.append("drop_degenerate_faces")
    unique = mesh.unique_faces()
    if int((~unique).sum()) > 0:
        mesh.update_faces(unique)
        actions.append("drop_duplicate_faces")
    mesh.remove_unreferenced_vertices()
    actions.append("remove_unreferenced_vertices")
    if not mesh.is_watertight:
        try:
            filled = trimesh.repair.fill_holes(mesh)
            actions.append("fill_holes" + ("" if filled else "_partial"))
        except ModuleNotFoundError as exc:
            # trimesh's hole filling needs networkx; degrade honestly.
            actions.append(f"fill_holes_unavailable ({exc})")
    trimesh.repair.fix_winding(mesh)
    trimesh.repair.fix_inversion(mesh)
    trimesh.repair.fix_normals(mesh)
    actions.append("fix_winding_and_normals")

    after = _analyze(mesh)
    out = Path(output_path)
    save_mesh(mesh, out)
    notes = ""
    if not after.is_watertight:
        notes = (
            "Mesh is still not watertight after CPU repair; complex holes may "
            "need manual repair in a DCC tool."
        )
    return PrintabilityRepairReport(
        op="repair_printability",
        input_path=str(input_path),
        output_path=str(out),
        before=before,
        after=after,
        actions=actions,
        notes=notes,
    )
