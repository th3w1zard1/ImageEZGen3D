---
title: "feat: Ship PR #22 trimesh quadric decimation to main"
type: feat
status: completed
date: 2026-05-24
origin: docs/plans/2026-05-24-039-feat-trimesh-quadric-decimation-plan.md
---

# feat: Ship PR #22 trimesh quadric decimation to main

## Summary

Merge PR #22 (quadric decimation + mesh deps), redeploy Space, extend hosted export-tier validation to assert `decimation_method: quadric` on balanced runs, and record KB evidence.

## Requirements

- R1. Squash-merge PR #22 when CI green
- R2. `hf_space_sync --execute` post-merge (trimesh in `requirements.txt`)
- R3. `hosted_golden_smoke.py` and `hosted_export_tier_smoke.py` exit 0
- R4. `validate_run_manifest` accepts optional `sidecar_path`; when `expect_raw`, assert sidecar `decimation.decimation_method == quadric`
- R5. `run_hosted_golden_smoke` passes export sidecar path from `/generate` output when validating balanced manifest
- R6. Unit tests for sidecar quadric assertion
- R7. Update `hosted-validation-2026-05-23.md` and ideation completed section
- R8. Mark Plan 040 `status: completed`

## Scope Boundaries

- Hunyuan enablement — deferred

## Files

- Modify: `src/imageezgen3d/hosted_golden_smoke.py`
- Modify: `scripts/hosted_export_tier_smoke.py` (if needed for sidecar wiring)
- Modify: `tests/test_hosted_export_tier_smoke.py`
- Modify: `docs/knowledgebase/40-operational-risk/hosted-validation-2026-05-23.md`
- Modify: `docs/ideation/2026-05-24-post-trust-slice-refresh.md`
