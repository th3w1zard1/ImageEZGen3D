---
title: "feat: Hunyuan runtime probe + operator CLIs (Phase M, pre-G7)"
type: feat
status: completed
date: 2026-05-28
origin: docs/plans/2026-05-28-131-feat-hunyuan-backend-phase-l-plan.md
---

# feat: Hunyuan runtime probe + operator CLIs (Phase M, pre-G7)

## Summary

Add tier B/C import probing and operator CLIs for weight warm + runtime surface checks so integrators can diagnose env readiness without enabling the adapter or claiming G7 PASS.

## Requirements

- R1. `probe_hunyuan_runtime()` reports tier B/C module availability and weight pin metadata.
- R2. `scripts/hunyuan_tier_c_probe.py` prints human or JSON probe (informational exit 0).
- R3. `scripts/hunyuan_warm_weights.py` wraps `ensure_hunyuan_weights()` with `--describe-only`.
- R4. Unit tests cover probe structure and script smoke without requiring tier C installs.
- R5. Admission preflight bundle remains exit 0 with `configured=False`.

## Out of scope

- Tencent tier-C inference wiring in `WeightVerifiedHunyuanBackend`
- `IMAGEEZ_HUNYUAN_CONFIGURED=true` on Space
- G7 hosted attestation update
