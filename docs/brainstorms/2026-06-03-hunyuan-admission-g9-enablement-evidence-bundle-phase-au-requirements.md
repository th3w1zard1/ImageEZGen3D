# Hunyuan admission + G9 enablement evidence preflight bundle (Phase AU)

**Date:** 2026-06-03  
**Status:** Requirements for `/lfg` slice after Phase AT

## Problem

The G9 runbook lists separate preferred commands for admission preflight (`hunyuan_preflight_bundle.py`) and G9 enablement evidence (`hunyuan_g9_enablement_evidence_bundle.py`). Enablement PR reviewers need one operator command that writes admission audit JSON and the G9 evidence capstone in one `--record-dir`.

## Requirements

- R1. `run_admission_g9_enablement_evidence_bundle()` runs admission preflight bundle then `run_g9_enablement_evidence_bundle()`.
- R2. `admission_g9_enablement_evidence_ok` when admission preflight passes and G9 evidence preflight passes.
- R3. Forward `--live-probe`, `--hosted-neural`, `--require-hosted-neural`, and status args to the G9 evidence capstone.
- R4. CLI with `--record-dir`, `--skip-weight-warm`, `--strict`, `--json`.
- R5. `--strict` exit 1 when `g9_enablement_evidence_ready=false`.
- R6. Do **not** enable adapter or claim G7 hosted PASS.

## Non-goals

- Merging the enablement PR.
- Live Space inference wiring.
