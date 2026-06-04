---
title: "feat: Hunyuan admission G9 enablement evidence verify bundle (Phase BA)"
type: feat
status: completed
date: 2026-06-03
origin: docs/brainstorms/2026-06-03-hunyuan-admission-g9-enablement-evidence-verify-bundle-phase-ba-requirements.md
---

# feat: Hunyuan admission G9 enablement evidence verify bundle (Phase BA)

## Summary

One verify command for admission capstone JSON under `--record-dir`, chaining record schema checks and bundle↔evidence parity.

## Implementation Units

### U1. Verify helper + CLI + tests

**Files:** `src/imageezgen3d/hunyuan_admission_g9_enablement_evidence_bundle.py`, `scripts/verify_admission_g9_enablement_evidence_bundle.py`, `tests/test_hunyuan_admission_g9_enablement_evidence_bundle.py`

### U2. CI + docs

**Files:** `.github/workflows/ci.yml`, `docs/solutions/best-practices/hunyuan-pre-g7-stack-2026-05-28.md`, `docs/knowledgebase/hunyuan-g9-enablement-runbook.md`

**Dependencies:** U1
