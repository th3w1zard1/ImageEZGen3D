---
status: active
execution: code
phase: "15"
program: meshy-parity
---

# Multi-color print job route (Phase 15)

## Scope

- Add `print-multi-color` mesh-op modality with `max_colors` / `max_depth` on `JobRequest`.
- Implement demo multi-color 3MF generation in `mesh_ops/multi_color_print.py` and `write_multi_color_3mf`.
- Wire Meshy-shaped route `POST /openapi/v1/print/multi-color` plus retrieve/stream.
- Update credits estimate (10 credits), `PARITY-MATRIX.md`, and workspace print modalities.

## Out of scope

- Hosted Space attestation (deferred since Phase 7).
- Gradio viewer button for multi-color print (API + job stack only).

## Verification

- `PYTHONPATH=src python scripts/verify_meshy_parity_bundle.py`
- `pytest tests/test_mesh_op_runner.py tests/test_meshy_http_api.py tests/test_credits.py -q`
