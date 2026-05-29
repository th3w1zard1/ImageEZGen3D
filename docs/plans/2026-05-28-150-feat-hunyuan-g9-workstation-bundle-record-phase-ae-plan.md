---
title: "feat: Hunyuan G9 workstation bundle record (Phase AE, pre-G7)"
type: feat
status: completed
date: 2026-05-28
origin: docs/plans/2026-05-28-149-feat-hunyuan-g9-workstation-bundle-phase-ad-plan.md
---

# feat: Hunyuan G9 workstation bundle record (Phase AE, pre-G7)

## Summary

Add G9 workstation bundle attestation record schema, verify scripts, fixtures, and CI guard for tier-C G9 evidence.

## Requirements

- R1. `G9WorkstationBundleAttestation` with `record_kind=hunyuan_g9_workstation_bundle`.
- R2. `run_g9_workstation_bundle()` writes `g9-workstation-bundle.json`.
- R3. `verify_g9_workstation_bundle_record.py` and fixture verify in CI.
- R4. G9 bundle smoke step in `hunyuan-admission-audit` job.
- R5. Unit tests for skipped/ready fixtures.

## Out of scope

- `IMAGEEZ_HUNYUAN_CONFIGURED=true` on Space
- G7 hosted Block/Vase attestation
