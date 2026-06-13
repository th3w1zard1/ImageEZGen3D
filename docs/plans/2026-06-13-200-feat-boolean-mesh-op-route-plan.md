---
status: active
execution: code
phase: "13"
program: meshy-parity
---

# Boolean mesh-op job route (Phase 13)

## Scope

- Add `second_mesh_path` and boolean modalities (`boolean-union`, `boolean-difference`, `boolean-intersection`) to the job stack.
- Wire `mesh_ops/booleans.py` through `mesh_op_runner.py`, `JobService` validation, and `build_mesh_op_job_request`.
- Update credits estimate, workspace `MESH_OP_MODALITIES`, and `PARITY-MATRIX.md`.

## Out of scope

- Gradio viewer buttons (two-mesh picker UX deferred).
- Meshy HTTP API route (no Meshy boolean endpoint; local job modality only).

## Verification

- `PYTHONPATH=src python scripts/verify_meshy_parity_bundle.py`
- `pytest tests/test_mesh_op_runner.py tests/test_gradio_mesh_op_bridge.py tests/test_credits.py`
