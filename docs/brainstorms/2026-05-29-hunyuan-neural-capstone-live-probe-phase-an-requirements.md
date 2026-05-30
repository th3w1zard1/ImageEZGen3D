# Hunyuan neural capstone live-probe wiring (Phase AN)

**Date:** 2026-05-29  
**Status:** Requirements for `/lfg` slice after Phase AM

## Problem

Operators run `hunyuan_g7_preflight.py --live-probe` and `hunyuan_neural_enablement_preflight_bundle.py` as separate steps. Phase AM added optional parity when both JSON files coexist, but the neural capstone does not produce the live-probe record.

## Requirements

- R1. Add `--live-probe` (plus `--space-url`, `--sample`) to `hunyuan_neural_enablement_preflight_bundle.py`.
- R2. When requested, write `hunyuan-g7-live-probe.json` under `--record-dir` and include live-probe status in bundle result/report.
- R3. Parity pass must run with the new artifact (Phase AM verify path).
- R4. CI default path unchanged (no network live probe).
- R5. Do **not** enable adapter or claim G7 hosted PASS.

## Non-goals

- Real G7 neural E2E on Space after enablement.
- G9 enablement PR.
