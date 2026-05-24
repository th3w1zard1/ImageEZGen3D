---
title: "feat: Ship PR #18 mesh decimation and RAW export to main"
type: feat
status: active
date: 2026-05-24
origin: docs/plans/2026-05-24-033-feat-mesh-decimation-raw-export-plan.md
---

# feat: Ship PR #18 mesh decimation and RAW export to main

## Summary

Merge PR #18, redeploy Space, run post-merge hosted draft smoke plus balanced generate API check for RAW/decimation sidecar, and record KB evidence.

## Requirements

- R1. Squash-merge PR #18 (CI green)
- R2. Post-merge `golden_sample_attestation.py` and `hosted_golden_smoke.py` on `main`
- R3. Hub deploy `hf_space_sync --execute`
- R4. Hosted balanced `/generate` — confirm `raw_exported` / decimation in sidecar via API path
- R5. Update `hosted-validation-2026-05-23.md` and ideation
- R6. Mark Plan 034 `status: completed`

## Scope Boundaries

- Quadric decimation / trimesh — deferred
- Hunyuan — deferred

## Files

- Modify: `docs/knowledgebase/40-operational-risk/hosted-validation-2026-05-23.md`
- Modify: `docs/ideation/2026-05-24-post-trust-slice-refresh.md`
