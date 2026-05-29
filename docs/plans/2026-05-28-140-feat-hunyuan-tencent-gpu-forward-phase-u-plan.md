---
title: "feat: Tencent GPU forward executors (Phase U, pre-G7)"
type: feat
status: completed
date: 2026-05-28
origin: docs/plans/2026-05-28-139-feat-hunyuan-tencent-mesh-phase-t-plan.md
---

# feat: Tencent GPU forward executors (Phase U, pre-G7)

## Summary

Implement opt-in GPU shape/texture forward executors that call upstream `from_pretrained` / `__call__`, gated by `IMAGEEZ_HUNYUAN_GPU_FORWARD` — default CI/Space path remains unregistered until G9 enablement.

## Requirements

- R1. `gpu_shape_forward_executor` / `gpu_texture_forward_executor` with CUDA + pipeline class guards.
- R2. `IMAGEEZ_HUNYUAN_GPU_FORWARD` config seam; default `false`.
- R3. `resolve_tencent_forward_executors()` wires GPU executors only when env enabled.
- R4. Probe reports GPU forward readiness; preflight bundle exit 0 with `configured=False`.
- R5. Unit tests mock upstream pipelines; no tier-C install required in CI.

## Out of scope

- Enabling GPU forward by default on Space
- `IMAGEEZ_HUNYUAN_CONFIGURED=true`
- G7 hosted attestation
