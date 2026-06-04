---
title: "feat: Hunyuan configured adapter inference path (Phase AH)"
type: feat
status: completed
date: 2026-05-29
origin: docs/brainstorms/2026-05-29-hunyuan-configured-inference-path-phase-ah-requirements.md
---

# feat: Hunyuan configured adapter inference path (Phase AH)

## Summary

Expose the configured-adapter inference seam (`generate` → `_run_hunyuan_inference_on_gpu` → `run_hunyuan_shape_texture`) via an operator probe and honest metadata when Tencent + GPU forward env is set.

## Implementation Units

### U1. Configured inference path module

**Files:** `src/imageezgen3d/hunyuan_configured_inference.py`, `tests/test_hunyuan_configured_inference.py`

**Test scenarios:** default CI-like `expected_outcome=adapter_disabled`; neural eligible when env flags + mocked workstation ready; probe script exit 0.

### U2. Metadata + adapter tests

**Files:** `src/imageezgen3d/hunyuan_backend.py`, `src/imageezgen3d/hunyuan_inference.py`, `tests/test_hunyuan_adapter.py`

**Dependencies:** U1

### U3. CLI, CI, docs

**Files:** `scripts/hunyuan_configured_inference_probe.py`, `.github/workflows/ci.yml`, stack + G7 readiness docs

**Dependencies:** U1
