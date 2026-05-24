---
title: "feat: Hosted export tier smoke via manifest validation"
type: feat
status: completed
date: 2026-05-24
origin: docs/plans/2026-05-24-034-feat-ship-pr18-mesh-decimation-main-plan.md
---

# feat: Hosted export tier smoke via manifest validation

## Summary

Extend hosted smoke to validate export-sidecar and RAW tier contracts by parsing the manifest file returned from `/generate`, without enabling Hunyuan.

## Requirements

- R1. `validate_run_manifest(path, expect_raw)` — artifact keys + parameters (`raw_exported`, `decimation_applied`)
- R2. `run_hosted_export_tier_smoke(quality, expect_raw)` — generate + manifest validation
- R3. `scripts/hosted_export_tier_smoke.py` — draft + balanced passes
- R4. CI workflow step in `hosted-golden-smoke.yml`
- R5. Unit tests for manifest validator
- R6. 108+ tests; style + ruff clean

## Scope Boundaries

- Hunyuan enablement — deferred
- New Gradio download outputs for sidecar — deferred (manifest-only validation)

## Files

- Modify: `src/imageezgen3d/hosted_golden_smoke.py`
- Add: `scripts/hosted_export_tier_smoke.py`
- Add: `tests/test_hosted_export_tier_smoke.py`
- Modify: `.github/workflows/hosted-golden-smoke.yml`
