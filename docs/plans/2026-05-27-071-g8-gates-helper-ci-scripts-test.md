---
title: G8 gates helper and CI scripts subprocess contract (Plan 071)
status: active
created: 2026-05-27
---

# Plan 071 — G8 gates helper + CI scripts subprocess contract

## Problem

Plan 070 centralized admission audit JSON, but G8 assembly for a gate tuple is still duplicated between `hunyuan_admission_audit.py` and `hunyuan_enablement_preflight.py`. There is no subprocess test mirroring scheduled smoke (both CLIs writing JSON artifacts).

## Scope

- Merge PR #52 (Plan 070) first.
- Add `g8_enablement_for_gates(gates)` in `hunyuan_g8_preflight.py`; use in audit builder and enablement preflight.
- Add `tests/test_hunyuan_ci_scripts.py` — subprocess `--record` for admission audit + enablement preflight; assert matching `g7_readiness` / `g8_enablement`.
- KB Plan 071 note.

## Out of scope

- Hunyuan enablement or Space deploy.

## Test scenarios

1. `g8_enablement_for_gates` matches `build_admission_audit_payload` G8 block.
2. Both CLI scripts exit 0 and write JSON with aligned G7/G8 sections.
