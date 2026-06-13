---
status: completed
execution: code
phase: "6"
program: meshy-parity
---

# Meshy-style Gradio workspace UI (Phase 6)

## Problem

Phase Z landed informational credits. Phase 6 reworks `app.py` toward the Meshy workspace: Model/Image/Print/Animate/Assets tabs, credit footer, viewer extras (stats, PBR strip, action bar), and Model Helper with bear-warrior preset.

## Scope

**In:** `workspace_ui.py`, `app.py` tab rail + wiring, CSS, tests.

**Out:** Full job wiring for viewer action chips, hosted Space deploy (Phase 7), plan file edits.

## Implementation units

1. **`src/imageezgen3d/workspace_ui.py`** — credit footer, model helper, PBR strip (filename labels), mesh stats, viewer action bar.
2. **`app.py`** — Model/Image/Print/Animate/Assets tabs; credit footer; preview extras on generate; history inspect extras; bear preset; CSS.
3. **`tests/test_workspace_ui.py`** — unit tests for workspace helpers.
4. **`tests/test_app.py`** — update tab name assertions (Model/Assets).

## Test scenarios

- Credit footer renders consumed credits for image draft and text production lanes.
- PBR strip shows channel labels and basenames when maps present.
- `_history_inspect_html` includes mesh-stats and viewer-action sections.
- App source exposes Model tab composer before starter cards and Assets tab artifact downloads.

## Verification

- `PYTHONPATH=src python -m pytest tests/test_workspace_ui.py tests/test_app.py -q`
- `ruff check app.py src/imageezgen3d/workspace_ui.py`
- `PYTHONPATH=src python scripts/check_python_style.py`
