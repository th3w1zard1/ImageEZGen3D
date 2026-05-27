---
title: "feat: Ship PR #39 + History tab idle backend rail parity"
type: feat
status: completed
date: 2026-05-27
origin: docs/plans/2026-05-27-057-feat-ship-pr38-golden-smoke-rail-chip-plan.md
---

# feat: Ship PR #39 + History tab idle backend rail parity

## Summary

Squash-merge PR #39 (Plan 057 hosted golden smoke rail assertion), then align History tab initial Project Rail with Create tab by passing `resolution` into `_history_overview_html` when there are no runs yet.

## Requirements

- R1. Squash-merge PR #39
- R2. History tab `history_summary` uses `_history_overview_html(history_runs, resolution=resolution)`
- R3. Unit tests pass (`test_hosted_golden_smoke`, `test_manifest_ui`; app tests if Gradio available)
- R4. Live hosted golden smoke + browser spot-check on Space
- R5. KB Plan 058 section; ideation follow-up marked shipped

## Scope boundaries

- G7 Hunyuan enablement — deferred (`configured=False`)
- Space redeploy — only if smoke fails on stale Space

## Files

- Modify: `app.py`
- Modify: `docs/ideation/2026-05-24-next-runtime-slice.md`
- Modify: `docs/knowledgebase/40-operational-risk/hosted-validation-2026-05-23.md`

## Test scenarios

- Idle History overview with `resolution` shows **What backend ran** (reuse `test_history_overview_shows_idle_backend_chips_from_resolution` contract)
- Hosted golden smoke still passes rail HTML check after merge
