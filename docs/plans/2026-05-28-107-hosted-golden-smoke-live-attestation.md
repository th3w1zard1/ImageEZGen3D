---
title: Live hosted golden smoke attestation (Plan 107)
status: completed
created: 2026-05-28
---

# Plan 107 — Fresh hosted golden smoke on live Space

## Problem

Plans 078–106 hardened scheduled smoke JSON verify on `main`, but hosted-validation evidence is from 2026-05-24 runs. `AGENTS.md` requires a fresh live Space check after guard-stack changes.

## Scope

- Run `hosted_golden_smoke.py` against https://th3w1zard1-imageezgen3d.hf.space/ (Block sample).
- Run `verify_hosted_golden_smoke_record.py` on the record.
- Add Plan 107 validation section to `hosted-validation-2026-05-23.md` with run id, adapter, `g7_false_neural_guard_ok`, artifact sizes.
- Do **not** commit transient JSON artifacts to the repo.

## Out of scope

- Hunyuan enablement or claiming G7 PASS / ZeroGPU neural validation.

## Test scenarios

1. Smoke exits 0; record shows Local CPU Preview or honest fallback (not false G7 neural).
2. `g7_false_neural_guard_ok` is true in the record.

## Files

- `docs/plans/2026-05-28-107-hosted-golden-smoke-live-attestation.md`
- `docs/knowledgebase/40-operational-risk/hosted-validation-2026-05-23.md`
