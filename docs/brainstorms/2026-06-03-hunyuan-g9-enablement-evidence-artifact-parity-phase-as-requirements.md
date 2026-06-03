# Hunyuan G9 enablement evidence ↔ neural artifact parity (Phase AS)

**Date:** 2026-06-03  
**Status:** Requirements for `/lfg` slice after Phase AR

## Problem

Phase AR writes `g9-enablement-evidence.json` alongside `neural-enablement-preflight.json` in one `--record-dir`, but nothing cross-checks that G9 evidence flags align with the neural record when both coexist.

## Requirements

- R1. `verify_g9_enablement_evidence_neural_artifact_parity()` fails when evidence record `ok=true` but neural record is not enablement-ready.
- R2. Extend `verify_neural_enablement_artifact_files()` when `g9-enablement-evidence.json` is present (optional — CI unchanged without file).
- R3. G9 evidence bundle runs parity after writing the evidence record and surfaces `parity_ok`.
- R4. Validate G9 evidence record schema before parity compare.
- R5. Do **not** enable adapter or claim G7 hosted PASS.

## Non-goals

- Live Space generate automation.
- G9 enablement PR merge.
