---
title: Verify hosted-golden-smoke.json artifact schema in CI
date: 2026-05-28
category: best-practices
module: hosted-golden-smoke
problem_type: best_practice
component: ci
severity: medium
applies_when:
  - "Changing HostedGoldenSmokeResult.to_dict fields"
  - "Changing hosted-golden-smoke workflow artifacts"
  - "Debugging scheduled hosted-golden-smoke upload failures"
tags: [hosted-golden-smoke, ci, admission-gates, g7, fallback-honesty]
---

# Verify hosted-golden-smoke.json artifact schema in CI

## Context

Scheduled `hosted-golden-smoke` writes `hosted-golden-smoke.json` with `--json --record`. Plan 082 added **`g7_false_neural_guard_ok`** for artifact review. Without a schema gate, a regression could omit that field while the smoke job still uploads JSON.

## Guidance

| Step | Command / location |
| --- | --- |
| Run smoke + record | `PYTHONPATH=src python scripts/hosted_golden_smoke.py --json --record hosted-golden-smoke.json` |
| Verify artifact | `PYTHONPATH=src python scripts/verify_hosted_golden_smoke_record.py hosted-golden-smoke.json` |
| Workflow | `.github/workflows/hosted-golden-smoke.yml` runs verify immediately after record |

`validate_hosted_golden_smoke_record()` in `hosted_golden_smoke.py` checks required keys and types (including `g7_false_neural_guard_ok: bool`). Exit **1** prints `issue=...` lines on stderr.

## When changing smoke results

- Add new fields to `HostedGoldenSmokeResult.to_dict()` **and** `_REQUIRED_HOSTED_GOLDEN_SMOKE_KEYS` together.
- Update `tests/test_hosted_golden_smoke.py` validation tests and workflow contract test.
- Do not remove `g7_false_neural_guard_ok` while the Hunyuan adapter is disabled — pair with [g7-false-neural-golden-smoke-guard-2026-05-28.md](g7-false-neural-golden-smoke-guard-2026-05-28.md).

## Related

- [g7-false-neural-golden-smoke-guard-2026-05-28.md](g7-false-neural-golden-smoke-guard-2026-05-28.md)
- [hunyuan-ci-artifact-parity-2026-05-27.md](hunyuan-ci-artifact-parity-2026-05-27.md)
- Plan 087 — `docs/plans/2026-05-28-087-verify-hosted-golden-smoke-record.md`
