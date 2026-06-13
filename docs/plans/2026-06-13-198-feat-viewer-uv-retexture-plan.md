---
status: active
execution: code
phase: "11"
program: meshy-parity
---

# Wire viewer UV unwrap and Edit Texture actions (Phase 11)

## Problem

Remesh and print mesh-ops are wired; **Unwrap UV** and **Edit Texture** remain stub chips despite library and retexture job support.

## Scope

**In:**
- `unwrap-uv` mesh-op modality in `mesh_op_runner` + job service + credits.
- Gradio **Unwrap UV** and **Edit Texture** buttons queue jobs from preview session model.
- Shared queued-run completion helper in `app.py`.
- Tests + PARITY-MATRIX updates.

**Out:** Retry, Download, Send to Print/Animate tab routing, Meshy HTTP route for UV.

## Verification

- `PYTHONPATH=src python scripts/verify_meshy_parity_bundle.py`
- `PYTHONPATH=src python -m pytest tests/test_mesh_op_runner.py tests/test_gradio_mesh_op_bridge.py tests/test_workspace_ui.py tests/test_app.py -q`
