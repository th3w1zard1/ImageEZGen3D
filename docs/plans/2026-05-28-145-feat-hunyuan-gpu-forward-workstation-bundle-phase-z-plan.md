---
title: "feat: Hunyuan GPU forward workstation bundle (Phase Z, pre-G7)"
type: feat
status: completed
date: 2026-05-28
origin: docs/plans/2026-05-28-144-feat-hunyuan-gpu-forward-exports-e2e-phase-y-plan.md
---

# feat: Hunyuan GPU forward workstation bundle (Phase Z, pre-G7)

## Summary

Add one-shot workstation evidence bundle (probe + exports E2E attestation + record verify) and CI fixture verify for gpu-forward-e2e JSON.

## Requirements

- R1. `run_gpu_forward_workstation_bundle()` chains probe, exports attestation, and record verify.
- R2. `scripts/hunyuan_gpu_forward_workstation_bundle.py` (default exit 0; `--strict` on verify failure).
- R3. `scripts/verify_gpu_forward_e2e_fixtures.py` validates test fixtures in CI.
- R4. Preflight bundle unchanged; adapter stays disabled on Space.
- R5. Unit tests for bundle skip path and fixture verify.

## Out of scope

- Real tier-C GPU execution on CI
- `IMAGEEZ_HUNYUAN_CONFIGURED=true` on Space
- G7 hosted Block/Vase attestation
