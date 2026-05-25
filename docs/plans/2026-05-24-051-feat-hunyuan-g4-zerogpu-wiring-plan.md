---
title: "feat: Hunyuan G4 ZeroGPU wiring scaffold"
type: feat
status: completed
date: 2026-05-24
origin: docs/ideation/2026-05-24-next-runtime-slice.md
---

# feat: Hunyuan G4 ZeroGPU wiring scaffold

## Summary

Close admission **gate G4** by isolating future Hunyuan inference behind `@spaces.GPU` in code, with a local no-op fallback when `spaces` is not installed. Adapter stays `configured=False`.

## Requirements

- R1. `hunyuan.py` exposes `@spaces.GPU`-decorated GPU inference shell (string present for audit)
- R2. `generate()` still raises while `configured=False`
- R3. `hunyuan_admission` G4 passes; tests for G4 + disabled adapter
- R4. Update `hunyuan-admission-gates.md` G4 row to **PASS**
- R5. Brief note in `zerogpu-runtime.md` linking scaffold

## Scope Boundaries

- No Hunyuan model install or weight download
- G3, G5–G8 remain open

## Files

- Modify: `src/imageezgen3d/adapters/hunyuan.py`
- Modify: `docs/knowledgebase/hunyuan-admission-gates.md`
- Modify: `docs/knowledgebase/zerogpu-runtime.md`
- Modify: `tests/test_hunyuan_admission.py`
- Add: `tests/test_hunyuan_adapter.py`

## Completion notes

- G4 closes wiring scaffold only; `configured=False` unchanged.
