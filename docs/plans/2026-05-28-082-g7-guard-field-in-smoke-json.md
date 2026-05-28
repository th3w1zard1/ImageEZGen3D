---
title: G7 guard field in golden smoke JSON (Plan 082)
status: completed
created: 2026-05-28
---

# Plan 082 — Expose `g7_false_neural_guard_ok` in smoke artifacts

## Problem

Plan 080–081 add the G7 false-neural guard but scheduled `hosted-golden-smoke.json` only lists generic `issues`. Operators cannot see guard pass/fail without parsing issue strings.

## Scope

- Add `g7_false_neural_guard_ok: bool` to `HostedGoldenSmokeResult` and `to_dict()`.
- Set in `run_hosted_golden_smoke` from `validate_g7_not_false_neural_claim` result.
- Include in `format_hosted_golden_report` output.
- Update unit tests and KB Plan 082 note.

## Out of scope

- Hunyuan enablement, merging open PRs.

## Test scenarios

1. Mocked cpu-demo run: `g7_false_neural_guard_ok=True`.
2. Mocked neural status run: `g7_false_neural_guard_ok=False` and `ok=False`.
3. `tests.test_hosted_golden_smoke` passes.
