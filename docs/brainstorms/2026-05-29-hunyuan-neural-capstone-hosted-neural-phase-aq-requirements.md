# Hunyuan neural capstone hosted-neural wiring (Phase AQ)

**Date:** 2026-05-29  
**Status:** Requirements for `/lfg` slice after Phase AP

## Problem

Operators run `hunyuan_g7_hosted_neural_record.py` and `hunyuan_neural_enablement_preflight_bundle.py` as separate steps. Phase AP added optional parity when both JSON files coexist, but the neural capstone does not produce the hosted-neural record.

## Requirements

- R1. Add `--hosted-neural` (plus `--status-file` or `--status-text`, optional `--sample`, `--space-url`) to `hunyuan_neural_enablement_preflight_bundle.py`.
- R2. When requested, write `hunyuan-g7-hosted-neural.json` under `--record-dir` and include hosted-neural status in bundle result/report.
- R3. Parity pass must run with the new artifact (Phase AP verify path).
- R4. CI default path unchanged (no status markdown required).
- R5. Do **not** enable adapter or claim G7 hosted PASS without valid status markdown.

## Non-goals

- Real G7 neural E2E on Space (operator execution).
- G9 enablement PR merge.
