---
title: "feat: Hunyuan enablement evidence capstones verify bundle (Phase BD)"
type: feat
status: completed
date: 2026-06-03
origin: docs/brainstorms/2026-06-03-hunyuan-enablement-evidence-capstones-verify-bundle-phase-bd-requirements.md
---

# feat: Hunyuan enablement evidence capstones verify bundle (Phase BD)

## Summary

One verify command for all enablement evidence capstones under `--record-dir`, chaining Phases BA–BC verify helpers after the admission capstone run.

## Implementation Units

### U1. Verify helper + CLI + tests

**Files:** `src/imageezgen3d/hunyuan_enablement_evidence_capstones.py`, `scripts/verify_enablement_evidence_capstones.py`, `tests/test_hunyuan_enablement_evidence_capstones.py`

**Test scenarios:**
- Empty record dir returns prefixed issues from all three capstone verifies.
- After `run_admission_g9_enablement_evidence_bundle(..., skip_weight_warm=True)`, umbrella verify returns no issues.
- CLI subprocess exits 0 on CI-like admission capstone record dir.

### U2. CI + docs

**Files:** `.github/workflows/ci.yml`, `docs/solutions/best-practices/hunyuan-pre-g7-stack-2026-05-28.md`, `docs/knowledgebase/hunyuan-g9-enablement-runbook.md`

**Dependencies:** U1
