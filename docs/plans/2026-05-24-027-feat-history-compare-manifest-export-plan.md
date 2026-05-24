---
title: "feat: History compare manifest diff export"
type: feat
status: completed
date: 2026-05-24
origin: docs/ideation/2026-05-24-post-trust-slice-refresh.md
---

# feat: History compare manifest diff export

## Summary

Complete the remaining Phase 3 compare item: export a structured manifest diff (JSON) plus downloadable markdown report alongside the in-app compare panel.

## Requirements

- R1. `manifest_ui.compare_runs_payload()` — structured left/right snapshots, `changed_fields`, artifact deltas
- R2. `compare_runs_markdown()` reuses payload (no behavior regression)
- R3. History tab: **Compare diff (JSON)** and **Compare report (MD)** file outputs after **Compare Runs**
- R4. Unit tests for payload structure and changed-field detection
- R5. Extend `hosted_history_compare_smoke.py` to assert JSON export fields via payload helper (local) or API file output optional — smoke still validates markdown API path
- R6. 92+ tests pass; style guard + ruff clean

## Scope Boundaries

- Quality-tier decimation wiring — next slice (Track 4)
- Hosted golden CI workflow — deferred
- Dual Model3D viewers — deferred

## Files

- Modify: `src/imageezgen3d/manifest_ui.py`
- Modify: `app.py`
- Modify: `tests/test_manifest_ui.py`
- Modify: `scripts/hosted_history_compare_smoke.py` (light validation hook if needed)
