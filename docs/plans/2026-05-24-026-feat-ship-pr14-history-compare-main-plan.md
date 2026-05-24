---
title: "feat: Ship PR #14 history compare to main"
type: feat
status: completed
date: 2026-05-24
origin: docs/plans/2026-05-24-025-feat-ship-history-compare-hosted-e2e-plan.md
---

# feat: Ship PR #14 history compare to main

## Summary

Unblock CI on `feat/phase3-history-compare-mvp`, merge PR #14, redeploy Space, and run post-merge hosted compare smoke on `main`.

## Requirements

- R1. Fix `scripts/hosted_history_compare_smoke.py` style guard (file must start with `from __future__ import annotations`)
- R2. `check_python_style.py` and full test suite pass locally
- R3. Push fix; CI green on PR #14
- R4. Squash-merge PR #14 to `main`
- R5. Post-merge: `hf_space_sync --execute` and `hosted_history_compare_smoke.py` on `main`
- R6. Record merge + post-merge run ids in hosted-validation KB

## Scope Boundaries

- Manifest diff export — deferred
- Mesh cleanup track — next slice after ship

## Files

- Modify: `scripts/hosted_history_compare_smoke.py`
- Modify: `docs/knowledgebase/40-operational-risk/hosted-validation-2026-05-23.md`
