---
title: "feat: retexture adapter hook (Phase U)"
type: feat
status: completed
date: 2026-06-03
origin: docs/plans/2026-06-03-185-feat-meshy-parity-gap-program-plan.md
---

# feat: retexture adapter hook (Phase U)

## Summary

Add Meshy-style **retexture** task wiring: `input_modality=retexture` on jobs and orchestrator, optional `texture_image_path` / `source_mesh_path` payload fields, and a `retexture-demo` adapter that exports reference PBR maps from a texture image with honest stand-in geometry.

---

## Problem Frame

Phase S landed reference PBR map export; Phase T added preview/refine lanes. Meshy also exposes retexture tasks (`texture_image_url` on existing mesh). ImageEZGen3D had no automation surface for retexture-only workflows.

---

## Requirements

- R1. **Modality** — Extend pipeline spec with `input_modality: retexture`.
- R2. **Job payload** — `texture_image_path` and optional `source_mesh_path` on `JobRequest`.
- R3. **retexture-demo adapter** — Reference-image PBR pack + stand-in mesh; honest disclaimer.
- R4. **Orchestrator routing** — Select `retexture-demo`, preprocess texture intake, stage shape skipped / texture succeeded.
- R5. **Validation** — Retexture jobs require texture image path; source mesh validated when provided.
- R6. **Tests** — Pipeline, job, and adapter integration coverage.

---

## Out of Scope

- Neural UV unwrap / paint on arbitrary GLB
- Gradio retexture UI panel
- Hosted smoke retexture attestation
