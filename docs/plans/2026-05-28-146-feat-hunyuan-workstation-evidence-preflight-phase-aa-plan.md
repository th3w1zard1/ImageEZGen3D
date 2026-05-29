---
title: "feat: Hunyuan workstation evidence preflight (Phase AA, pre-G7)"
type: feat
status: completed
date: 2026-05-28
origin: docs/plans/2026-05-28-145-feat-hunyuan-gpu-forward-workstation-bundle-phase-z-plan.md
---

# feat: Hunyuan workstation evidence preflight (Phase AA, pre-G7)

## Summary

Add preflight for optional local `gpu-forward-e2e.json` workstation evidence before G9 enablement — does not claim G7 hosted PASS.

## Requirements

- R1. `evaluate_workstation_evidence_preflight()` reads optional record and reports `workstation_evidence_ok`.
- R2. `workstation_evidence_ok=true` requires `ok=true` and `with_exports=true` in a schema-valid record.
- R3. `scripts/hunyuan_workstation_evidence_preflight.py` (default exit 0; `--strict` for missing evidence when record present).
- R4. Preflight bundle unchanged; adapter stays disabled on Space.
- R5. Unit tests against skipped and succeeded-exports fixtures.

## Out of scope

- Setting `IMAGEEZ_HUNYUAN_CONFIGURED=true`
- G7 hosted Block/Vase attestation
- Requiring workstation evidence in default CI
