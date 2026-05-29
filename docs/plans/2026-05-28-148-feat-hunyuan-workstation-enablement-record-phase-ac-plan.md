---
title: "feat: Hunyuan workstation enablement record (Phase AC, pre-G7)"
type: feat
status: completed
date: 2026-05-28
origin: docs/plans/2026-05-28-147-feat-hunyuan-workstation-enablement-preflight-phase-ab-plan.md
---

# feat: Hunyuan workstation enablement record (Phase AC, pre-G7)

## Summary

Add workstation enablement attestation record schema, `--record` on enablement preflight CLI, and verify scripts for tier-C G9 evidence.

## Requirements

- R1. `WorkstationEnablementAttestation` with `record_kind=hunyuan_workstation_enablement`.
- R2. `--record` on `hunyuan_workstation_enablement_preflight.py`.
- R3. `verify_workstation_enablement_record.py` and fixture verify in CI.
- R4. Preflight bundle unchanged; adapter stays disabled on Space.
- R5. Unit tests for skipped/ready fixtures.

## Out of scope

- `IMAGEEZ_HUNYUAN_CONFIGURED=true` on Space
- G7 hosted Block/Vase attestation
