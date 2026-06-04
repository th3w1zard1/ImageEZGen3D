# Hunyuan neural capstone verify bundle (Phase BC)

**Date:** 2026-06-03  
**Status:** Requirements for `/lfg` slice after Phase BB

## Problem

Phases BA–BB unified verify for admission and G9 capstones, but the neural enablement capstone still requires separate `verify_neural_enablement_record.py` and `verify_neural_enablement_artifact_parity.py` calls.

## Requirements

- R1. `verify_neural_enablement_preflight_bundle_files()` chains neural record verify and record-dir artifact parity.
- R2. `scripts/verify_neural_enablement_preflight_bundle.py` operator CLI.
- R3. CI smoke on record dir after neural capstone run.
- R4. Update stack index and G9 runbook neural capstone verify path.
- R5. Do **not** enable adapter or claim G7 hosted PASS.

## Non-goals

- Replacing admission or G9 verify bundles (Phases BA–BB).
- Tier-C GPU workstation execution.
