---
title: "feat: Ship PR #20 Gradio export tier downloads to main"
type: feat
status: completed
date: 2026-05-24
origin: docs/plans/2026-05-24-037-feat-gradio-export-tier-downloads-plan.md
---

# feat: Ship PR #20 Gradio export tier downloads to main

## Summary

Merge PR #20 (export sidecar + RAW GLB Gradio downloads), redeploy Hugging Face Space, run post-merge hosted smokes, and record KB evidence.

## Requirements

- R1. Squash-merge PR #20 when CI is green
- R2. Sync `main`, redeploy Space via `scripts/hf_space_sync.py --execute`
- R3. Live Space: app loads; Block sample generation completes with run id
- R4. Post-merge `scripts/hosted_golden_smoke.py` and `scripts/hosted_export_tier_smoke.py` exit 0
- R5. Update `docs/knowledgebase/40-operational-risk/hosted-validation-2026-05-23.md` with PR #20 / UI download evidence
- R6. Update ideation doc completed section for Plan 037
- R7. Mark Plan 038 `status: completed`

## Scope Boundaries

- Hunyuan enablement — deferred
- New feature code beyond shipping PR #20 — deferred

## Files

- Modify: `docs/knowledgebase/40-operational-risk/hosted-validation-2026-05-23.md`
- Modify: `docs/ideation/2026-05-24-post-trust-slice-refresh.md`
- Modify: `docs/plans/2026-05-24-038-feat-ship-pr20-gradio-export-downloads-main-plan.md` (status)

## Test scenarios

- TS1: `gh pr checks 20` all success before merge
- TS2: Hosted golden smoke passes on live Space URL after deploy
- TS3: Export tier smoke passes (draft + balanced manifest contracts)
