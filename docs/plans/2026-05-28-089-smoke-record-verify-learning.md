---
title: Institutional learning for hosted golden smoke record verify (Plan 089)
status: completed
created: 2026-05-28
---

# Plan 089 — Compound learning for smoke JSON artifact verify

## Problem

Plan 087–088 landed `verify_hosted_golden_smoke_record.py` on `main`, but agents lack a `docs/solutions/` entry and `AGENTS.md` does not mention the verify CLI alongside the G7 guard learning.

## Scope

- Add `docs/solutions/best-practices/hosted-golden-smoke-record-verify-2026-05-28.md` + README index row.
- Extend `AGENTS.md` hosted/Hunyuan bullet with verify script reference.
- Subprocess test in `tests/test_hosted_golden_smoke.py` for `verify_hosted_golden_smoke_record.py` exit codes.
- KB Plan 089 note in `hosted-validation-2026-05-23.md`.

## Out of scope

- Hunyuan enablement or Space deploy.
- Changing smoke validation logic.

## Test scenarios

1. Subprocess: valid record exits 0; payload missing `g7_false_neural_guard_ok` exits 1.
2. Solutions doc links to Plan 087, G7 guard learning, and verify script.

## Files

- `docs/plans/2026-05-28-089-smoke-record-verify-learning.md`
- `docs/solutions/best-practices/hosted-golden-smoke-record-verify-2026-05-28.md`
- `docs/solutions/README.md`
- `AGENTS.md`
- `tests/test_hosted_golden_smoke.py`
- `docs/knowledgebase/40-operational-risk/hosted-validation-2026-05-23.md`
