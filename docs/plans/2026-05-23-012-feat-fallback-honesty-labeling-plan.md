---
title: "feat: Hosted fallback honesty labeling"
type: feat
status: completed
date: 2026-05-24
origin: docs/ideation/2026-05-23-next-focus-ideation.md #2
---

# feat: Hosted fallback honesty labeling

## Summary

Merge PR #3, then surface cpu-demo fallback reason and preview disclaimer in Create UI, run status, and manifest — never silent box-mesh "success" when ZeroGPU adapter is disabled on Space.

---

## Requirements

- R1. Merge PR #3 (docs post-merge validation)
- R2. Pre-run notice when fallback is armed (ZeroGPU unavailable/disabled)
- R3. Post-run status includes preview disclaimer for cpu-demo fallback runs
- R4. Manifest records `preview_disclaimer` when applicable
- R5. Unit tests for new copy helpers
- R6. Full unittest suite passes

---

## Scope Boundaries

- Hunyuan enablement — out of scope
- Full manifest-driven component library — deferred

---

## Files

- Modify: `app.py`, `src/imageezgen3d/orchestrator.py`, `tests/test_app.py`
