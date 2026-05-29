---
title: "feat: Tencent shape+texture pipeline probes (Phase Q, pre-G7)"
type: feat
status: completed
date: 2026-05-28
origin: docs/plans/2026-05-28-135-feat-hunyuan-tencent-runner-phase-p-plan.md
---

# feat: Tencent shape+texture pipeline probes (Phase Q, pre-G7)

## Summary

Add staged Tencent upstream module probes for shape and texture towers inside `TencentHunyuanInferenceRunner`, with operator CLI — stopping at honest `NotImplementedError` before neural execution.

## Requirements

- R1. Document pinned upstream entrypoints (`hy3dshape`, `hy3dpaint`) at commit `82920d64`.
- R2. `probe_tencent_pipeline_modules()` reports shape/texture import availability.
- R3. Runner validates checkpoint, probes modules, stages shape then texture tracker updates before stop.
- R4. `scripts/hunyuan_tencent_pipeline_probe.py` (informational exit 0).
- R5. Admission preflight bundle remains exit 0 with `configured=False`.

## Out of scope

- Calling upstream neural inference APIs
- `IMAGEEZ_HUNYUAN_CONFIGURED=true` on Space
- G7 hosted attestation
