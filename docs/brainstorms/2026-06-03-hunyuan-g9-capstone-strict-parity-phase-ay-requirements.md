# Hunyuan G9 capstone `--strict` parity gate (Phase AY)

**Date:** 2026-06-03  
**Status:** Requirements for `/lfg` slice after Phase AX

## Problem

Tier-C operator docs require `--strict` until `g9_enablement_evidence_ready=true` **and** `parity_ok=true`, but admission and G9 evidence capstone CLIs only fail `--strict` on readiness—not on `parity_ok`.

## Requirements

- R1. `hunyuan_admission_g9_enablement_evidence_bundle.py --strict` exits 1 when `parity_ok` is false.
- R2. `hunyuan_g9_enablement_evidence_bundle.py --strict` exits 1 when `parity_ok` is false.
- R3. Tests cover strict+parity failure paths (mocked).
- R4. Update stack index and G9 runbook strict semantics.
- R5. Do **not** enable adapter or claim G7 hosted PASS.

## Non-goals

- Tier-C GPU workstation execution.
- Live Space G7 neural run.
