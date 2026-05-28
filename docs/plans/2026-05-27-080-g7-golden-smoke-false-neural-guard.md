---
title: G7 false-neural guard in hosted golden smoke (Plan 080)
status: completed
created: 2026-05-28
---

# Plan 080 — Fail golden smoke if status falsely passes G7 neural validators

## Problem

`hosted_golden_smoke` validates G8 CPU fallback honesty via `validate_g8_cpu_fallback_status` but does not guard against a status markdown that would satisfy `validate_g7_hosted_generate_status` while the adapter remains disabled. A misconfigured Space could report a false G7-shaped neural success.

## Scope

- In `run_hosted_golden_smoke`, after G8 validation, fail when `validate_g7_hosted_generate_status` returns success (unexpected while adapter disabled).
- Add unit tests with fixture status strings (cpu-demo ok; fake neural markers fail).
- KB Plan 080 note in hosted-validation.

## Out of scope

- Enabling Hunyuan adapter or closing G7 gate.
- Changing scheduled workflow adapter selection.

## Test scenarios

1. Status with cpu-demo only: smoke ok (G7 validator fails as expected).
2. Status that passes G7 neural validator: smoke fails with explicit issue.
3. `tests/test_hosted_golden_smoke.py` (or g7 tests) cover both.
