# Hunyuan admission + G9 evidence bundle record ↔ evidence artifact parity (Phase AW)

**Date:** 2026-06-03  
**Status:** Requirements for `/lfg` slice after Phase AV

## Problem

Phase AV writes `admission-g9-enablement-evidence-bundle.json` with a nested `evidence` object alongside standalone `g9-enablement-evidence.json`, but nothing cross-checks that both artifacts stay aligned in one `--record-dir`.

## Requirements

- R1. `verify_admission_g9_enablement_evidence_bundle_evidence_artifact_parity()` fails when nested `evidence` diverges from standalone G9 evidence JSON.
- R2. Extend `verify_neural_enablement_artifact_files()` when both bundle and evidence JSON are present.
- R3. `run_admission_g9_enablement_evidence_bundle()` folds bundle evidence parity into `parity_ok`.
- R4. Gitignore local `g9-enablement-evidence.json` and `admission-g9-enablement-evidence-bundle.json`.
- R5. Do **not** enable adapter or claim G7 hosted PASS.

## Non-goals

- Merging the enablement PR.
- Live Space inference wiring.
