---
title: "feat: Hunyuan admission + G9 enablement evidence bundle record (Phase AV)"
type: feat
status: active
date: 2026-06-03
origin: docs/brainstorms/2026-06-03-hunyuan-admission-g9-enablement-evidence-bundle-record-phase-av-requirements.md
---

# feat: Hunyuan admission + G9 enablement evidence bundle record (Phase AV)

## Summary

Persist `admission-g9-enablement-evidence-bundle.json` from the Phase AU operator bundle, with verify scripts, fixtures, and CI guardrails.

## Requirements

| ID | Requirement |
| --- | --- |
| R1 | Attestation schema + write/verify for bundle record |
| R2 | AU bundle writes and re-verifies record after run |
| R3 | Nested `g9-enablement-evidence.json` schema delegation |
| R4 | CI smoke + fixture verify |
| R5 | Adapter stays disabled |

## Implementation Units

### U1. Record module + bundle wiring

**Goal:** Attestation record, verify, and AU bundle integration.

**Files:** `src/imageezgen3d/hunyuan_admission_g9_enablement_evidence_bundle_record.py`, `src/imageezgen3d/hunyuan_admission_g9_enablement_evidence_bundle.py`, `scripts/verify_admission_g9_enablement_evidence_bundle_record.py`, `scripts/verify_admission_g9_enablement_evidence_bundle_record_fixtures.py`, `tests/fixtures/admission-g9-enablement-evidence-bundle-skipped.json`, `tests/test_hunyuan_admission_g9_enablement_evidence_bundle_record.py`, `tests/test_hunyuan_admission_g9_enablement_evidence_bundle.py`

**Test scenarios:**
- Skipped fixture verifies
- AU bundle writes valid skipped record on CI-like path
- `ok=true` rejected when admission or nested evidence gates fail

### U2. CI + docs

**Goal:** Wire CI smoke/fixture verify; update stack index and runbook.

**Files:** `.github/workflows/ci.yml`, `docs/solutions/best-practices/hunyuan-pre-g7-stack-2026-05-28.md`, `docs/knowledgebase/hunyuan-g9-enablement-runbook.md`

**Dependencies:** U1
