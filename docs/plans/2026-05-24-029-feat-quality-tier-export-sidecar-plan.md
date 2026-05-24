---
title: "feat: Quality-tier export sidecar and decimation presets"
type: feat
status: completed
date: 2026-05-24
origin: docs/ideation/2026-05-24-post-trust-slice-refresh.md
---

# feat: Quality-tier export sidecar and decimation presets

## Summary

Wire quality tier to decimation targets in manifests and add a per-run **export sidecar** JSON (topology + budget) alongside GLB/OBJ exports. Establishes the mesh cleanup / export tiers contract before neural backends honor decimation.

## Requirements

- R1. `export_tiers.resolve_decimation_target(quality)` — draft / balanced / high presets
- R2. Orchestrator records `decimation_target` in manifest parameters; passes to adapters
- R3. `export_all` writes `{stem}.export.json` sidecar with topology and `within_decimation_budget`
- R4. CPU demo adapter produces sidecar; artifact key `export_sidecar`
- R5. `manifest_ui` surfaces export budget in run report; compare payload includes decimation
- R6. Unit tests for tiers, sidecar export, orchestrator parameters
- R7. 94+ tests; style guard + ruff clean

## Scope Boundaries

- Actual mesh decimation algorithm — deferred (neural / post-process path)
- RAW mesh duplicate format — deferred
- Hosted golden CI workflow — next optional slice

## Files

- Add: `src/imageezgen3d/export_tiers.py`
- Add: `tests/test_export_tiers.py`
- Modify: `src/imageezgen3d/exporters.py`, `src/imageezgen3d/adapters/base.py`, `src/imageezgen3d/adapters/cpu_demo.py`, `src/imageezgen3d/orchestrator.py`, `src/imageezgen3d/manifest_ui.py`
- Modify: `tests/test_cpu_demo.py`
