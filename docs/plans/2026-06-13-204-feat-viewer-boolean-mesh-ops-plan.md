---
status: active
execution: code
phase: "17"
program: meshy-parity
---

# Viewer boolean mesh-op UX (Phase 17)

## Scope

- Add second-mesh file picker and Union / Difference / Intersect viewer buttons.
- Wire `run_viewer_boolean_mesh_op` through `build_mesh_op_job_request(..., second_mesh_path=…)`.
- Register boolean actions in `WIRED_VIEWER_BOOLEAN_OPS` and refresh PARITY-MATRIX.

## Out of scope

- Meshy HTTP API route (no Meshy boolean endpoint).
- Hosted Space re-attestation.

## Verification

- `PYTHONPATH=src python scripts/verify_meshy_parity_bundle.py`
- `pytest tests/test_app.py tests/test_workspace_ui.py tests/test_gradio_mesh_op_bridge.py -q`
