---
title: "feat: Phase 3 history compare MVP"
type: feat
status: active
date: 2026-05-24
origin: docs/ideation/2026-05-24-post-trust-slice-refresh.md
---

# feat: Phase 3 history compare MVP

## Summary

Ship PR #13, then add a minimal History **Compare Runs** flow: pick two recent runs and render a manifest-backed diff using `manifest_ui` (adapter, quality, score, fallback, artifacts).

## Requirements

- R0. Merge PR #13 to `main`
- R1. `manifest_ui.compare_runs_markdown()` diffs two run payloads
- R2. History tab: second run selector, **Compare Runs** button, compare markdown panel
- R3. Unit tests for compare markdown (same run, different adapters, artifact key diff)
- R4. Full `unittest discover` passes (89+ tests)
- R5. Browser smoke on live Space: History tab shows compare UI after Open Run path validated

## Scope Boundaries

- Dual Model3D side-by-side viewers — deferred
- Manifest JSON file export download — deferred
- Hunyuan / ZeroGPU — out of scope

## Files

- Modify: `src/imageezgen3d/manifest_ui.py`
- Modify: `app.py`
- Add: `tests/test_manifest_ui.py` (compare tests)
