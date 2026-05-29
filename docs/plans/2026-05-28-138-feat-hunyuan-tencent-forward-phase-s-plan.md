---
title: "feat: Tencent upstream forward plan scaffolding (Phase S, pre-G7)"
type: feat
status: completed
date: 2026-05-28
origin: docs/plans/2026-05-28-137-feat-hunyuan-tencent-bindings-phase-r-plan.md
---

# feat: Tencent upstream forward plan scaffolding (Phase S, pre-G7)

## Summary

Document and build pinned upstream `from_pretrained` / `__call__` forward plans for Tencent shape and texture towers, pass planned mesh paths between stages, and stop at honest `NotImplementedError` before neural execution.

## Requirements

- R1. `TencentShapeForwardPlan` / `TencentTextureForwardPlan` mirror upstream @ `82920d64`.
- R2. `describe_tencent_forward_contract()` exposed in pipeline probe output.
- R3. Stage helpers validate plans and bindings before raising on unwired `__call__`.
- R4. Runner passes planned shape mesh path into texture stage.
- R5. Preflight bundle remains exit 0 with `configured=False`.

## Out of scope

- Loading pipelines on GPU or invoking upstream `__call__`
- `IMAGEEZ_HUNYUAN_CONFIGURED=true` on Space
- G7 hosted attestation
