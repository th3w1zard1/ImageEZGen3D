---
title: Verify hosted-export-tier-smoke.json artifact schema in CI
date: 2026-05-28
category: best-practices
module: hosted-golden-smoke
problem_type: best_practice
component: ci
severity: medium
applies_when:
  - "Changing hosted_export_tier_smoke.py record shape"
  - "Changing draft/balanced tier smoke checks"
  - "Debugging scheduled export-tier artifact uploads"
tags: [hosted-golden-smoke, export-tiers, ci, g7, fallback-honesty]
---

# Verify hosted-export-tier-smoke.json artifact schema in CI

## Context

`hosted_export_tier_smoke.py` runs draft and balanced `/generate` passes and writes `hosted-export-tier-smoke.json` as `{"checks": [<golden-smoke dict>, ...]}`. Each check must satisfy the same schema as [hosted-golden-smoke-record-verify-2026-05-28.md](hosted-golden-smoke-record-verify-2026-05-28.md), including **`g7_false_neural_guard_ok`**.

## Guidance

| Step | Command / location |
| --- | --- |
| Run tier smoke + record | `PYTHONPATH=src python scripts/hosted_export_tier_smoke.py --record hosted-export-tier-smoke.json` |
| Verify artifact | `PYTHONPATH=src python scripts/verify_hosted_export_tier_smoke_record.py hosted-export-tier-smoke.json` |
| Workflow | `.github/workflows/hosted-golden-smoke.yml` after export tier `--record` |

`validate_hosted_export_tier_smoke_record()` requires exactly two checks with qualities **draft** and **balanced**. Per-check issues are prefixed `checks[n]:`.

## When changing tier smoke

- If you add a third quality tier to smoke, update `_EXPORT_TIER_QUALITIES`, `_TIER_CHECKS`, and validation tests together.
- Keep [g7-false-neural-golden-smoke-guard-2026-05-28.md](g7-false-neural-golden-smoke-guard-2026-05-28.md) in mind for status markdown while the adapter is disabled.

## Related

- [hosted-golden-smoke-record-verify-2026-05-28.md](hosted-golden-smoke-record-verify-2026-05-28.md)
- Plan 091 — `docs/plans/2026-05-28-091-verify-export-tier-smoke-record.md`
