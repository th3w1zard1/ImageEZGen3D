# Hunyuan G7 live-probe ↔ neural artifact parity (Phase AM)

**Date:** 2026-05-29  
**Status:** Requirements for `/lfg` slice after Phase AL

## Problem

Scheduled smoke and tier-C operators may have both `hunyuan-g7-live-probe.json` (hosted `--live-probe`) and `neural-enablement-preflight.json` in the same `--record-dir`, but `g7_readiness` / `readiness` is not cross-checked.

## Requirements

- R1. `verify_g7_live_probe_neural_artifact_parity()` fails when `readiness` diverges from neural `preflight.g7_enablement.g7_readiness`.
- R2. Extend `verify_neural_enablement_artifact_files()` to run live-probe parity **when** `hunyuan-g7-live-probe.json` is present (optional — CI neural preflight unchanged).
- R3. Validate live-probe record schema before parity compare.
- R4. Do **not** enable adapter on Space or claim G7 hosted PASS.

## Non-goals

- Wiring `--live-probe` into neural enablement preflight bundle (future operator slice).
- G9 enablement PR.
