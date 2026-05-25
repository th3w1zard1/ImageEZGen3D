---
title: "feat: Hunyuan G3 dependency audit"
type: feat
status: completed
date: 2026-05-24
origin: docs/ideation/2026-05-24-next-runtime-slice.md
---

# feat: Hunyuan G3 dependency audit

## Summary

Close admission **gate G3** with pinned upstream requirements, redistribution notes, optional `hunyuan-audit` extra, and CI/local pip dry-run smoke. Adapter stays `configured=False`.

## Requirements

- R1. `requirements/hunyuan-pins.txt` at upstream commit `82920d64`
- R2. `hunyuan-dependencies.md` with `G3_STATUS: PASS`
- R3. `pyproject.toml` `[hunyuan-audit]` optional extra
- R4. `scripts/hunyuan_dependency_smoke.py` + CI job
- R5. Admission evaluator + gates doc G3 **PASS**

## Completion notes

- Full tier-C stack (bpy, cupy, deepspeed) documented but not installed — **G5** next.
