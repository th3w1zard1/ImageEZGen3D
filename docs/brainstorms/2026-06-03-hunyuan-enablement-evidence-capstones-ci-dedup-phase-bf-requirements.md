# Hunyuan enablement evidence capstones CI dedup (Phase BF)

**Date:** 2026-06-03  
**Status:** Requirements for `/lfg` slice after Phase BE

## Problem

Phase BE runs umbrella capstone verify inside the preflight CLI, but CI still executes `verify_neural_enablement_artifact_parity.py` afterward. Post-BE operational docs also reference older capstone commands instead of the BE one-shot path.

## Requirements

- R1. Remove redundant CI `verify_neural_enablement_artifact_parity.py` step after capstones preflight.
- R2. Add test asserting capstones verify subsumes neural artifact parity on a CI-like record dir.
- R3. Align post-BE operator paths in stack index and G7 readiness doc with `hunyuan_enablement_evidence_capstones.py --strict`.
- R4. Do **not** enable adapter or claim G7 hosted PASS.

## Non-goals

- Removing individual capstone run CLIs or fixture verify steps.
- Tier-C GPU workstation execution or hosted G7 Block/Vase runs.
