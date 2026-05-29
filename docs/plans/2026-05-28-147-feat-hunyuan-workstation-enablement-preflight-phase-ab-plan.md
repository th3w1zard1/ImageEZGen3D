---
title: "feat: Hunyuan workstation enablement preflight (Phase AB, pre-G7)"
type: feat
status: completed
date: 2026-05-28
origin: docs/plans/2026-05-28-146-feat-hunyuan-workstation-evidence-preflight-phase-aa-plan.md
---

# feat: Hunyuan workstation enablement preflight (Phase AB, pre-G7)

## Summary

Unify workstation bundle and evidence preflight into one operator command for tier-C enablement readiness before G9.

## Requirements

- R1. `run_workstation_enablement_preflight()` chains bundle then evidence preflight.
- R2. `enablement_workstation_ready=true` only when bundle verify passes and evidence is ok.
- R3. `scripts/hunyuan_workstation_enablement_preflight.py` (`--strict` for not ready).
- R4. Preflight bundle unchanged; adapter stays disabled on Space.
- R5. Unit tests for CI-like skip path.

## Out of scope

- `IMAGEEZ_HUNYUAN_CONFIGURED=true` on Space
- G7 hosted Block/Vase attestation
