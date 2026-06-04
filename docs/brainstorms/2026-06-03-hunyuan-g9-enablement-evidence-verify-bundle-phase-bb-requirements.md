# Hunyuan G9 enablement evidence verify bundle (Phase BB)

**Date:** 2026-06-03  
**Status:** Requirements for `/lfg` slice after Phase BA

## Problem

Phase AR provides the G9 evidence capstone run command, but operators still run `verify_g9_enablement_evidence_record.py` and rely on separate neural parity checks manually after `--record-dir` execution.

## Requirements

- R1. `verify_g9_enablement_evidence_bundle_files()` chains G9 evidence record verify and record-dir artifact parity.
- R2. `scripts/verify_g9_enablement_evidence_bundle.py` operator CLI.
- R3. CI smoke on record dir after G9 evidence capstone run.
- R4. Update stack index and G9 runbook preferred verify path for G9 capstone subset.
- R5. Do **not** enable adapter or claim G7 hosted PASS.

## Non-goals

- Replacing admission capstone verify bundle (Phase BA).
- Tier-C GPU workstation execution.
