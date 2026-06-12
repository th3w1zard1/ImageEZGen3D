# Meshy Parity Matrix

Maps each Meshy capability to the ImageEZGen3D module that implements (or will
implement) it locally. Status values:

- **real** — genuine CPU implementation, same observable behavior class
- **demo** — functional stand-in adapter with honest disclaimer metadata; gated
  neural path documented for later enablement
- **planned (Phase N)** — scheduled in the parity program, not yet landed
- **gated** — implemented behind admission gates (G1–G8), disabled by default

| Meshy capability | Meshy credits | ImageEZGen3D module | Status |
| --- | --- | --- | --- |
| Text to 3D (preview/refine) | 20 + 10 | `adapters/text_demo.py`, `adapters/text_neural.py`, preview/refine lanes in `generation_pipeline.py` | demo (neural gated) |
| Image to 3D | 20–30 | `adapters/cpu_demo.py`, `adapters/hunyuan.py` | demo (Hunyuan gated) |
| Multi-Image to 3D | 20–30 | `view_image_paths` job field; fusion hook | planned (Phase 3) |
| Remesh | 5 | `mesh_ops/remesh.py` (+ existing `mesh_decimation.py`) | planned (Phase 2) |
| Convert (GLB/FBX/OBJ/STL/USDZ/BLEND/3MF) | 1 | `delivery_exports.py`, `mesh_ops/convert.py` | real (exports landed; task surface planned Phase 2) |
| Resize (height / longest-side / auto) | 1 | `mesh_ops/resize.py` | planned (Phase 2) |
| Retexture (text/image prompt) | 10 | `adapters/retexture_demo.py`, `input_modality=retexture` | demo (Phase U landed) |
| Auto-Rigging | 5 | `adapters/rigging_demo.py` | planned (Phase 3) |
| Animation (preset catalog) | 3 | `adapters/animation_demo.py` + [animation-library.json](animation-library.json) | planned (Phase 3) |
| Text to Image | 3–9 | `adapters/text_to_image_demo.py` | planned (Phase 3) |
| Image to Image | 3–12 | `adapters/image_to_image_demo.py` | planned (Phase 3) |
| Multi-Color Print (3MF) | 10 | 3MF export landed (`delivery_exports.py`); multi-color task | planned (Phase 3) |
| Analyze Printability | free | `mesh_ops/printability.py` (analyze) | planned (Phase 2) |
| Repair Printability | 10 | `mesh_ops/printability.py` (repair) | planned (Phase 2) |
| Creative Lab — Keychain | 6 + 20 | `adapters/creative_lab.py` (depth-relief) | planned (Phase 3) |
| Creative Lab — Fridge Magnet | 6 + 20 | `adapters/creative_lab.py` | planned (Phase 3) |
| Creative Lab — Figure | 6 + 20 | `adapters/creative_lab.py` | planned (Phase 3) |
| Creative Lab — Lamp | 6 + 30 | `adapters/creative_lab.py` | planned (Phase 3) |
| Async task model (poll) | — | `jobs/` (file-backed queue, poll API) | real |
| SSE streaming (`/:id/stream`) | — | `jobs/http_api.py` | planned (Phase 4) |
| Webhooks | — | `jobs/webhooks.py` | real (payload alignment planned Phase 4) |
| Task lifecycle (PENDING/IN_PROGRESS/SUCCEEDED/FAILED/CANCELED) | — | `jobs/models.py` status mapping | planned (Phase 4) |
| Balance endpoint | — | `jobs/http_api.py` + `credits.py` ledger | planned (Phases 4–5) |
| Pricing / credits | — | `credits.py` (informational ledger from [pricing.md](pricing.md)) | planned (Phase 5) |
| PBR maps (`enable_pbr`) | — | `pbr_map_exports.py` (reference maps) | real (reference-grade) |

Beyond-Meshy extras (Blender-parity, Phase 2): boolean union/difference/
intersect (`mesh_ops/booleans.py`) and UV unwrap (`mesh_ops/uv.py`).
