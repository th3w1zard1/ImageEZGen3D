---
title: G7 live probe learning and artifact verify (Plan 097)
status: completed
created: 2026-05-28
---

# Plan 097 — G7 live-probe learning + `hunyuan-g7-live-probe.json` verify

## Problem

Plan 095–096 landed scheduled G7 `--live-probe` and `verify_hosted_smoke_artifacts.py` on `main`, but there is no solutions doc for agents and no CI gate on `hunyuan-g7-live-probe.json` schema.

## Scope

- Add `docs/solutions/best-practices/hunyuan-g7-live-probe-scheduled-smoke-2026-05-28.md` + README row.
- Add `validate_hunyuan_g7_live_probe_record()` and `scripts/verify_hunyuan_g7_live_probe_record.py`.
- Workflow step after G7 live probe `--record`.
- Extend `tests/test_hunyuan_g7_preflight.py`, `tests/test_workflows.py`.
- Update `AGENTS.md`, G7 KB, ideation; KB Plan 097 note.

## Out of scope

- Hunyuan enablement or closing G7 gate.

## Test scenarios

1. Valid live-probe payload passes validation; missing `hosted_probe` fails.
2. Workflow references `verify_hunyuan_g7_live_probe_record.py`.
3. Solutions doc links G7 guard and smoke artifact verify learnings.

## Files

- `docs/plans/2026-05-28-097-g7-live-probe-learning-and-verify.md`
- `src/imageezgen3d/hunyuan_g7_preflight.py`
- `scripts/verify_hunyuan_g7_live_probe_record.py`
- `.github/workflows/hosted-golden-smoke.yml`
- `docs/solutions/best-practices/hunyuan-g7-live-probe-scheduled-smoke-2026-05-28.md`
- `docs/solutions/README.md`
- `AGENTS.md`
- `docs/ideation/2026-05-24-post-trust-slice-refresh.md`
- `docs/knowledgebase/hunyuan-g7-preflight.md`
- `tests/test_hunyuan_g7_preflight.py`
- `tests/test_workflows.py`
- `docs/knowledgebase/40-operational-risk/hosted-validation-2026-05-23.md`
