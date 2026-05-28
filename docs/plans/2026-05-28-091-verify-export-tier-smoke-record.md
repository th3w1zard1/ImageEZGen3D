---
title: Verify hosted-export-tier-smoke.json artifact (Plan 091)
status: completed
created: 2026-05-28
---

# Plan 091 — CI guard for `hosted-export-tier-smoke.json`

## Problem

Scheduled smoke writes `hosted-export-tier-smoke.json` with a `checks` array of golden-smoke dicts, but there is no schema gate (unlike `hosted-golden-smoke.json` after Plan 087). Plans 066–069 remain `status: active` though KB validation already landed on `main`.

## Scope

- Add `validate_hosted_export_tier_smoke_record()` reusing per-check golden smoke validation.
- Add `scripts/verify_hosted_export_tier_smoke_record.py` and workflow step after export tier `--record`.
- Extend `tests/test_hosted_export_tier_smoke.py` and `tests/test_workflows.py`.
- Mark Plans 066–069 `status: completed`; refresh `hunyuan-admission-gates.md` last-audit line (through Plan 090).
- KB Plan 091 note.

## Out of scope

- Hunyuan enablement or G7 gate closure.
- Space deploy.

## Test scenarios

1. Valid two-entry `checks` payload passes; missing `g7_false_neural_guard_ok` in a check fails.
2. Workflow references verify script after `hosted-export-tier-smoke.json`.

## Files

- `src/imageezgen3d/hosted_golden_smoke.py`
- `scripts/verify_hosted_export_tier_smoke_record.py`
- `.github/workflows/hosted-golden-smoke.yml`
- `tests/test_hosted_export_tier_smoke.py`
- `tests/test_workflows.py`
- `docs/plans/2026-05-28-091-verify-export-tier-smoke-record.md`
- `docs/plans/2026-05-27-066-g8-gate-section-alignment.md` (status)
- `docs/plans/2026-05-27-067-g8-preflight-artifact-visibility.md` (status)
- `docs/plans/2026-05-27-068-enablement-json-parity-hosted-section.md` (status)
- `docs/plans/2026-05-27-069-hosted-doc-paths-artifact-parity.md` (status)
- `docs/knowledgebase/hunyuan-admission-gates.md`
- `docs/knowledgebase/40-operational-risk/hosted-validation-2026-05-23.md`
