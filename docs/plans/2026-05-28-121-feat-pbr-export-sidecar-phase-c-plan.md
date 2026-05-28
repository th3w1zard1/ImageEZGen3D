---
title: "feat: PBR delivery sidecar contract (Phase C metallic-roughness slots)"
type: feat
status: completed
date: 2026-05-28
origin: docs/plans/2026-05-28-119-feat-meshy-class-platform-foundation-plan.md
---

# feat: PBR delivery sidecar contract (Phase C metallic-roughness slots)

## Summary

Add an industry-aligned **PBR delivery block** to export sidecars and wire the manifest `pbr` pipeline stage from sidecar truth — without claiming textured map packs until Hunyuan paint lands. Keeps cpu-demo/text-demo honest (factor-only GLB) while giving downstream tools stable map slots.

---

## Requirements

- R1. Export sidecar includes `pbr_delivery` with metallic-roughness workflow and map slot paths (null when absent).
- R2. `pbr_available: false` for factor-only adapters; notes explain embedded GLB factors.
- R3. Orchestrator sets manifest `pbr` stage from sidecar after export validation.
- R4. Tests cover sidecar schema and pipeline stage outcomes.
- R5. Export guide documents the sidecar block.

---

## Scope Boundaries

- FBX/USDZ exporters (deferred)
- Actual texture map file generation
- Enabling Hunyuan on Space

---

## Implementation Units

- U1. `build_pbr_delivery_block` + extend `build_export_sidecar`
- U2. Orchestrator `pbr` stage from sidecar
- U3. Tests + export-guide update

---

## Key Technical Decisions

- Map slots: `base_color`, `normal`, `metallic_roughness`, `ao` (paths or null).
- `pbr` stage `succeeded` only when `pbr_available` and map paths present; else `skipped` with explicit note.
