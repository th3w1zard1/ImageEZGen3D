---
title: Fail golden smoke when status falsely passes G7 neural validators
date: 2026-05-28
category: best-practices
module: hosted-golden-smoke
problem_type: best_practice
component: ci
severity: high
applies_when:
  - "Changing hosted_golden_smoke validation"
  - "Changing validate_g7_hosted_generate_status criteria"
  - "Debugging golden-sample or scheduled hosted-golden-smoke failures"
tags: [hunyuan, g7, hosted-golden-smoke, admission-gates, fallback-honesty]
---

# Fail golden smoke when status falsely passes G7 neural validators

## Context

While `HunyuanPlaceholderAdapter` remains disabled, hosted generation should use **cpu-demo / Local CPU Preview**. G8 honesty is enforced via `validate_g8_cpu_fallback_status`. Without a G7 guard, a misconfigured Space could return status markdown that satisfies `validate_g7_hosted_generate_status` (hunyuan-zerogpu markers, no fallback labels) and look like G7 closed when it is not.

## Guidance

| Check | Function | Expected while adapter disabled |
| --- | --- | --- |
| CPU fallback honesty | `validate_g8_cpu_fallback_status` | Status shows cpu-demo or Local CPU Preview |
| No false G7 neural claim | `validate_g7_not_false_neural_claim` | `validate_g7_hosted_generate_status` must **fail** |

`run_hosted_golden_smoke` calls both. The G7 helper **lazy-imports** `validate_g7_hosted_generate_status` to avoid a circular import with `hunyuan_g7_preflight` (which imports smoke constants).

Scheduled smoke JSON (`hosted-golden-smoke.json`) includes **`g7_false_neural_guard_ok`** so artifact review does not require parsing `issues` strings.

## When changing validators

- If you tighten G7 neural criteria, ensure golden smoke fixtures in `tests/test_hosted_golden_smoke.py` still use cpu-demo-shaped status for the happy path.
- If you add a real Hunyuan path to golden smoke (post-enablement), gate the G7 guard behind adapter configuration — do not fail legitimate neural runs.

## Related

- [hunyuan-g7-preflight.md](../../knowledgebase/hunyuan-g7-preflight.md)
- [hunyuan-ci-artifact-parity-2026-05-27.md](hunyuan-ci-artifact-parity-2026-05-27.md)
- Plan 080 — `docs/plans/2026-05-27-080-g7-golden-smoke-false-neural-guard.md`
