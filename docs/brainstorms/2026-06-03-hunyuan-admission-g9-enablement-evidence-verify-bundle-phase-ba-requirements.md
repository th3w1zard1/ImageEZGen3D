# Hunyuan admission + G9 evidence verify bundle (Phase BA)

**Date:** 2026-06-03  
**Status:** Requirements for `/lfg` slice after Phase AZ

## Problem

Phase AU provides one run command for the admission + G9 evidence capstone, but operators still run multiple verify CLIs (bundle record, G9 evidence record, bundle↔evidence parity) manually after `--record-dir` execution.

## Requirements

- R1. `verify_admission_g9_enablement_evidence_bundle_files()` chains bundle record, G9 evidence record, and bundle↔evidence parity checks in one record directory.
- R2. `scripts/verify_admission_g9_enablement_evidence_bundle.py` operator CLI.
- R3. CI smoke on record dir after admission capstone run.
- R4. Update stack index and G9 runbook preferred verify path.
- R5. Do **not** enable adapter or claim G7 hosted PASS.

## Non-goals

- Replacing `verify_neural_enablement_artifact_parity.py` (broader cross-artifact scope).
- Tier-C GPU workstation execution.
