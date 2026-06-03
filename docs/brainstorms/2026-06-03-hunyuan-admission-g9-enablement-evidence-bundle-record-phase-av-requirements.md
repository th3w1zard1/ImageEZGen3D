# Hunyuan admission + G9 enablement evidence bundle record (Phase AV)

**Date:** 2026-06-03  
**Status:** Requirements for `/lfg` slice after Phase AU

## Problem

Phase AU orchestrates admission preflight and the G9 evidence capstone but does not persist a top-level attestation record or CI fixture guard like Phase AE did for the G9 workstation bundle.

## Requirements

- R1. `AdmissionG9EnablementEvidenceBundleAttestation` with `record_kind=hunyuan_admission_g9_enablement_evidence_bundle`.
- R2. `run_admission_g9_enablement_evidence_bundle()` writes `admission-g9-enablement-evidence-bundle.json`.
- R3. Record verify delegates nested `g9-enablement-evidence.json` schema checks.
- R4. CI smoke step + fixture verify in `hunyuan-admission-audit` job.
- R5. `ok=true` requires `admission_preflight_ok=true` and nested evidence `ok=true`.
- R6. Do **not** enable adapter or claim G7 hosted PASS.

## Non-goals

- Merging the enablement PR.
- Live Space inference wiring.
