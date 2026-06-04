---
title: "feat: Hunyuan enablement evidence capstones preflight (Phase BE)"
type: feat
status: completed
date: 2026-06-03
origin: docs/brainstorms/2026-06-03-hunyuan-enablement-evidence-capstones-preflight-phase-be-requirements.md
---

# feat: Hunyuan enablement evidence capstones preflight (Phase BE)

## Summary

One run+verify command for enablement evidence capstones under `--record-dir`, chaining the admission capstone run and Phase BD umbrella verify.

## Implementation Units

### U1. Run helper + CLI + tests

**Files:** `src/imageezgen3d/hunyuan_enablement_evidence_capstones.py`, `scripts/hunyuan_enablement_evidence_capstones.py`, `tests/test_hunyuan_enablement_evidence_capstones.py`

**Test scenarios:**
- CI-like skip path returns `enablement_evidence_capstones_ok=true` and empty verify issues.
- Umbrella verify failure surfaces prefixed verify issues in combined `issues`.
- CLI subprocess exits 0 after CI-like run; `--strict` exits 1 when evidence not ready.

### U2. CI + docs

**Files:** `.github/workflows/ci.yml`, `docs/solutions/best-practices/hunyuan-pre-g7-stack-2026-05-28.md`, `docs/knowledgebase/hunyuan-g9-enablement-runbook.md`

**Dependencies:** U1
