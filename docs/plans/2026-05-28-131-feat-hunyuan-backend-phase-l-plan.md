---
title: "feat: Hunyuan dev backend shell (Phase L, pre-G7)"
type: feat
status: completed
date: 2026-05-28
origin: docs/plans/2026-05-28-130-feat-hunyuan-weights-phase-k-plan.md
---

# feat: Hunyuan dev backend shell (Phase L, pre-G7)

## Summary

Add env-gated dev preview backend and weight-verified neural shell so local integrators can exercise the Hunyuan pipeline without enabling the hosted adapter or claiming G7 PASS.

## Requirements

- R1. `DevPreviewHunyuanBackend` returns image-colored preview mesh with staged tracker updates.
- R2. `WeightVerifiedHunyuanBackend` calls `ensure_hunyuan_weights` then raises before tier-C runtime.
- R3. `IMAGEEZ_HUNYUAN_DEV_BACKEND` resolves default backend in `run_hunyuan_shape_texture`.
- R4. Dev runs set honest `preview_disclaimer`; no false neural claims.
- R5. Default Space path unchanged (`configured=False`, dev flag off).

## Out of scope

- Tencent tier-C runtime integration
- G7 hosted attestation
- `IMAGEEZ_HUNYUAN_CONFIGURED=true` on Space
