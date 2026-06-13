---
status: completed
execution: code
phase: "9"
program: meshy-parity
---

# Wire viewer mesh-op actions (Phase 9)

## Problem

Phase 6 shipped viewer action labels as static HTML chips. Remesh and printability mesh-op jobs exist in `mesh_op_runner` but the Gradio preview panel cannot queue them from the current model.

## Scope

**In:**
- Gradio buttons for Remesh, Analyze Print, Repair Print using preview session `model` path as `mesh_input_path`.
- Shared job-queue completion path updating preview, status, artifacts, history.
- `gradio_bridge.build_mesh_op_job_request`, tests, PARITY-MATRIX status bump.

**Out:** Retexture/UV/Download/Send-to-* wiring, hosted redeploy (unless needed for validation).

## Files

- `src/imageezgen3d/jobs/gradio_bridge.py`
- `src/imageezgen3d/workspace_ui.py`
- `app.py`
- `tests/test_gradio_mesh_op_bridge.py`
- `tests/test_workspace_ui.py`
- `docs/reference/meshy/PARITY-MATRIX.md`

## Verification

- `PYTHONPATH=src python -m pytest tests/test_gradio_mesh_op_bridge.py tests/test_workspace_ui.py tests/test_app.py -q`
- `PYTHONPATH=src python scripts/verify_meshy_parity_bundle.py`
