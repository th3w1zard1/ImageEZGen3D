---
title: "feat: Hunyuan enablement-neural artifact parity (Phase AL)"
type: feat
status: completed
date: 2026-05-29
origin: docs/brainstorms/2026-05-29-hunyuan-enablement-neural-artifact-parity-phase-al-requirements.md
---

# feat: Hunyuan enablement-neural artifact parity (Phase AL)

## Summary

Verify `g7_readiness` alignment between enablement preflight and neural enablement JSON records.

## Implementation Units

### U1. Enablement-neural parity module

**Files:** extend `src/imageezgen3d/hunyuan_neural_enablement_artifact_parity.py`, `tests/test_hunyuan_neural_enablement_artifact_parity.py`

### U2. Wire into bundle + docs

**Files:** `src/imageezgen3d/hunyuan_neural_enablement_preflight_bundle.py`, stack docs, G9 runbook

**Dependencies:** U1
