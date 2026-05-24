---
title: "feat: Ship PR #15 compare export to main"
type: feat
status: active
date: 2026-05-24
origin: docs/plans/2026-05-24-027-feat-history-compare-manifest-export-plan.md
---

# feat: Ship PR #15 compare export to main

## Summary

Merge PR #15 (manifest compare JSON/MD export), redeploy Space, run post-merge hosted smoke with JSON validation, and close out Phase 3 compare in ideation/KB.

## Requirements

- R1. Squash-merge PR #15 (CI already green)
- R2. Post-merge `hosted_history_compare_smoke.py` exit 0 including JSON export checks
- R3. Hub deploy from `main`
- R4. Update `hosted-validation-2026-05-23.md` Plan 027/028 evidence
- R5. Update `docs/ideation/2026-05-24-post-trust-slice-refresh.md` — mark Phase 3 compare complete; next = mesh cleanup tiers
- R6. Mark Plan 027 `status: completed`

## Scope Boundaries

- Quality-tier decimation implementation — next slice
- Hosted golden CI workflow — deferred

## Files

- Modify: `docs/knowledgebase/40-operational-risk/hosted-validation-2026-05-23.md`
- Modify: `docs/ideation/2026-05-24-post-trust-slice-refresh.md`
- Modify: `docs/plans/2026-05-24-027-feat-history-compare-manifest-export-plan.md`
