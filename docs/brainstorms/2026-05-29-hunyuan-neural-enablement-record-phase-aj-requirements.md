# Hunyuan neural enablement attestation record (Phase AJ)

**Date:** 2026-05-29  
**Status:** Requirements for `/lfg` slice after Phase AI

## Problem

Neural enablement preflight reports to stdout but does not persist a tier-C evidence record like G9 `g9-workstation-bundle.json`.

## Requirements

- R1. `NeuralEnablementAttestation` with `record_kind=hunyuan_neural_enablement` written to `neural-enablement-preflight.json`.
- R2. `run_neural_enablement_preflight_bundle()` writes and verifies the record under `--record-dir`.
- R3. `verify_neural_enablement_record.py` + fixture verify for CI.
- R4. `ok=true` requires `neural_enablement_ready=true` and nested preflight gates.
- R5. Do **not** enable adapter on Space or claim G7 hosted PASS.

## Non-goals

- Hosted G7 attestation or G9 enablement PR.
