---
title: "feat: Hunyuan neural enablement artifact parity (Phase AK)"
type: feat
status: active
date: 2026-05-29
origin: docs/brainstorms/2026-05-29-hunyuan-neural-enablement-artifact-parity-phase-ak-requirements.md
---

# feat: Hunyuan neural enablement artifact parity (Phase AK)

## Summary

Verify cross-artifact consistency between neural enablement and G9 workstation JSON records.

## Implementation Units

### U1. Artifact parity module

**Files:** `src/imageezgen3d/hunyuan_neural_enablement_artifact_parity.py`, `tests/test_hunyuan_neural_enablement_artifact_parity.py`

### U2. Wire into neural preflight bundle

**Files:** `src/imageezgen3d/hunyuan_neural_enablement_preflight_bundle.py`, `tests/test_hunyuan_neural_enablement_preflight_bundle.py`

**Dependencies:** U1

### U3. CLI, CI, docs

**Files:** `scripts/verify_neural_enablement_artifact_parity.py`, `.github/workflows/ci.yml`, stack docs

**Dependencies:** U1
