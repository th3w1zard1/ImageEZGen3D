---
title: "feat: Ship PR #16 export sidecar to main"
type: feat
status: active
date: 2026-05-24
origin: docs/plans/2026-05-24-029-feat-quality-tier-export-sidecar-plan.md
---

# feat: Ship PR #16 export sidecar to main

## Summary

Merge PR #16 (quality-tier decimation presets + export sidecar), extend golden-sample attestation to require `export_sidecar`, redeploy Space, and record post-merge hosted Block E2E with export budget visible.

## Requirements

- R1. Extend `golden_sample` attestation: require `export_sidecar` artifact and `decimation_target` in parameters (draft → 25_000)
- R2. Full test suite + golden attestation pass on PR branch
- R3. Squash-merge PR #16 to `main`
- R4. Post-merge `golden_sample_attestation.py` and `hf_space_sync --execute` on `main`
- R5. Hosted Block `/generate` — run id, export budget in status, manifest/GLB/OBJ/export sidecar downloadable
- R6. Update `hosted-validation-2026-05-23.md` and ideation (mesh tiers partial → sidecar landed; next = hosted golden CI optional)
- R7. Mark Plans 029–030 `status: completed`

## Scope Boundaries

- Real mesh decimation algorithm — deferred
- Hosted golden scheduled workflow — next optional slice

## Files

- Modify: `src/imageezgen3d/golden_sample.py`
- Modify: `tests/test_golden_sample.py` (if present) or add coverage in existing tests
- Modify: `docs/knowledgebase/40-operational-risk/hosted-validation-2026-05-23.md`
- Modify: `docs/ideation/2026-05-24-post-trust-slice-refresh.md`
- Modify: `docs/plans/2026-05-24-029-feat-quality-tier-export-sidecar-plan.md`
