---
title: G7 live probe in scheduled hosted smoke (Plan 095)
status: completed
created: 2026-05-28
---

# Plan 095 — Scheduled G7 live probe while adapter disabled

## Problem

`hunyuan_g7_preflight.py --live-probe` exists but scheduled `hosted-golden-smoke` only runs local G1–G6 readiness. There is no CI artifact proving the live Space rejects false G7 neural success when `hunyuan-zerogpu` is requested but disabled.

## Scope

- Add `--record` to `scripts/hunyuan_g7_preflight.py`.
- Run `--live-probe --json --record hunyuan-g7-live-probe.json` in `hosted-golden-smoke.yml` (uses `IMAGEEZ_HF_SPACE_URL`).
- Add `scripts/verify_hosted_smoke_artifacts.py` (both smoke record verifiers in one CLI).
- Extend `tests/test_workflows.py`, `tests/test_hunyuan_g7_preflight.py`, and smoke-artifacts subprocess test.
- Update `hunyuan-g7-preflight.md`, admission-gates last-audit, KB Plan 095 note.

## Out of scope

- Enabling Hunyuan adapter or closing G7 gate.
- Claiming ZeroGPU neural validation.

## Test scenarios

1. Mocked `probe_hosted_hunyuan_not_enabled` still covered; CLI `--record` writes JSON.
2. Workflow YAML includes `--live-probe` and artifact upload path.
3. `verify_hosted_smoke_artifacts.py` exits 0 on valid golden + export-tier fixtures.

## Files

- `docs/plans/2026-05-28-095-g7-live-probe-scheduled-smoke.md`
- `scripts/hunyuan_g7_preflight.py`
- `scripts/verify_hosted_smoke_artifacts.py`
- `.github/workflows/hosted-golden-smoke.yml`
- `tests/test_workflows.py`
- `tests/test_hunyuan_g7_preflight.py`
- `tests/test_hosted_smoke_artifacts.py` (new)
- `docs/knowledgebase/hunyuan-g7-preflight.md`
- `docs/knowledgebase/hunyuan-admission-gates.md`
- `docs/knowledgebase/40-operational-risk/hosted-validation-2026-05-23.md`
