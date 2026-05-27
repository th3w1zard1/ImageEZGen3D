---
title: Hosted doc paths and CI artifact parity (Plan 069)
status: active
created: 2026-05-27
---

# Plan 069 — Hosted doc paths + admission/enablement G8 parity

## Problem

Plan 068 deduplicated section parsing but `hunyuan_enablement_preflight` still imports private `_HOSTED_VALIDATION` and `_read_text` from `hunyuan_admission`. There is no automated check that admission audit and enablement preflight emit the same `g8_enablement` snapshot.

## Scope

- Merge PR #50 (Plan 068) first.
- Move `HOSTED_VALIDATION_PATH` and `read_repo_text()` into `hosted_validation.py`.
- Update admission, enablement preflight, and admission audit script to use public imports.
- Add integration test for G8 (and G7 readiness) parity between audit JSON shape and enablement preflight.
- Refresh `hunyuan-admission-gates.md` last-audit line.

## Out of scope

- Hunyuan enablement or Space deploy.

## Test scenarios

1. `read_repo_text` returns empty string for missing path (unchanged behavior).
2. `evaluate_enablement_preflight().g8_enablement` equals `evaluate_g8_enablement_status(...)` with same gates.
3. Existing Hunyuan unit tests still pass.
