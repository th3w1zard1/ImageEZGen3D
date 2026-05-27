---
title: Bundle-first admission docs and CI bundle test (Plan 077)
status: active
created: 2026-05-27
---

# Plan 077 — Bundle-first docs and subprocess CI parity test

## Problem

Plans 075–076 wired CI to `hunyuan_preflight_bundle.py` and fixed lint, but `hunyuan-admission-gates.md` still lists only the standalone audit CLI. `test_hunyuan_ci_scripts.py` exercises the legacy three-command path only, not the bundle path CI actually runs.

## Scope

- Update `docs/knowledgebase/hunyuan-admission-gates.md` — bundle-first audit commands; keep individual CLI as advanced.
- Add `test_bundle_record_matches_ci_artifact_parity` in `tests/test_hunyuan_ci_scripts.py`.
- Assert `hunyuan_preflight_bundle.py --json` in `tests/test_workflows.py` for hosted-golden-smoke.
- KB Plan 077 note in hosted-validation.

## Out of scope

- Hunyuan enablement, Space deploy, merging PR #57 (human/merge step).

## Test scenarios

1. `test_hunyuan_ci_scripts` bundle test exits 0 and JSON g7/g8 blocks match.
2. `test_workflows` sees `--json` on bundle step in hosted-golden-smoke.
3. Full unittest + ruff pass.
