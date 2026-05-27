---
title: "feat: Ship PR #46 + G7 validation placeholder and G9 enablement runbook"
type: feat
status: completed
date: 2026-05-27
origin: docs/plans/2026-05-27-064-feat-ship-pr45-enablement-preflight-scheduled-plan.md
---

# feat: Ship PR #46 + G7 validation placeholder and G9 enablement runbook

## Summary

Squash-merge PR #46 (enablement preflight on scheduled smoke), add a **`## G7 validation` placeholder** in hosted-validation (prevents prose false passes), document **G9 enablement/rollback runbook**, and align admission gate table labels with automated checks.

## Requirements

- R1. Squash-merge PR #46
- R2. `## G7 validation` placeholder section with `G7_STATUS: OPEN` in hosted-validation doc
- R3. `docs/knowledgebase/hunyuan-g9-enablement-runbook.md` (rollback + enablement PR checklist)
- R4. Align `hunyuan-admission-gates.md` G8/G9 status notes with code
- R5. Test `_g7_hosted_validation_passed` rejects placeholder OPEN section
- R6. Hosted golden smoke + enablement preflight still pass

## Scope boundaries

- Do not set `configured=True`
- Do not claim G7 PASS

## Files

- Modify: `docs/knowledgebase/40-operational-risk/hosted-validation-2026-05-23.md`
- Add: `docs/knowledgebase/hunyuan-g9-enablement-runbook.md`
- Modify: `docs/knowledgebase/hunyuan-admission-gates.md`
- Modify: `tests/test_hunyuan_admission.py`
