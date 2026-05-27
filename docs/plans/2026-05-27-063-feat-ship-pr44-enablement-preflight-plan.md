---
title: "feat: Ship PR #44 + unified Hunyuan enablement preflight"
type: feat
status: completed
date: 2026-05-27
origin: docs/plans/2026-05-27-062-feat-ship-pr43-g8-fallback-honesty-smoke-plan.md
---

# feat: Ship PR #44 + unified Hunyuan enablement preflight

## Summary

Squash-merge PR #44 (G8 in hosted golden smoke), then add a single **enablement preflight** CLI that reports G1–G9 status, G7 readiness, and blocking gates before any enablement PR.

## Requirements

- R1. Squash-merge PR #44
- R2. `src/imageezgen3d/hunyuan_enablement_preflight.py` + `scripts/hunyuan_enablement_preflight.py`
- R3. CI: run enablement preflight in `hunyuan-admission-audit` job
- R4. Unit tests; update admission gates last-audit line
- R5. KB note in hosted-validation Plan 063
- R6. `hunyuan_g7_preflight.py` + hosted golden smoke still pass

## Scope boundaries

- Do not set `configured=True`
- Do not claim G7/G8/G9 closed

## Files

- Add: `src/imageezgen3d/hunyuan_enablement_preflight.py`
- Add: `scripts/hunyuan_enablement_preflight.py`
- Add: `tests/test_hunyuan_enablement_preflight.py`
- Modify: `.github/workflows/ci.yml`, `docs/knowledgebase/hunyuan-admission-gates.md`
