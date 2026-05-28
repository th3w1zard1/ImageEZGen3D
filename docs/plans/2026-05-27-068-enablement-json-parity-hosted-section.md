---
title: Enablement JSON parity and hosted validation helper (Plan 068)
status: completed
created: 2026-05-27
---

# Plan 068 — Enablement preflight JSON parity + shared hosted section helper

## Problem

Plan 067 added `g8_enablement` to admission audit JSON but enablement preflight JSON still exposes only `g8_enablement_documented` (boolean). G7 is similarly reduced to `g7_readiness_ready`. Operators comparing scheduled smoke artifacts must cross-reference two files for full G7/G8 state.

`hosted_validation_section()` is duplicated in `hunyuan_admission.py` and `hunyuan_g8_preflight.py`.

## Scope

- Merge PR #49 (Plan 067) first.
- Add `src/imageezgen3d/hosted_validation.py` with shared section parser.
- Enablement preflight `to_dict()` includes nested `g7_readiness` and `g8_enablement` (keep boolean fields for compatibility).
- Docs + tests.

## Out of scope

- Hunyuan enablement or Space deploy.

## Test scenarios

1. `hunyuan-enablement-preflight.json` contains `g8_enablement.interim_open` and `g7_readiness.ready`.
2. G7/G8 validators unchanged behavior after shared helper extraction.
3. Admission audit JSON still includes `g8_enablement`.
