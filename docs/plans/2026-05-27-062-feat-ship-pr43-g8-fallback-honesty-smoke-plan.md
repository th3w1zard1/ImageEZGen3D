---
title: "feat: Ship PR #43 + G8 fallback honesty in hosted golden smoke"
type: feat
status: completed
date: 2026-05-27
origin: docs/plans/2026-05-27-061-feat-ship-pr42-g7-preflight-ci-plan.md
---

# feat: Ship PR #43 + G8 fallback honesty in hosted golden smoke

## Summary

Squash-merge PR #43 (G7 preflight CI), then automate **G8 CPU fallback honesty** checks on every hosted golden smoke run (status must show fallback + preview disclaimer, not neural-only claims).

## Requirements

- R1. Squash-merge PR #43
- R2. `validate_g8_cpu_fallback_status()` + integrate into `run_hosted_golden_smoke`
- R3. `scripts/hunyuan_g8_preflight.py` for local/CI use (optional `--live` uses golden smoke path)
- R4. Unit tests; admission G8 evidence references G8 preflight module
- R5. KB `hunyuan-g8-preflight.md`; hosted-validation Plan 062 note
- R6. Live hosted golden smoke passes with G8 checks

## Scope boundaries

- Do not enable Hunyuan adapter
- G8 final closure after enablement uses `## G8 validation` + `G8_STATUS: PASS` (future)

## Files

- Add: `src/imageezgen3d/hunyuan_g8_preflight.py`
- Add: `scripts/hunyuan_g8_preflight.py`
- Add: `tests/test_hunyuan_g8_preflight.py`
- Add: `docs/knowledgebase/hunyuan-g8-preflight.md`
- Modify: `src/imageezgen3d/hosted_golden_smoke.py`
- Modify: `src/imageezgen3d/hunyuan_admission.py`
