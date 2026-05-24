---
title: "feat: Ship fallback honesty + hosted Space validation"
type: feat
status: completed
date: 2026-05-24
origin: docs/plans/2026-05-23-012-feat-fallback-honesty-labeling-plan.md
---

# feat: Ship fallback honesty + hosted Space validation

## Summary

Merge PR #4 (Plan 012 fallback honesty labeling), fix CI lint, redeploy the HF Space from `main`, and run hosted Block E2E to verify fallback banner, disclaimer, manifest, and artifacts on the live app.

---

## Requirements

- R1. Fix Ruff E402 on `app.py` orchestrator imports (CI lint green)
- R2. Merge PR #4 to `main`
- R3. Deploy Space via repo sync script / HF CLI
- R4. Hosted E2E: Block sample completes with run id, cpu-demo fallback visible, manifest + GLB + OBJ present
- R5. Update hosted validation KB evidence and parity register if needed
- R6. Full unittest suite passes locally

---

## Scope Boundaries

- Trust-first Phase 1 UX polish — deferred to next plan
- Hunyuan adapter enablement — out of scope

---

## Files

- Modify: `app.py` (lint fix)
- Modify: `docs/knowledgebase/40-operational-risk/hosted-validation-2026-05-23.md`
- Modify: `docs/knowledgebase/40-operational-risk/source-runtime-parity-register.md` (if warranted)
