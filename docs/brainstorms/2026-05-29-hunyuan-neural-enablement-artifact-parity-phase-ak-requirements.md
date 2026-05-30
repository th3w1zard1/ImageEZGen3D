# Hunyuan neural enablement artifact parity (Phase AK)

**Date:** 2026-05-29  
**Status:** Requirements for `/lfg` slice after Phase AJ

## Problem

`neural-enablement-preflight.json` and `g9-workstation-bundle.json` are written under the same `--record-dir` but nothing verifies cross-artifact consistency.

## Requirements

- R1. `verify_neural_enablement_artifact_parity()` checks neural record schema plus alignment with G9 bundle when present.
- R2. `run_neural_enablement_preflight_bundle()` runs parity verify after record write; exposes `parity_ok`.
- R3. `scripts/verify_neural_enablement_artifact_parity.py` for operators; CI step after neural preflight.
- R4. Do **not** enable adapter on Space or claim G7 hosted PASS.

## Non-goals

- Hosted G7 attestation or G9 enablement PR.
