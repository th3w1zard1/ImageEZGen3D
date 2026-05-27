---
title: "feat: Ship PR #41 + Hunyuan G7 preflight harness"
type: feat
status: completed
date: 2026-05-27
origin: docs/ideation/2026-05-24-next-runtime-slice.md
---

# feat: Ship PR #41 + Hunyuan G7 preflight harness

## Summary

Squash-merge PR #41 (G6 manifest sample), then add a **G7 preflight** module and CLI that proves G1–G6 are closed in-repo and documents the hosted contract for a future real `hunyuan-zerogpu` run—without enabling the adapter.

## Requirements

- R1. Squash-merge PR #41
- R2. `evaluate_g7_readiness()` — admission G1–G6 must pass; G7 remains open
- R3. `validate_g7_hosted_generate_status()` — asserts neural path markers (for post-enablement runs)
- R4. `scripts/hunyuan_g7_preflight.py` — local audit + optional live Space probe (`adapter=hunyuan-zerogpu` must not claim success while disabled)
- R5. Unit tests; `hunyuan_admission_audit` G7 evidence mentions preflight
- R6. KB `hunyuan-g7-preflight.md`; ideation note G7 preflight landed
- R7. Hosted golden smoke (cpu path) still passes

## Scope boundaries

- Do **not** set `configured=True` or claim G7 PASS
- No Space deploy unless PR #41 code not yet on Hub (G6 is repo-only)

## Files

- Add: `src/imageezgen3d/hunyuan_g7_preflight.py`
- Add: `scripts/hunyuan_g7_preflight.py`
- Add: `tests/test_hunyuan_g7_preflight.py`
- Add: `docs/knowledgebase/hunyuan-g7-preflight.md`
- Modify: `src/imageezgen3d/hunyuan_admission.py`
- Modify: `docs/knowledgebase/hunyuan-admission-gates.md`

## Test scenarios

- Readiness fails if any G1–G6 gate open (mock)
- G7 status validator accepts hunyuan-zerogpu status, rejects cpu-demo
- CLI exits 0 when G1–G6 pass locally
