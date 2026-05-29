---
title: "feat: Hunyuan inference runner protocol shell (Phase O, pre-G7)"
type: feat
status: completed
date: 2026-05-28
origin: docs/plans/2026-05-28-133-feat-hunyuan-tier-c-readiness-phase-n-plan.md
---

# feat: Hunyuan inference runner protocol shell (Phase O, pre-G7)

## Summary

Introduce a pluggable `HunyuanInferenceRunner` protocol and operator probe so tier-C readiness can report `inference_wired` from a single resolver — without enabling the adapter or claiming G7 PASS.

## Requirements

- R1. `HunyuanInferenceRunner` protocol accepts weight paths and returns `HunyuanMeshResult`.
- R2. `resolve_hunyuan_inference_runner()` returns `None` by default (unwired).
- R3. `prepare_tier_c_runtime()` derives `inference_wired` from the resolver.
- R4. `WeightVerifiedHunyuanBackend` delegates to runner when wired; otherwise honest `NotImplementedError`.
- R5. Admission preflight bundle remains exit 0 with `configured=False`.

## Out of scope

- Tencent tier-C neural implementation
- `IMAGEEZ_HUNYUAN_CONFIGURED=true` on Space
- G7 hosted attestation
