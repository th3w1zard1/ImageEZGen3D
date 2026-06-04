# Hunyuan enablement evidence capstones verify bundle (Phase BD)

**Date:** 2026-06-03  
**Status:** Requirements for `/lfg` slice after Phase BC

## Problem

Phases BA–BC unified verify per capstone (admission, G9, neural), but operators and CI still run three separate verify commands after the admission capstone produces a full `--record-dir`.

## Requirements

- R1. `verify_enablement_evidence_capstones_files()` chains admission, G9, and neural capstone verify helpers in one record directory.
- R2. `scripts/verify_enablement_evidence_capstones.py` operator CLI.
- R3. CI smoke: one umbrella verify after all capstone runs (replace per-capstone verify steps).
- R4. Update stack index and G9 runbook preferred verify path.
- R5. Do **not** enable adapter or claim G7 hosted PASS.

## Non-goals

- Replacing individual capstone verify CLIs (Phases BA–BC).
- Tier-C GPU workstation execution or hosted G7 Block/Vase runs.
