---
title: "feat: Hunyuan GPU forward exports E2E (Phase Y, pre-G7)"
type: feat
status: completed
date: 2026-05-28
origin: docs/plans/2026-05-28-143-feat-hunyuan-gpu-forward-e2e-attest-phase-x-plan.md
---

# feat: Hunyuan GPU forward exports E2E (Phase Y, pre-G7)

## Summary

Extend GPU forward E2E through `run_hunyuan_shape_texture` with G6 export finalization, attestation artifact gates, and operator CLI.

## Requirements

- R1. `attempt_gpu_forward_workstation_exports_e2e()` runs weight backend + `finalize_hunyuan_exports`.
- R2. Attestation `with_exports=true` requires manifest/GLB/OBJ/export_sidecar size gates.
- R3. `scripts/hunyuan_gpu_forward_exports_e2e.py` with `--record` support.
- R4. Preflight bundle unchanged; adapter stays disabled on Space.
- R5. Unit tests for exports attestation gates and CLI skip path.

## Out of scope

- Real tier-C GPU execution on CI
- `IMAGEEZ_HUNYUAN_CONFIGURED=true` on Space
- G7 hosted Block/Vase attestation
