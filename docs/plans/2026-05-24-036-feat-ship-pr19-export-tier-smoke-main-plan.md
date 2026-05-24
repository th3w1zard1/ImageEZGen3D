---
title: "feat: Ship PR #19 hosted export tier smoke to main"
type: feat
status: completed
date: 2026-05-24
origin: docs/plans/2026-05-24-035-feat-hosted-export-tier-smoke-plan.md
---

# feat: Ship PR #19 hosted export tier smoke to main

## Summary

Merge PR #19 (manifest-based export tier smoke), run post-merge hosted tier smoke on live Space, and record KB evidence.

## Requirements

- R1. Squash-merge PR #19 (CI green)
- R2. Post-merge `hosted_export_tier_smoke.py` exit 0 on `main`
- R3. Trigger `Hosted Golden Smoke` workflow on `main`
- R4. Update `hosted-validation-2026-05-23.md`
- R5. Mark Plan 036 `status: completed`

## Scope Boundaries

- Hunyuan enablement — deferred
- Space redeploy — only if smoke fails on stale build

## Files

- Modify: `docs/knowledgebase/40-operational-risk/hosted-validation-2026-05-23.md`
