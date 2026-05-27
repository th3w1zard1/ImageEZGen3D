---
title: Hunyuan CI artifact parity institutional learning (Plan 073)
status: active
created: 2026-05-27
---

# Plan 073 — Compound learning for Hunyuan CI artifact parity

## Problem

Plans 068–072 built admission/enablement JSON parity, verify scripts, and workflow gates, but the lesson is not captured in `docs/solutions/` for future agents. `test_hunyuan_ci_scripts.py` does not yet invoke the verify CLI.

## Scope

- Merge PR #54 (Plan 072) first.
- Add `docs/solutions/best-practices/hunyuan-ci-artifact-parity-2026-05-27.md` + README index row.
- Update `AGENTS.md` and G9 runbook with verify step.
- Extend `test_hunyuan_ci_scripts.py` to run `verify_hunyuan_ci_artifact_parity.py` on recorded files.

## Out of scope

- Hunyuan enablement or Space deploy.

## Test scenarios

1. Subprocess test runs verify script after both JSON records; exit 0.
2. Solutions doc links to KB runbooks and verify script.
