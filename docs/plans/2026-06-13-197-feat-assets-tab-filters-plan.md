---
status: active
execution: code
phase: "10"
program: meshy-parity
---

# Assets tab search and phase filters (Phase 10)

## Problem

The Assets tab reopens history but lacks Meshy-style search and phase filtering. Users cannot narrow runs by modality or query text.

## Scope

**In:**
- `input_modality` on `RunStore.list_runs` summaries.
- Pure filter/group helpers in `workspace_ui.py`.
- Assets tab search box, phase dropdown, grouped gallery HTML.
- Wire filter changes to history radio choices + overview + gallery.
- Tests + PARITY-MATRIX bump.

**Out:** Cross-tab filter persistence, hosted redeploy, full Meshy asset CDN parity.

## Files

- `src/imageezgen3d/storage.py`
- `src/imageezgen3d/workspace_ui.py`
- `app.py`
- `tests/test_workspace_ui.py`
- `tests/test_storage.py`
- `tests/test_app.py`
- `docs/reference/meshy/PARITY-MATRIX.md`

## Verification

- `PYTHONPATH=src python -m pytest tests/test_workspace_ui.py tests/test_storage.py tests/test_app.py -q`
- `PYTHONPATH=src python scripts/verify_meshy_parity_bundle.py`
