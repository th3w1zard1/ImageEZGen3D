---
title: "feat: Hunyuan GPU forward E2E attempt (Phase W, pre-G7)"
type: feat
status: completed
date: 2026-05-28
origin: docs/plans/2026-05-28-141-feat-hunyuan-gpu-forward-probe-phase-v-plan.md
---

# feat: Hunyuan GPU forward E2E attempt (Phase W, pre-G7)

## Summary

Add an operator CLI that attempts weight-verified Tencent GPU forward when Phase V workstation gates pass — skips honestly on CI/Space, does not enable the adapter.

## Requirements

- R1. `attempt_gpu_forward_workstation_e2e()` runs `WeightVerifiedHunyuanBackend` when readiness passes.
- R2. `scripts/hunyuan_gpu_forward_e2e.py` (default exit 0; `--strict` for failed attempts).
- R3. Report `attempt_status`: `skipped`, `not_implemented`, `failed`, or `succeeded`.
- R4. Preflight bundle unchanged; `configured=False` on Space.
- R5. Unit tests cover skip path and mocked success/failure without tier-C install.

## Operator env (tier-C workstation only)

```bash
export IMAGEEZ_HUNYUAN_GPU_FORWARD=true
export IMAGEEZ_HUNYUAN_INFERENCE_RUNNER=tencent
export IMAGEEZ_HUNYUAN_WEIGHT_BACKEND=true
PYTHONPATH=src python scripts/hunyuan_gpu_forward_e2e.py
```

## Out of scope

- `IMAGEEZ_HUNYUAN_CONFIGURED=true` on Space
- G7 hosted Block/Vase attestation
- Claiming neural success on CI without real GPU forward evidence
