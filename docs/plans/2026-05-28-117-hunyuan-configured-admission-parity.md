---
title: Hunyuan configured admission parity (Plan 117)
type: fix
status: completed
date: 2026-05-28
---

# Plan 117 — Hunyuan `configured` admission parity

## Summary

Plan 115 wired `IMAGEEZ_HUNYUAN_CONFIGURED` into the orchestrator, but admission audit and enablement preflight still read `HunyuanPlaceholderAdapter()` with default `configured=False`. Add a single resolver and use it everywhere so unsafe enablement is detected when the env flag is on.

## Requirements

- R1. `resolve_hunyuan_configured()` reads `AppConfig.hunyuan.configured` (env/pyproject).
- R2. `hunyuan_admission`, `hunyuan_admission_audit`, `hunyuan_enablement_preflight` use the resolver.
- R3. When env configured true with G7–G9 open, preflight/audit exit 1 (unsafe config).
- R4. Orchestrator `adapter_choices` includes `hunyuan-zerogpu` when config configured true.
- R5. No Space deploy; G7 still OPEN.

## Scope Boundaries

- GPU inference implementation.
- Setting env on hosted Space.

## Implementation Units

- U1. Resolver + call-site updates (`hunyuan.py`, admission modules)
- U2. Tests (`test_hunyuan_admission.py`, `test_hunyuan_enablement_preflight.py`, `test_cpu_demo.py`)
- U3. KB Plan 117 note in hosted-validation

**Verification:** `pytest` on hunyuan + config + cpu_demo orchestrator tests.
