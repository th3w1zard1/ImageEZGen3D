---
title: "feat: Gradio downloads for export sidecar and RAW GLB"
type: feat
status: completed
date: 2026-05-24
origin: docs/ideation/2026-05-24-post-trust-slice-refresh.md
---

# feat: Gradio downloads for export sidecar and RAW GLB

## Summary

Wire `export_sidecar` and `raw_glb` artifact keys into Create and History download components so users can fetch tier metadata and pre-decimation meshes from the UI. Backend and hosted smokes already produce these files; the gap is Gradio outputs only.

## Requirements

- R1. Create tab: `gr.File` for **Export sidecar** (`export_sidecar`) and **RAW GLB** (`raw_glb`) after STL, before ZIP bundle
- R2. `run_generate` populates session state and all return paths with verified paths for both keys
- R3. History tab: matching `gr.File` components; `open_history_run` returns verified paths
- R4. `generate.click` and `history_open.click` output lists include the two new components in consistent order
- R5. History inspect `artifact_strip_html` already lists keys present in manifest — no change required beyond verified artifacts dict
- R6. `tests/test_app.py` — source assertions that Create/History tabs declare the new download labels
- R7. Full unit suite passes (109+ tests); ruff clean on touched files

## Scope Boundaries

- Hunyuan enablement — deferred
- Hosted deploy / golden smoke — optional post-merge; not blocking this slice
- Draft tier may omit `raw_glb` — UI shows empty file when key absent (same as optional PLY/STL)

## Files

- Modify: `app.py`
- Modify: `tests/test_app.py`

## Test scenarios

- TS1: Create tab source contains `Export sidecar` and `RAW GLB` file labels
- TS2: History tab source contains same labels on history artifact files
- TS3: `generate.click` outputs list includes new file components between STL and bundle

## Decisions

- Place sidecar/RAW between STL and ZIP so tier-specific files sit with mesh exports and bundle remains last
- Reuse `_verified_artifact_state` — missing keys yield `None` on download widgets without fake paths
