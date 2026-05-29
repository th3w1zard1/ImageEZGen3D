---
title: "feat: Tencent Hunyuan inference runner shell (Phase P, pre-G7)"
type: feat
status: completed
date: 2026-05-28
origin: docs/plans/2026-05-28-134-feat-hunyuan-inference-runner-phase-o-plan.md
---

# feat: Tencent Hunyuan inference runner shell (Phase P, pre-G7)

## Summary

Register a `TencentHunyuanInferenceRunner` when `IMAGEEZ_HUNYUAN_INFERENCE_RUNNER=tencent`, validating weight checkpoints and staging tracker updates before stopping at honest `NotImplementedError` — without enabling the hosted adapter or claiming G7 PASS.

## Requirements

- R1. `HunyuanSettings.inference_runner` env/config seam (`IMAGEEZ_HUNYUAN_INFERENCE_RUNNER`).
- R2. `resolve_hunyuan_inference_runner()` returns `TencentHunyuanInferenceRunner` for `tencent`.
- R3. Runner verifies `shape_checkpoint` and fails before neural claims.
- R4. Unit tests mock paths; no tier-C install required in CI.
- R5. Admission preflight bundle remains exit 0 with `configured=False`.

## Out of scope

- Full Tencent upstream pipeline integration
- `IMAGEEZ_HUNYUAN_CONFIGURED=true` on Space
- G7 hosted attestation
