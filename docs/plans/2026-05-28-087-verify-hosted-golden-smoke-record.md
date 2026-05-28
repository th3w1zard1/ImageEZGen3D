---
title: Verify hosted golden smoke JSON artifact (Plan 087)
status: completed
created: 2026-05-28
---

# Plan 087 — CI guard for `hosted-golden-smoke.json`

## Problem

Plan 086 merged the G7 guard stack and workflow `--json` contract, but scheduled smoke can still upload a malformed `hosted-golden-smoke.json` (missing `g7_false_neural_guard_ok` or wrong types) without failing the job.

Plans 070–073 remain `status: active` in frontmatter though KB validation sections already record them complete on `main`.

## Scope

- Add `validate_hosted_golden_smoke_record()` in `src/imageezgen3d/hosted_golden_smoke.py`.
- Add `scripts/verify_hosted_golden_smoke_record.py` (exit 1 on validation issues).
- Run verify step in `.github/workflows/hosted-golden-smoke.yml` after smoke `--record`.
- Extend `tests/test_workflows.py` and `tests/test_hosted_golden_smoke.py`.
- Mark Plans 070–073 `status: completed`.
- KB Plan 087 note in `hosted-validation-2026-05-23.md`.

## Out of scope

- Hunyuan enablement or Space deploy (no `app.py` change in PR #59).
- Closing G7/G8 admission gates.

## Test scenarios

1. Valid `HostedGoldenSmokeResult.to_dict()` payload passes validation.
2. Missing `g7_false_neural_guard_ok` fails with explicit issue.
3. Workflow YAML references `verify_hosted_golden_smoke_record.py` after `hosted-golden-smoke.json` is written.

## Files

- `src/imageezgen3d/hosted_golden_smoke.py`
- `scripts/verify_hosted_golden_smoke_record.py`
- `.github/workflows/hosted-golden-smoke.yml`
- `tests/test_hosted_golden_smoke.py`
- `tests/test_workflows.py`
- `docs/plans/2026-05-28-087-verify-hosted-golden-smoke-record.md`
- `docs/plans/2026-05-27-070-admission-audit-payload-builder.md` (status)
- `docs/plans/2026-05-27-071-g8-gates-helper-ci-scripts-test.md` (status)
- `docs/plans/2026-05-27-072-ci-artifact-verify-script.md` (status)
- `docs/plans/2026-05-27-073-hunyuan-ci-parity-learning.md` (status)
- `docs/knowledgebase/40-operational-risk/hosted-validation-2026-05-23.md`
