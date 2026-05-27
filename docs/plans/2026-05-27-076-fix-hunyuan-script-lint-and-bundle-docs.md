---
title: Fix Hunyuan script lint and align bundle docs (Plan 076)
status: active
created: 2026-05-27
---

# Plan 076 — Unblock Plan 075 PR (lint + bundle doc parity)

## Problem

PR #57 (Plan 075) CI **lint** fails: unused `sys` imports in `scripts/hunyuan_enablement_preflight.py`, `hunyuan_g7_preflight.py`, and `hunyuan_g8_preflight.py` (Ruff F401).

`docs/knowledgebase/hunyuan-enablement-preflight.md` still describes scheduled smoke as three separate steps; workflows now use `hunyuan_preflight_bundle.py`.

## Scope

- Remove unused `sys` imports from the three scripts (ruff clean on `scripts/`).
- Update `hunyuan-enablement-preflight.md` Scheduled CI section for bundle + `--json`.
- Add `test_bundle_json_flag` in `tests/test_hunyuan_preflight_bundle.py`.

## Out of scope

- Hunyuan enablement, Space deploy, workflow changes (done in Plan 075).

## Test scenarios

1. `ruff check app.py src scripts tests` passes.
2. `hunyuan_preflight_bundle.py --json --record-dir <tmp>` exits 0; JSON files valid.
3. Unit tests for bundle and workflows pass.
