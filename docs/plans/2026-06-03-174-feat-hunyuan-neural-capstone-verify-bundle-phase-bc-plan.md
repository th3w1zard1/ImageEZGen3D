---
title: "feat: Hunyuan neural capstone verify bundle (Phase BC)"
type: feat
status: completed
date: 2026-06-03
origin: docs/brainstorms/2026-06-03-hunyuan-neural-capstone-verify-bundle-phase-bc-requirements.md
---

# feat: Hunyuan neural capstone verify bundle (Phase BC)

## Summary

One verify command for neural capstone JSON under `--record-dir`, chaining record schema checks and artifact parity.

## Implementation Units

### U1. Verify helper + CLI + tests

**Files:** `src/imageezgen3d/hunyuan_neural_enablement_preflight_bundle.py`, `scripts/verify_neural_enablement_preflight_bundle.py`, `tests/test_hunyuan_neural_enablement_preflight_bundle.py`

### U2. CI + docs

**Files:** `.github/workflows/ci.yml`, `docs/solutions/best-practices/hunyuan-pre-g7-stack-2026-05-28.md`, `docs/knowledgebase/hunyuan-g9-enablement-runbook.md`

**Dependencies:** U1
