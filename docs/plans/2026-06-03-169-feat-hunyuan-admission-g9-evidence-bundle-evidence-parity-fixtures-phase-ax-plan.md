---
title: "feat: Hunyuan admission G9 bundle ↔ evidence parity fixtures + verify CLI (Phase AX)"
type: feat
status: active
date: 2026-06-03
origin: docs/brainstorms/2026-06-03-hunyuan-admission-g9-evidence-bundle-evidence-parity-fixtures-phase-ax-requirements.md
---

# feat: Hunyuan admission G9 bundle ↔ evidence parity fixtures + verify CLI (Phase AX)

## Summary

Dedicated bundle↔evidence parity verify CLI, aligned skipped fixtures, and CI fixture smoke after Phase AW parity logic.

## Implementation Units

### U1. Parity files helper + verify scripts

**Goal:** Operator CLI and record-dir loader.

**Files:** `src/imageezgen3d/hunyuan_neural_enablement_artifact_parity.py`, `scripts/verify_admission_g9_enablement_evidence_bundle_evidence_artifact_parity.py`, `scripts/verify_admission_g9_enablement_evidence_bundle_evidence_artifact_parity_fixtures.py`, `tests/test_hunyuan_neural_enablement_artifact_parity.py`

**Test scenarios:**
- Pass when both JSON present and aligned
- Fail when bundle missing
- Fixture verify script exits 0 on aligned fixtures

### U2. Align fixtures + CI + docs

**Goal:** Static fixture pair and CI smoke; update stack index and runbook.

**Files:** `tests/fixtures/admission-g9-enablement-evidence-bundle-skipped.json`, `.github/workflows/ci.yml`, `docs/solutions/best-practices/hunyuan-pre-g7-stack-2026-05-28.md`, `docs/knowledgebase/hunyuan-g9-enablement-runbook.md`

**Dependencies:** U1
