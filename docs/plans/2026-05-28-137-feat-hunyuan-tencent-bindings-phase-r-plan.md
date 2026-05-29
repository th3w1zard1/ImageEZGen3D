---
title: "feat: Tencent upstream pipeline class bindings (Phase R, pre-G7)"
type: feat
status: completed
date: 2026-05-28
origin: docs/plans/2026-05-28-136-feat-hunyuan-tencent-pipeline-phase-q-plan.md
---

# feat: Tencent upstream pipeline class bindings (Phase R, pre-G7)

## Summary

Resolve pinned upstream pipeline classes (`Hunyuan3DDiTPipeline`, `Hunyuan3DPaintPipeline`) from Phase Q module probes, pass stage context from the Tencent runner, and stop at honest `NotImplementedError` before the neural forward pass.

## Requirements

- R1. Document upstream class symbols at commit `82920d64`.
- R2. `resolve_tencent_pipeline_bindings()` reports shape/texture class resolution.
- R3. `TencentStageContext` carries checkpoint, weight root, image, and run dir into stage helpers.
- R4. Runner invokes shape then texture stage helpers with tracker updates before stop.
- R5. Probe CLI reports binding readiness; preflight bundle remains exit 0 with `configured=False`.

## Out of scope

- Calling upstream `from_pretrained` / `__call__` neural forward
- `IMAGEEZ_HUNYUAN_CONFIGURED=true` on Space
- G7 hosted attestation
