---
title: "feat: Hunyuan G2 weight access documentation"
type: feat
status: completed
date: 2026-05-24
origin: docs/ideation/2026-05-24-next-runtime-slice.md
---

# feat: Hunyuan G2 weight access documentation

## Summary

Close admission **gate G2** by recording a live `hf download --dry-run` for `tencent/Hunyuan3D-2.1`, documenting Space secret handling, and wiring the admission audit — without downloading weights into git or enabling the adapter.

## Requirements

- R1. Add `hunyuan-weight-access.md` with dry-run log summary, size, file count, auth notes
- R2. Set `G2_STATUS: PASS` marker and Space secrets plan in deployment docs
- R3. Update `hunyuan-admission-gates.md` G2 row to **PASS**
- R4. Update `hunyuan_admission.py` G2 evaluation + test
- R5. Adapter remains `configured=False`

## Scope Boundaries

- No full weight download to repo or CI artifacts
- G3–G8 remain open

## Files

- Add: `docs/knowledgebase/hunyuan-weight-access.md`
- Modify: `docs/knowledgebase/deployment-hf-cli.md`
- Modify: `docs/knowledgebase/hunyuan-admission-gates.md`
- Modify: `src/imageezgen3d/hunyuan_admission.py`
- Modify: `tests/test_hunyuan_admission.py`

## Completion notes

- Dry-run: 30 files, 14.9 GB; Hub `gated=false`; pin `0b946776`.
- G3–G8 remain open; adapter `configured=False`.
