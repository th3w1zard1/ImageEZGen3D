---
title: "feat: Ship manifest UI + hosted validation"
type: feat
status: completed
date: 2026-05-24
origin: docs/plans/2026-05-24-017-feat-manifest-driven-ui-components-plan.md
---

# feat: Ship manifest UI + hosted validation

## Summary

PR #9 merged to `main`. Redeploy HF Space, run hosted Block E2E, verify comprehension exit and manifest-driven copy on live Space, update hosted validation KB.

---

## Requirements

- R1. Deploy Space from `main` via `scripts/hf_space_sync.py --execute`
- R2. Hosted `/generate` Block sample completes with run id and artifacts
- R3. Status markdown includes `## What happened` (manifest_ui report path)
- R4. Browser smoke: Create tab quality intake + fallback notice on live Space
- R5. Update `hosted-validation-2026-05-23.md` with Plan 017 evidence
- R6. Full unittest suite passes on `main`

---

## Scope Boundaries

- History tab UI automation for Open Run — optional browser only; API E2E sufficient for R3

---

## Files

- Modify: `docs/knowledgebase/40-operational-risk/hosted-validation-2026-05-23.md`
