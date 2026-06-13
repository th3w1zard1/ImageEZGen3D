---
status: active
execution: code
phase: "14"
program: meshy-parity
---

# Multi-Image to 3D route label (Phase 14)

## Scope

- Preserve `multi-image-to-3d` as a dedicated `input_modality` through pipeline, orchestrator, jobs, and Meshy HTTP translation.
- Parse Meshy `image_urls` arrays into staged `view_image_paths` + primary `image_path`.
- Auto-promote Gradio runs with labeled views from `image` to `multi-image-to-3d`.

## Out of scope

- Neural multi-view fusion beyond existing `fuse_multi_view_color` demo path.
- `input_task_id` chaining from prior 2D gen tasks.

## Verification

- `PYTHONPATH=src python scripts/verify_meshy_parity_bundle.py`
- `pytest tests/test_generation_pipeline.py tests/test_meshy_http_api.py tests/test_gradio_mesh_op_bridge.py`
