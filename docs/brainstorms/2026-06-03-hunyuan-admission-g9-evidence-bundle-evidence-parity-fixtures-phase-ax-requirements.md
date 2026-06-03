# Hunyuan admission + G9 evidence bundle ↔ evidence parity fixtures (Phase AX)

**Date:** 2026-06-03  
**Status:** Requirements for `/lfg` slice after Phase AW

## Problem

Phase AW added bundle↔evidence parity in the artifact parity module and wired it into the neural capstone, but operators lack a dedicated verify CLI and CI lacks a static fixture smoke for the aligned artifact pair.

## Requirements

- R1. `verify_admission_g9_enablement_evidence_bundle_evidence_artifact_parity_files()` loads both JSON in a record directory.
- R2. `scripts/verify_admission_g9_enablement_evidence_bundle_evidence_artifact_parity.py` CLI for operators.
- R3. Align `tests/fixtures/admission-g9-enablement-evidence-bundle-skipped.json` nested `evidence` with `g9-enablement-evidence-skipped.json`; add fixture verify script + CI smoke.
- R4. Update stack index and G9 runbook.
- R5. Do **not** enable adapter or claim G7 hosted PASS.

## Non-goals

- Tier-C `--strict` workstation execution.
- Live Space G7 neural run.
- G9 enablement PR merge.
