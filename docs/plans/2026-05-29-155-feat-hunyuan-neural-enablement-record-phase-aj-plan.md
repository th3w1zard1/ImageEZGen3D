---
title: "feat: Hunyuan neural enablement attestation record (Phase AJ)"
type: feat
status: active
date: 2026-05-29
origin: docs/brainstorms/2026-05-29-hunyuan-neural-enablement-record-phase-aj-requirements.md
---

# feat: Hunyuan neural enablement attestation record (Phase AJ)

## Summary

Persist neural enablement preflight as a verifiable JSON record for tier-C operators and CI fixture gates.

## Implementation Units

### U1. Neural enablement record module

**Files:** `src/imageezgen3d/hunyuan_neural_enablement_record.py`, `tests/test_hunyuan_neural_enablement_record.py`

### U2. Wire record into preflight bundle

**Files:** `src/imageezgen3d/hunyuan_neural_enablement_preflight_bundle.py`, `tests/test_hunyuan_neural_enablement_preflight_bundle.py`

**Dependencies:** U1

### U3. CLI, fixtures, CI, docs

**Files:** `scripts/verify_neural_enablement_record.py`, `scripts/verify_neural_enablement_record_fixtures.py`, `tests/fixtures/neural-enablement-preflight-skipped.json`, `.github/workflows/ci.yml`, stack docs

**Dependencies:** U1
