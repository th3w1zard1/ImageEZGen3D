---
status: completed
execution: code
phase: "16"
program: meshy-parity
---

# Viewer Multi-Color 3MF button (Phase 16)

## Scope

- Add **Multi-Color 3MF** viewer button wired to `run_viewer_mesh_op("print-multi-color", …)`.
- Register action in `WIRED_VIEWER_MESH_OPS` and refresh Print lane copy.
- Extend Gradio bridge / app wiring tests for the new button.

## Out of scope

- Hosted Space re-attestation.
- Boolean two-mesh picker UX.

## Verification

- `PYTHONPATH=src python scripts/verify_meshy_parity_bundle.py`
- `pytest tests/test_app.py tests/test_workspace_ui.py tests/test_gradio_mesh_op_bridge.py -q`
