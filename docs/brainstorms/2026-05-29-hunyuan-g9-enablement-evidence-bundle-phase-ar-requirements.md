# Hunyuan G9 enablement evidence bundle (Phase AR)

**Date:** 2026-05-29  
**Status:** Requirements for `/lfg` slice after Phase AQ

## Problem

The G9 runbook chains admission preflight, neural capstone, hosted-neural recording, and parity verify as separate commands. Operators lack one attestation record (`g9-enablement-evidence.json`) that summarizes readiness for the enablement PR checklist.

## Requirements

- R1. `run_g9_enablement_evidence_bundle()` chains `run_neural_enablement_preflight_bundle()` and writes `g9-enablement-evidence.json`.
- R2. `g9_enablement_evidence_ready=true` requires `neural_enablement_ready=true` and `neural_enablement_preflight_ok=true`.
- R3. `--require-hosted-neural` additionally requires hosted G7 PASS (`hosted_neural_ok=true`).
- R4. Forward `--live-probe`, `--hosted-neural`, and status args to the neural capstone.
- R5. Record verify + fixture verify for CI; default CI path unchanged (no hosted neural required).
- R6. Do **not** set `configured=True` or claim G7 hosted PASS without valid status markdown.

## Non-goals

- Wiring GPU inference or merging the enablement PR.
- Updating hosted-validation markdown.
