---
title: CI bundle workflow contract test (Plan 079)
status: completed
created: 2026-05-27
---

# Plan 079 — Assert CI vs smoke bundle flags in workflow tests

## Problem

`test_workflows` checks hosted-golden-smoke uses `hunyuan_preflight_bundle.py --json` but does not assert `ci.yml` uses the bundle **without** `--json` (matching the actual workflow split).

## Scope

- Extend `tests/test_workflows.py` with contract tests for `ci.yml` bundle step (no `--json`) vs smoke (`--json`).
- Add Plan 079 note to hosted-validation after merge/stack.
- Update solutions README index blurb for hunyuan parity doc (bundle-first).

## Out of scope

- Hunyuan enablement, G7 neural E2E, Space deploy.

## Test scenarios

1. `test_workflows` passes: smoke has `--json`, ci hunyuan job does not pass `--json` to bundle.
2. `python -m unittest tests.test_workflows` green.
