---
title: CI workflows use Hunyuan preflight bundle (Plan 075)
status: active
created: 2026-05-27
---

# Plan 075 — Use preflight bundle in CI and scheduled smoke

## Problem

Plan 074 added `hunyuan_preflight_bundle.py` for local/agent use, but `ci.yml` and `hosted-golden-smoke.yml` still run three separate Hunyuan JSON/verify steps. That duplicates the contract the bundle was meant to unify.

## Scope

- Merge PR #56 (Plan 074) first.
- Add optional `--json` to the bundle (audit + enablement subcommands).
- Replace separate audit / enablement / verify steps with one bundle step in both workflows (keep G7 preflight and G1/G5 in CI as today).
- Update workflow contract tests and KB Plan 075 note.

## Out of scope

- Hunyuan enablement or Space deploy.

## Test scenarios

1. Bundle `--json` writes valid JSON files; verify still passes.
2. `test_workflows` asserts `hunyuan_preflight_bundle.py` in `ci.yml` and `hosted-golden-smoke.yml`.
