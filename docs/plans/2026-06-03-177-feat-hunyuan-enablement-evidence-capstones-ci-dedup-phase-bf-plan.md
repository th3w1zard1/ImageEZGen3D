---
title: "feat: Hunyuan enablement evidence capstones CI dedup (Phase BF)"
type: feat
status: active
date: 2026-06-03
origin: docs/brainstorms/2026-06-03-hunyuan-enablement-evidence-capstones-ci-dedup-phase-bf-requirements.md
---

# feat: Hunyuan enablement evidence capstones CI dedup (Phase BF)

## Summary

Drop redundant CI artifact parity after Phase BE capstones preflight and align post-BE operator docs with the BE `--strict` path.

## Implementation Units

### U1. Test coverage + CI

**Files:** `tests/test_hunyuan_enablement_evidence_capstones.py`, `.github/workflows/ci.yml`

**Test scenarios:**
- After CI-like capstones preflight, `verify_neural_enablement_artifact_files` returns no issues when capstones verify passes.

### U2. Docs

**Files:** `docs/solutions/best-practices/hunyuan-pre-g7-stack-2026-05-28.md`, `docs/solutions/best-practices/g7-enablement-readiness-2026-05-28.md`

**Dependencies:** U1
