---
title: CI artifact parity verify script (Plan 072)
status: completed
created: 2026-05-27
---

# Plan 072 — Verify Hunyuan CI artifact parity in workflows

## Problem

Plan 071 added `tests/test_hunyuan_ci_scripts.py` for local subprocess parity, but scheduled `hosted-golden-smoke` still uploads `hunyuan-admission-audit.json` and `hunyuan-enablement-preflight.json` without a workflow step that fails when G7/G8 blocks diverge.

## Scope

- Merge PR #53 (Plan 071) first.
- Add `scripts/verify_hunyuan_ci_artifact_parity.py` (compare two JSON files; exit 1 on mismatch).
- Run after enablement preflight in `hosted-golden-smoke.yml` and in `ci.yml` `hunyuan-admission-audit` job.
- Unit tests + KB Plan 072 note.

## Out of scope

- Hunyuan enablement or Space deploy.

## Test scenarios

1. Script exits 0 when G7/G8 blocks match; 1 when `g8_enablement` differs.
2. Workflow files reference the verify script after both JSON records exist.
