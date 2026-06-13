---
title: "feat: preview/refine orchestrator lanes (Phase T)"
type: feat
status: completed
date: 2026-06-03
origin: docs/plans/2026-06-03-185-feat-meshy-parity-gap-program-plan.md
---

# feat: preview/refine orchestrator lanes (Phase T)

## Summary

Add Meshy-style **preview** and **refine** generation lanes to the orchestrator so automation clients can request a fast geometry-first pass or a full texture/PBR refine pass. Record honest pipeline stage progression and restrict preview exports to lightweight formats.

---

## Problem Frame

ImageEZGen3D today exposes `draft` and `production` lanes that differ mainly by quality/decimation but still run a single-pass export. Meshy separates preview mesh delivery from a slower refine/texture pass. Phase S landed reference PBR maps on demo adapters; Phase T adds explicit lane semantics without neural paint.

---

## Requirements

- R1. **Lane types** — Accept `preview` and `refine` alongside `draft`/`production` in pipeline spec resolution.
- R2. **Preview behavior** — GLB/OBJ subset exports, no PBR map files, texture/pbr stages skipped with refine guidance.
- R3. **Refine behavior** — Balanced default quality, full exports + reference PBR maps, texture stage succeeded before PBR sidecar application.
- R4. **Orchestrator stages** — Central `finalize_pipeline_stages_for_lane()` after adapter export validation.
- R5. **Job + Gradio parity** — Lane values pass through existing `lane` fields; manifest records `workflow_phase`.
- R6. **Tests** — Lane resolution, preview export subset, orchestrator stage outcomes for preview vs refine.

---

## Key Technical Decisions

- **Backward compatible** — `draft`/`production` keep legacy single-pass stage semantics.
- **No run chaining** — Refine lane is a standalone full pass; linking to prior preview run_id deferred.
- **Preview formats** — `glb` + `obj` when configured; honor explicit `target_formats` when set.

---

## Out of Scope

- Neural texture/refine adapters (Hunyuan paint)
- Gradio “refine this run” button wiring to parent run_id
- Hosted smoke required preview/refine attestation
