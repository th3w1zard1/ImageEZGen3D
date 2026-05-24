---
title: "feat: Ship PR #17 hosted golden smoke to main"
type: feat
status: completed
date: 2026-05-24
origin: docs/plans/2026-05-24-031-feat-hosted-golden-smoke-workflow-plan.md
---

# feat: Ship PR #17 hosted golden smoke to main

## Summary

Merge PR #17 (scheduled hosted golden smoke workflow), trigger first `workflow_dispatch` run on `main`, and record post-merge local + KB evidence.

## Requirements

- R1. Squash-merge PR #17 (CI green)
- R2. Post-merge `scripts/hosted_golden_smoke.py` exit 0 on `main`
- R3. Trigger `Hosted Golden Smoke` workflow via `gh workflow run`
- R4. Update `hosted-validation-2026-05-23.md` with merge SHA + smoke run id
- R5. Update ideation — hosted golden CI complete; mesh decimation next
- R6. Mark Plan 032 `status: completed`

## Scope Boundaries

- Real mesh decimation — next slice
- Hunyuan enablement — deferred

## Files

- Modify: `docs/knowledgebase/40-operational-risk/hosted-validation-2026-05-23.md`
- Modify: `docs/ideation/2026-05-24-post-trust-slice-refresh.md`
