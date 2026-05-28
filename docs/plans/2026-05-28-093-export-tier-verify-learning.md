---
title: Institutional learning for export-tier smoke record verify (Plan 093)
status: completed
created: 2026-05-28
---

# Plan 093 — Compound learning for export-tier smoke JSON verify

## Problem

Plan 091–092 landed `verify_hosted_export_tier_smoke_record.py` on `main`, but agents lack a `docs/solutions/` entry and `AGENTS.md` does not mention the export-tier verify CLI alongside the golden smoke verifier.

## Scope

- Add `docs/solutions/best-practices/hosted-export-tier-smoke-record-verify-2026-05-28.md` + README index row.
- Cross-link golden smoke record verify solution.
- Extend `AGENTS.md` and `hunyuan-g9-enablement-runbook.md` with export-tier verify step.
- Subprocess test in `tests/test_hosted_export_tier_smoke.py` for verify CLI exit 0/1.
- Refresh ideation doc with Plans 078–092 smoke guard stack on `main`.
- KB Plan 093 note.

## Out of scope

- Hunyuan enablement or Space deploy.

## Test scenarios

1. Subprocess: valid two-check record exits 0; missing `g7_false_neural_guard_ok` exits 1.
2. Solutions doc links Plan 091 and golden smoke record verify learning.

## Files

- `docs/plans/2026-05-28-093-export-tier-verify-learning.md`
- `docs/solutions/best-practices/hosted-export-tier-smoke-record-verify-2026-05-28.md`
- `docs/solutions/best-practices/hosted-golden-smoke-record-verify-2026-05-28.md`
- `docs/solutions/README.md`
- `AGENTS.md`
- `docs/knowledgebase/hunyuan-g9-enablement-runbook.md`
- `docs/ideation/2026-05-24-post-trust-slice-refresh.md`
- `tests/test_hosted_export_tier_smoke.py`
- `docs/knowledgebase/40-operational-risk/hosted-validation-2026-05-23.md`
