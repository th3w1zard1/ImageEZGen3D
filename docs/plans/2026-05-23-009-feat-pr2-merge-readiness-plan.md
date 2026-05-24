---
title: "feat: PR #2 merge readiness and plan housekeeping"
type: feat
status: completed
date: 2026-05-24
origin: docs/ideation/2026-05-23-next-focus-ideation.md
---

# feat: PR #2 merge readiness and plan housekeeping

## Summary

Close housekeeping gaps after Plan 005: fix release-config test env isolation, mark completed plans 006–008, refresh stale ideation/parity rows (P8), add Space startup learning doc, and keep PR #2 CI green.

---

## Requirements

- R1. Fix `test_load_release_from_pyproject_sections` env pollution from prior tests / `.env`
- R2. Mark plans 006, 007, 008 `status: completed`
- R3. Update parity P8 and export-guide cross-links after brief audit
- R4. Add `docs/solutions/` learning for Space `demo` + port 7860 fix (`e2f0708`)
- R5. Refresh ideation doc stale blocker lines
- R6. Full unittest suite passes

---

## Scope Boundaries

- New product features — out of scope
- Hosted ZeroGPU enablement — out of scope

---

## Implementation Units

### U1. Test isolation fix

**Files:** `tests/test_release_config.py`

**Test scenarios:** Full suite passes; isolated test still passes

### U2. Plan status updates

**Files:** `docs/plans/2026-05-23-006-*.md`, `007-*.md`, `008-*.md`

### U3. KB / ideation refresh

**Files:** parity register P8, `export-guide.md`, ideation doc

### U4. Solutions learning

**Files:** `docs/solutions/tooling-decisions/hf-space-demo-port-binding-2026-05-24.md`, `docs/solutions/README.md`
