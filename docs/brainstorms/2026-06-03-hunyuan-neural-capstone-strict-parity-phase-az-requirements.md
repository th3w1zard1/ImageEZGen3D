# Hunyuan neural capstone `--strict` parity gate (Phase AZ)

**Date:** 2026-06-03  
**Status:** Requirements for `/lfg` slice after Phase AY

## Problem

Phase AY aligned G9/admission capstone `--strict` with `parity_ok`, but the neural enablement capstone CLI still exits 0 under `--strict` when artifact parity fails while readiness flags pass.

## Requirements

- R1. `hunyuan_neural_enablement_preflight_bundle.py --strict` exits 1 when `parity_ok` is false.
- R2. Test covers strict+parity failure (mocked).
- R3. Update stack index and G9 runbook neural strict semantics.
- R4. Do **not** enable adapter or claim G7 hosted PASS.

## Non-goals

- Tier-C GPU workstation execution.
- Live Space G7 neural run.
