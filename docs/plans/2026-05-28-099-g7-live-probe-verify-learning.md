---
title: Institutional learning for G7 live probe record verify (Plan 099)
status: completed
created: 2026-05-28
---

# Plan 099 — Compound learning for G7 live-probe JSON verify

## Problem

Plans 097–098 landed `verify_hunyuan_g7_live_probe_record.py` on `main`, but agents lack a subprocess contract test and the G9 enablement runbook does not list the G7 live-probe verify step alongside golden/export-tier verifiers.

## Scope

- Subprocess test in `tests/test_hunyuan_g7_preflight.py` for `verify_hunyuan_g7_live_probe_record.py` exit 0/1.
- Extend `docs/knowledgebase/hunyuan-g9-enablement-runbook.md` with G7 live-probe verify + `verify_hosted_smoke_artifacts.py`.
- Cross-link [hunyuan-g7-live-probe-scheduled-smoke-2026-05-28.md](../solutions/best-practices/hunyuan-g7-live-probe-scheduled-smoke-2026-05-28.md) to smoke bundle verify learning.
- Refresh ideation with PR #65 / Plans 097–098 on `main`.
- KB Plan 099 note in `hosted-validation-2026-05-23.md`.

## Out of scope

- Hunyuan enablement or Space deploy.
- Changing validation logic in `hunyuan_g7_preflight.py`.

## Test scenarios

1. Subprocess: valid live-probe record exits 0; payload missing `hosted_probe` exits 1.
2. Enablement runbook lists all three smoke verify CLIs.

## Files

- `docs/plans/2026-05-28-099-g7-live-probe-verify-learning.md`
- `tests/test_hunyuan_g7_preflight.py`
- `docs/knowledgebase/hunyuan-g9-enablement-runbook.md`
- `docs/solutions/best-practices/hunyuan-g7-live-probe-scheduled-smoke-2026-05-28.md`
- `docs/ideation/2026-05-24-post-trust-slice-refresh.md`
- `docs/knowledgebase/40-operational-risk/hosted-validation-2026-05-23.md`
