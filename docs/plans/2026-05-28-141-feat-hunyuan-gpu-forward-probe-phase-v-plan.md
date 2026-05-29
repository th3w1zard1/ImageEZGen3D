---
title: "feat: Hunyuan GPU forward workstation probe (Phase V, pre-G7)"
type: feat
status: completed
date: 2026-05-28
origin: docs/plans/2026-05-28-140-feat-hunyuan-tencent-gpu-forward-phase-u-plan.md
---

# feat: Hunyuan GPU forward workstation probe (Phase V, pre-G7)

## Summary

Add an operator CLI that merges tier-C readiness, Tencent pipeline probes, and GPU forward gates into one workstation smoke report — informational exit 0, no neural execution.

## Requirements

- R1. `evaluate_gpu_forward_workstation_readiness()` aggregates tier-C, pipeline, and GPU gates.
- R2. `scripts/hunyuan_gpu_forward_probe.py` (informational exit 0).
- R3. Report lists explicit blockers when workstation is not ready for GPU forward.
- R4. Preflight bundle unchanged and still exit 0 with `configured=False`.
- R5. Unit tests cover blocker aggregation without tier-C install.

## Out of scope

- Running GPU forward on CI or Space
- `IMAGEEZ_HUNYUAN_CONFIGURED=true`
- G7 hosted attestation
