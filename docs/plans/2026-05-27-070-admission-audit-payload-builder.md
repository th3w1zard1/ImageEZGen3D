---
title: Centralized admission audit JSON payload (Plan 070)
status: completed
created: 2026-05-27
---

# Plan 070 — Centralized admission audit JSON payload

## Problem

Plan 069 added CI artifact parity tests that re-implement admission audit G8 logic inline. `scripts/hunyuan_admission_audit.py` owns the payload shape but it is not importable, so drift is possible when the script changes.

## Scope

- Merge PR #51 (Plan 069) first.
- Add `build_admission_audit_payload()` in `src/imageezgen3d/hunyuan_admission_audit.py`.
- Thin the CLI script to call the builder.
- Update parity tests to use the shared builder for G7/G8 assertions.
- Document in `hunyuan-g7-preflight.md` and hosted-validation Plan 070 note.

## Out of scope

- Hunyuan enablement or Space deploy.

## Test scenarios

1. Payload includes `adapter_configured`, `g7_readiness`, `g8_enablement`, `gates`.
2. `payload["g8_enablement"]` matches `evaluate_enablement_preflight().g8_enablement`.
3. Admission audit subprocess `--record` still succeeds.
