# Hunyuan G7 hosted neural attestation record (Phase AO)

**Date:** 2026-05-29  
**Status:** Requirements for `/lfg` slice after Phase AN

## Problem

After enablement, operators must prove a real hosted Block/Vase run via `validate_g7_hosted_generate_status()`, but there is no JSON attestation record or verify CLI like other Hunyuan evidence artifacts.

## Requirements

- R1. `hunyuan_g7_hosted_neural_record` module builds/writes/verifies `hunyuan-g7-hosted-neural.json` from generation status markdown.
- R2. `ok=true` only when `validate_g7_hosted_generate_status()` passes and `run_id` is present.
- R3. Record CLI accepts `--status-file` or `--status-text`; verify CLI + fixture verify for CI.
- R4. Do **not** enable adapter on Space or claim G7 PASS in hosted-validation from fixtures alone.

## Non-goals

- Automated live Space generate in CI.
- G9 enablement PR merge.
