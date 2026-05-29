---
title: "feat: Hunyuan G9 workstation bundle (Phase AD, pre-G7)"
type: feat
status: completed
date: 2026-05-28
origin: docs/plans/2026-05-28-148-feat-hunyuan-workstation-enablement-record-phase-ac-plan.md
---

# feat: Hunyuan G9 workstation bundle (Phase AD, pre-G7)

## Summary

Add one-shot G9 operator bundle chaining admission preflight bundle with workstation enablement record verify.

## Requirements

- R1. `run_g9_workstation_bundle()` runs preflight bundle then workstation enablement attestation.
- R2. `g9_workstation_bundle_ok` when preflight bundle passes and record verify passes.
- R3. `scripts/hunyuan_g9_workstation_bundle.py` (`--strict` for evidence ready).
- R4. Does not enable adapter or claim G7 hosted PASS.
- R5. Unit tests for CI-like skip path.

## Out of scope

- `IMAGEEZ_HUNYUAN_CONFIGURED=true` on Space
- G7 hosted Block/Vase attestation
