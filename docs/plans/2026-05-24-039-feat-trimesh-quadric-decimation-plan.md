---
title: "feat: Trimesh quadric decimation with MVP fallback"
type: feat
status: completed
date: 2026-05-24
origin: docs/ideation/2026-05-24-post-trust-slice-refresh.md
---

# feat: Trimesh quadric decimation with MVP fallback

## Summary

Replace largest-face decimation MVP with `trimesh` quadric simplification when `trimesh` and `fast-simplification` are installed; keep the existing MVP path as fallback. Record `decimation_method` in decimation metadata for export sidecar transparency.

## Requirements

- R1. `decimate_mesh` tries quadric via `Trimesh.simplify_quadric_decimation(face_count=target_faces)` when dependencies available
- R2. On import failure or quadric error, fall back to largest-face MVP (current behavior)
- R3. Decimation metadata includes `decimation_method`: `quadric` or `largest_face_mvp`
- R4. Optional extra `mesh = ["trimesh>=4.4", "fast-simplification>=0.1"]`; install in CI, Dockerfile, and `requirements.txt` for Space
- R5. Tests: quadric reduces faces when trimesh installed; fallback path when trimesh import blocked
- R6. 110+ tests; ruff clean on touched files

## Scope Boundaries

- Hunyuan enablement — deferred
- Neural adapter hookup — deferred (CPU demo uses same `decimate_mesh`)
- Ship PR #21 docs — merge to `main` before feature branch (no code in that PR)

## Files

- Modify: `src/imageezgen3d/mesh_decimation.py`
- Modify: `pyproject.toml`, `requirements.txt`, `Dockerfile`
- Modify: `.github/workflows/ci.yml`, `.github/workflows/hosted-golden-smoke.yml` (install `[mesh]` extra)
- Modify: `tests/test_mesh_decimation.py`

## Test scenarios

- TS1: With trimesh available, decimate dense mesh to 100 faces → `decimation_method=quadric`, `faces_after<=100`
- TS2: With `trimesh` import patched to fail, same call → `decimation_method=largest_face_mvp`, faces exactly 100
- TS3: Under-budget mesh → noop, no `decimation_method` change to applied path
