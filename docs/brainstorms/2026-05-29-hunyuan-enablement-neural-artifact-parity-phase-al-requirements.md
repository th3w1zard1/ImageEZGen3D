# Hunyuan enablement-neural artifact parity (Phase AL)

**Date:** 2026-05-29  
**Status:** Requirements for `/lfg` slice after Phase AK

## Problem

After neural preflight runs, `hunyuan-enablement-preflight.json` and `neural-enablement-preflight.json` coexist in `--record-dir` but `g7_readiness` is not cross-checked.

## Requirements

- R1. `verify_enablement_neural_artifact_parity()` fails when `g7_readiness` diverges between enablement preflight and neural record.
- R2. Extend neural preflight bundle parity pass to include enablement-neural checks.
- R3. Extend `verify_neural_enablement_artifact_parity.py` CLI to verify all three artifacts in `--record-dir`.
- R4. Do **not** enable adapter on Space or claim G7 hosted PASS.

## Non-goals

- Hosted G7 attestation or G9 enablement PR.
