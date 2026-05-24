---
title: "feat: Mesh decimation post-process and RAW export tier"
type: feat
status: completed
date: 2026-05-24
origin: docs/ideation/2026-05-24-post-trust-slice-refresh.md
---

# feat: Mesh decimation post-process and RAW export tier

## Summary

Apply a real decimation pass when face count exceeds the quality-tier budget, write a pre-decimation **RAW** GLB alongside tier exports, and record before/after topology in the export sidecar.

## Requirements

- R1. `mesh_decimation.decimate_mesh(mesh, target_faces)` — reduce faces when over budget (smallest-face removal MVP)
- R2. `mesh_decimation.subdivide_mesh(mesh, levels)` — optional densification for CPU demo balanced/high paths
- R3. `export_all` accepts optional `raw_mesh`; writes `{stem}.raw.glb` when provided
- R4. `build_export_sidecar` / CPU demo — `decimation_applied`, `faces_before`, `faces_after`, `raw_exported`
- R5. Golden + cpu_demo tests updated for decimation metadata
- R6. 105+ tests; style guard + ruff clean

## Scope Boundaries

- Quadric decimation / trimesh — deferred
- Neural backend integration — adapters call same export path later
- Hunyuan enablement — deferred

## Files

- Add: `src/imageezgen3d/mesh_decimation.py`
- Add: `tests/test_mesh_decimation.py`
- Modify: `src/imageezgen3d/exporters.py`, `src/imageezgen3d/export_tiers.py`, `src/imageezgen3d/adapters/cpu_demo.py`
- Modify: `tests/test_cpu_demo.py`, `tests/test_export_tiers.py`
