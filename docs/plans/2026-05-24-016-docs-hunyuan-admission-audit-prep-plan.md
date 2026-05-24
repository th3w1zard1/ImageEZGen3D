---
title: "docs: Hunyuan admission audit prep"
type: docs
status: completed
date: 2026-05-24
origin: docs/ideation/2026-05-23-next-focus-ideation.md #3
---

# docs: Hunyuan admission audit prep

## Summary

Publish a durable Hunyuan enablement gate checklist (documentation only). Do not enable the `hunyuan-zerogpu` adapter or change `configured=True`.

---

## Requirements

- R1. Add `docs/knowledgebase/hunyuan-admission-gates.md` with numbered gates, evidence fields, and current status
- R2. Cross-link from `license-audit.md`, `model-matrix.md`, and KB index
- R3. Point `HunyuanPlaceholderAdapter` error message at the new gate doc
- R4. Note hosted CPU fallback validation as a completed prerequisite (Plan 015)
- R5. Unit test asserts adapter remains disabled and references gate doc
- R6. Full unittest suite passes

---

## Scope Boundaries

- Wiring Hunyuan model code — out of scope
- Setting `configured=True` — forbidden in this plan

---

## Files

- Add: `docs/knowledgebase/hunyuan-admission-gates.md`
- Modify: `docs/knowledgebase/license-audit.md`, `docs/knowledgebase/README.md`, `docs/knowledgebase/model-matrix.md`, `src/imageezgen3d/adapters/hunyuan.py`, `tests/test_hunyuan_admission.py`
