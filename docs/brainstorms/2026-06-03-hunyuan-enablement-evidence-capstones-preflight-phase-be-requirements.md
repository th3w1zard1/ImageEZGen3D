# Hunyuan enablement evidence capstones preflight (Phase BE)

**Date:** 2026-06-03  
**Status:** Requirements for `/lfg` slice after Phase BD

## Problem

Phase BD unified capstone verify under `--record-dir`, but operators still run the admission capstone and umbrella verify as two separate commands.

## Requirements

- R1. `run_enablement_evidence_capstones()` runs admission capstone plus umbrella verify in one record directory.
- R2. `scripts/hunyuan_enablement_evidence_capstones.py` operator CLI (forwards admission capstone flags).
- R3. CI smoke: replace separate admission run + umbrella verify with one one-shot command.
- R4. Update stack index and G9 runbook preferred operator path.
- R5. Do **not** enable adapter or claim G7 hosted PASS.

## Non-goals

- Replacing individual capstone run or verify CLIs (Phases AU–BD).
- Tier-C GPU workstation execution or hosted G7 Block/Vase runs.
