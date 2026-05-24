---
title: "fix: Resolve PR #2 merge conflicts with main"
type: fix
status: completed
date: 2026-05-24
origin: PR #2 mergeable CONFLICTING
---

# fix: Resolve PR #2 merge conflicts with main

## Summary

Merge `origin/main` (PR #1 landed as `18f2ae1`) into `feat/knowledgebase-orchestration-pass`, resolve 11 conflicted files, verify tests, and push so PR #2 becomes mergeable with fresh CI.

---

## Requirements

- R1. Resolve all merge conflicts without losing Space port 7860 fix, hosted E2E evidence, or plan 005–009 completions
- R2. Preserve main-only changes if any are not duplicated on branch
- R3. Full unittest suite passes after merge
- R4. Push merge commit; PR #2 mergeable

---

## Conflict files

- `src/imageezgen3d/config.py`, `tests/test_config.py` — port resolution logic
- `docs/knowledgebase/deployment-hf-cli.md` — port/runbook
- Docs/plans/solutions/ideation/parity — add/add; prefer branch post-005 state

---

## Scope Boundaries

- New features — out of scope
- Rebase/force-push — avoid; use merge commit
