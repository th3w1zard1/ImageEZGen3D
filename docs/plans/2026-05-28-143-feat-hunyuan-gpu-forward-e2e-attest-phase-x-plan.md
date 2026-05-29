---
title: "feat: Hunyuan GPU forward E2E attestation record (Phase X, pre-G7)"
type: feat
status: completed
date: 2026-05-28
origin: docs/plans/2026-05-28-142-feat-hunyuan-gpu-forward-e2e-phase-w-plan.md
---

# feat: Hunyuan GPU forward E2E attestation record (Phase X, pre-G7)

## Summary

Add attestation record schema, `--record` on the E2E CLI, and a verify script so tier-C workstation evidence can be captured and checked before G9 enablement.

## Requirements

- R1. `GpuForwardE2eAttestation` with `record_kind=hunyuan_gpu_forward_e2e`.
- R2. `ok=True` only when `attempt_status=succeeded`, mesh counts pass, and shape/texture stages use `hunyuan-zerogpu`.
- R3. `scripts/hunyuan_gpu_forward_e2e.py --record` writes JSON without changing default stdout.
- R4. `scripts/verify_gpu_forward_e2e_record.py` validates schema and success gates.
- R5. Fixtures + unit tests; preflight bundle unchanged.

## Out of scope

- CI job requiring real GPU E2E success
- `IMAGEEZ_HUNYUAN_CONFIGURED=true` on Space
- G7 hosted Block/Vase attestation
