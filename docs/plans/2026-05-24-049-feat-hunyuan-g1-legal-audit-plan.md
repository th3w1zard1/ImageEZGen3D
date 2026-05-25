---
title: "feat: Hunyuan G1 legal audit documentation"
type: feat
status: completed
date: 2026-05-24
origin: docs/ideation/2026-05-24-post-trust-slice-refresh.md
---

# feat: Hunyuan G1 legal audit documentation

## Summary

Close admission **gate G1** by documenting Tencent Hunyuan 3D 2.1 Community License terms at pinned GitHub/HF revisions in `license-audit.md`, without enabling the adapter.

## Requirements

- R1. Add Hunyuan3D-2.1 audit record with revision pins and license summary table
- R2. Set `G1_STATUS: PASS` marker for automated audit
- R3. Update `hunyuan-admission-gates.md` G1 row to **PASS**
- R4. Update `hunyuan_admission.py` G1 evaluation + test
- R5. Adapter remains `configured=False`

## Completion

- GitHub pin: `82920d643c0dc2f7bfd7255f45f62d386edfe60c`
- HF pin: `0b94677654c57bb9a6b6845cd7b704ccf551d327`
- G2–G8 remain open
