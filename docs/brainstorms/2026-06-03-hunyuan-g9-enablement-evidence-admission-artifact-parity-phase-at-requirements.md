# Hunyuan G9 enablement evidence ↔ admission audit artifact parity (Phase AT)

**Date:** 2026-06-03  
**Status:** Requirements for `/lfg` slice after Phase AS

## Problem

Phase AR–AS write `g9-enablement-evidence.json` and cross-check it against `neural-enablement-preflight.json`, but admission-layer JSON (`hunyuan-admission-audit.json`, `hunyuan-enablement-preflight.json`) in the same `--record-dir` is not cross-checked against G9 evidence when both coexist.

## Requirements

- R1. `verify_g9_enablement_evidence_admission_artifact_parity()` fails when evidence `ok=true` but admission audit has `adapter_configured=true` (enablement PR safety guard).
- R2. Extend `verify_neural_enablement_artifact_files()` when `g9-enablement-evidence.json` and `hunyuan-admission-audit.json` are both present (optional — CI unchanged without both files).
- R3. When admission enablement preflight JSON is also present, delegate `verify_hunyuan_ci_artifact_parity` (reuse existing rules).
- R4. Validate G9 evidence record schema before parity compare.
- R5. Do **not** enable adapter or claim G7 hosted PASS.

## Non-goals

- Merging the enablement PR or setting `IMAGEEZ_HUNYUAN_CONFIGURED=true`.
- Live Space Block/Vase automation.
