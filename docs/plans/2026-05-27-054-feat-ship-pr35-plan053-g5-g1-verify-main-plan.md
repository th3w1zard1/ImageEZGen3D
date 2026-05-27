---
title: "feat: Ship PR #35 Plan 053 G5 + G1 verify to main"
type: feat
status: active
date: 2026-05-27
origin: docs/plans/2026-05-24-053-feat-hunyuan-g5-resource-fit-plan.md
---

# feat: Ship PR #35 Plan 053 G5 + G1 verify to main

## Summary

Fix CI lint on PR #35, squash-merge to `main`, verify admission audit + hosted golden smoke, record Plan 054 KB evidence.

## Requirements

- R1. CI lint green on PR #35 branch
- R2. Squash-merge PR #35
- R3. `unittest discover` + `hunyuan_admission_audit.py` pass on `main`
- R4. Hosted golden smoke exit 0
- R5. Plan 054 section in `hosted-validation-2026-05-23.md`; ideation note; plan `completed`

## Scope Boundaries

- Hunyuan enablement (`configured=True`) — deferred (G7)
- Space redeploy — not required unless merge changes runtime

## Files

- Fix lint in: `scripts/hunyuan_g1_legal_verify.py`, `scripts/hunyuan_resource_estimate.py` (if needed)
- Modify: `docs/knowledgebase/40-operational-risk/hosted-validation-2026-05-23.md`
- Modify: `docs/ideation/2026-05-24-next-runtime-slice.md`
- Modify: this plan file

## Test scenarios

- `ruff check` (or project lint command)
- `PYTHONPATH=src python -m unittest discover -s tests`
- `PYTHONPATH=src python scripts/hunyuan_admission_audit.py`
- `PYTHONPATH=src python scripts/hosted_golden_smoke.py`
