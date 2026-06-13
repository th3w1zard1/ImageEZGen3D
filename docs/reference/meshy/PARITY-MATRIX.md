# Meshy Parity Matrix

Maps each Meshy capability to the ImageEZGen3D module that implements it locally.
Updated after Meshy Parity program Phases U–7 (2026-06-13).

Status values:

- **real** — genuine CPU implementation with job/API or export path
- **demo** — functional stand-in adapter with honest disclaimer metadata
- **partial** — library or UI surface exists; job route or Gradio action not fully wired
- **gated** — neural path implemented but disabled behind admission gates (G1–G8)
- **stub** — documented/UI-only affordance without job wiring

| Meshy capability | Meshy credits | ImageEZGen3D module | Status |
| --- | --- | --- | --- |
| Text to 3D (preview/refine) | 20 + 10 | `adapters/text_demo.py`, `adapters/text_neural.py`, lanes in `generation_pipeline.py` | demo (`text_neural` **gated**) |
| Image to 3D | 20–30 | `adapters/cpu_demo.py`, `adapters/hunyuan.py` | demo (`hunyuan` **gated**) |
| Multi-Image to 3D | 20–30 | `view_image_paths` on `JobRequest`, orchestrator multi-view intake | **partial** (fusion hook; no dedicated Meshy route label) |
| Remesh | 5 | `mesh_ops/remesh.py`, `jobs/mesh_op_runner.py`, `meshy_api` `/openapi/v1/remesh` | **real** (job + API; viewer chip **stub**) |
| Convert (GLB/FBX/OBJ/STL/USDZ/BLEND/3MF) | 1 | `delivery_exports.py`, `mesh_ops/convert.py`, mesh-op jobs | **real** |
| Resize (height / longest-side / auto) | 1 | `mesh_ops/resize.py`, mesh-op jobs | **real** |
| Retexture (text/image prompt) | 10 | `adapters/retexture_demo.py`, `input_modality=retexture` | **demo** |
| Auto-Rigging | 5 | `adapters/rigging_demo.py` | **demo** |
| Animation (preset catalog) | 3 | `adapters/animation_demo.py`, `docs/reference/meshy/animation-library.json` | **demo** |
| Text to Image | 3–9 | `adapters/text_to_image_demo.py` | **demo** |
| Image to Image | 3–12 | `adapters/image_to_image_demo.py` | **demo** |
| Multi-Color Print (3MF) | 10 | `delivery_exports.py` (3MF export) | **partial** (export only; no multi-color print task) |
| Analyze Printability | free | `mesh_ops/printability.py` (analyze), mesh-op jobs | **real** |
| Repair Printability | 10 | `mesh_ops/printability.py` (repair), mesh-op jobs | **real** |
| Creative Lab — Keychain | 6 + 20 | `adapters/creative_lab.py` | **demo** |
| Creative Lab — Fridge Magnet | 6 + 20 | `adapters/creative_lab.py` | **demo** |
| Creative Lab — Figure | 6 + 20 | `adapters/creative_lab.py` | **demo** |
| Creative Lab — Lamp | 6 + 30 | `adapters/creative_lab.py` | **demo** |
| Async task model (poll) | — | `jobs/` file-backed queue | **real** |
| SSE streaming (`/:id/stream`) | — | `jobs/meshy_api.py` | **real** |
| Webhooks | — | `jobs/webhooks.py` | **real** |
| Task lifecycle (PENDING/IN_PROGRESS/SUCCEEDED/FAILED/CANCELED) | — | `jobs/models.py`, `meshy_api.py` | **real** |
| Balance endpoint | — | `jobs/meshy_api.py`, `credits.informational_balance_starting()` | **real** (informational) |
| Pricing / credits in UI + manifests | — | `credits.py`, `manifest_ui.py`, `workspace_ui.credit_footer_html` | **real** (informational) |
| PBR maps (`enable_pbr`) | — | `pbr_map_exports.py` | **real** (reference-grade maps) |
| Gradio workspace (Model/Image/Print/Animate/Assets) | — | `app.py`, `workspace_ui.py` | **real** (Phase 6) |
| Model Helper + bear-warrior preset | — | `workspace_ui.py` | **real** |
| Viewer action bar (Retry, Remesh, UV, …) | — | `app.py`, `workspace_ui.py` | **partial** (Remesh, print analyze/repair, UV unwrap, Edit Texture wired; Retry/Download/Send-* stub) |
| Assets gallery (search, phase filters) | — | `app.py`, `workspace_ui.py` | **real** (search, phase filters, grouped gallery; reopen via Open Run) |

Beyond-Meshy extras (Blender-parity):

| Capability | Module | Status |
| --- | --- | --- |
| Boolean union/difference/intersect | `mesh_ops/booleans.py` | **partial** (library only; no mesh-op job route) |
| UV unwrap | `mesh_ops/uv.py`, `jobs/mesh_op_runner.py` | **real** (mesh-op job + viewer button; needs xatlas) |

## Verification

After Meshy-facing changes, run:

```bash
PYTHONPATH=src python scripts/verify_meshy_parity_bundle.py
```

Hosted re-attestation: `scripts/hosted_golden_smoke.py` + Space deploy per `AGENTS.md`. See Phase 7 notes in `docs/knowledgebase/40-operational-risk/hosted-validation-2026-05-23.md`.

## Out of scope (by design)

- Runtime calls to Meshy API (local reimplementation only)
- Real neural generation until Hunyuan / neural adapters pass admission gates G1–G8
