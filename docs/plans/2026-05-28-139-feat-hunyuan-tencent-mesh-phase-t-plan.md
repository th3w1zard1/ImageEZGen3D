---
title: "feat: Tencent mesh conversion + forward executor shell (Phase T, pre-G7)"
type: feat
status: completed
date: 2026-05-28
origin: docs/plans/2026-05-28-138-feat-hunyuan-tencent-forward-phase-s-plan.md
---

# feat: Tencent mesh conversion + forward executor shell (Phase T, pre-G7)

## Summary

Add trimesh/OBJ to `SimpleMesh` conversion, pluggable shape/texture forward executors, and runner assembly of `HunyuanMeshResult` when injected executors complete — default executors still stop before GPU inference.

## Requirements

- R1. `tencent_mesh_convert.simple_mesh_from_obj()` and trimesh-like conversion helper.
- R2. `tencent_hunyuan_forward` defines default executors that raise before neural load.
- R3. Stage helpers accept optional executors; runner returns `HunyuanMeshResult` on injected success path.
- R4. Unit tests cover conversion and injected executor end-to-end without tier-C deps.
- R5. Preflight bundle remains exit 0 with `configured=False`.

## Out of scope

- Default GPU `from_pretrained` / `__call__` on Space or CI
- `IMAGEEZ_HUNYUAN_CONFIGURED=true`
- G7 hosted attestation
