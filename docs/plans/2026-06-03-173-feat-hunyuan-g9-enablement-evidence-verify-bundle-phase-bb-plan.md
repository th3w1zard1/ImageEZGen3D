---
title: "feat: Hunyuan G9 enablement evidence verify bundle (Phase BB)"
type: feat
status: completed
date: 2026-06-03
origin: docs/brainstorms/2026-06-03-hunyuan-g9-enablement-evidence-verify-bundle-phase-bb-requirements.md
---

# feat: Hunyuan G9 enablement evidence verify bundle (Phase BB)

## Summary

One verify command for G9 evidence capstone JSON under `--record-dir`, chaining record schema checks and neural artifact parity.

## Implementation Units

### U1. Verify helper + CLI + tests

**Files:** `src/imageezgen3d/hunyuan_g9_enablement_evidence_bundle.py`, `scripts/verify_g9_enablement_evidence_bundle.py`, `tests/test_hunyuan_g9_enablement_evidence_bundle.py`

### U2. CI + docs

**Files:** `.github/workflows/ci.yml`, `docs/solutions/best-practices/hunyuan-pre-g7-stack-2026-05-28.md`, `docs/knowledgebase/hunyuan-g9-enablement-runbook.md`

**Dependencies:** U1
