---
title: "feat: Ship history compare with hosted E2E"
type: feat
status: completed
date: 2026-05-24
origin: docs/plans/2026-05-24-024-feat-phase3-history-compare-mvp-plan.md
---

# feat: Ship history compare with hosted E2E

## Summary

Close Plan 024 R5: validate **Compare Runs** on the live Hugging Face Space with two persisted runs and API-driven compare, then record evidence in the hosted validation KB.

## Requirements

- R1. Explicit Gradio `api_name` on compare and history refresh handlers (`compare_history_runs`, `history_updates`)
- R2. `scripts/hosted_history_compare_smoke.py` — two `/generate` calls (Block sample), `/history_updates_1`, `/compare_history_runs`; exit 0 when `## Run comparison` present
- R3. Update `docs/knowledgebase/40-operational-risk/hosted-validation-2026-05-23.md` with Plan 024/025 evidence
- R4. Mark Plan 024 requirements complete in plan frontmatter
- R5. Run smoke script against live Space; redeploy if app API names changed
- R6. Unit tests remain green (90+)

## Scope Boundaries

- CI job for hosted smoke — deferred (ideation item 4)
- Manifest diff export download — deferred
- Merge PR #14 — orchestrator step after validation

## Files

- Modify: `app.py`
- Add: `scripts/hosted_history_compare_smoke.py`
- Modify: `docs/knowledgebase/40-operational-risk/hosted-validation-2026-05-23.md`
- Modify: `docs/plans/2026-05-24-024-feat-phase3-history-compare-mvp-plan.md`
