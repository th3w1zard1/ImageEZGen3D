# Hunyuan G7 hosted neural ↔ enablement artifact parity (Phase AP)

**Date:** 2026-05-29  
**Status:** Requirements for `/lfg` slice after Phase AO

## Problem

G9 evidence may colocate `hunyuan-g7-hosted-neural.json` (post-enablement PASS) with `neural-enablement-preflight.json` in one `--record-dir`, but nothing checks that hosted G7 PASS aligns with tier-C neural enablement readiness.

## Requirements

- R1. `verify_g7_hosted_neural_enablement_artifact_parity()` fails when hosted record `ok=true` but neural record is not enablement-ready.
- R2. Extend `verify_neural_enablement_artifact_files()` when hosted neural JSON is present (optional — CI unchanged without file).
- R3. Validate hosted neural record schema before parity compare.
- R4. Do **not** enable adapter or claim G7 PASS from fixtures alone.

## Non-goals

- Live Space generate automation.
- Updating hosted-validation markdown.
