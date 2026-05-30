# Hunyuan neural enablement preflight bundle (Phase AI)

**Date:** 2026-05-29  
**Status:** Requirements for `/lfg` slice after Phase AH

## Problem

Operators must run `hunyuan_g7_enablement_preflight_bundle.py` and `hunyuan_configured_inference_probe.py` separately to know whether tier-C neural enablement is ready. CI runs both as independent steps.

## Requirements

- R1. `run_neural_enablement_preflight_bundle()` chains G7 enablement preflight + configured adapter inference path.
- R2. `neural_enablement_ready=true` only when `g7_enablement_ready` and `neural_forward_ready` are both true.
- R3. CLI `--strict` exits 1 until `neural_enablement_ready`; CI-like skip exits 0 with `neural_enablement_ready=false`.
- R4. Replace separate G7 + configured-probe CI steps with one neural bundle step (superset).
- R5. Do **not** enable adapter on Space or claim G7 hosted PASS.

## Non-goals

- Hosted G7 live attestation or G9 enablement PR.
