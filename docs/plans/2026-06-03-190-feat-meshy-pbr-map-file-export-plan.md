---
title: "feat: PBR map file export (Phase S)"
type: feat
status: completed
date: 2026-06-03
origin: docs/plans/2026-06-03-185-feat-meshy-parity-gap-program-plan.md
---

# feat: PBR map file export (Phase S)

## Summary

Export on-disk PBR texture maps (base color, normal, metallic-roughness, AO) for demo adapters and wire `pbr_delivery.pbr_available=true` in export sidecars so manifest `pbr` pipeline stages succeed when map files exist.

---

## Problem Frame

Phase C landed sidecar map slots with honest `pbr_available=false` for factor-only GLB. Meshy-class parity requires separate map files on disk, not metadata-only placeholders. Hunyuan neural paint is gated; this slice delivers a **reference map pack** from input-derived color so CI, jobs API, and bundle ZIPs prove the full PBR delivery contract.

---

## Requirements

- R1. **Map writers** — `pbr_map_exports.py` writes PNG maps under `exports/pbr/`.
- R2. **Sidecar truth** — `pbr_available=true` with relative map paths; honest notes (reference pack, not neural bake).
- R3. **Adapter wiring** — cpu-demo (image thumb), text-demo (procedural color), Hunyuan finalize (mesh embedded image).
- R4. **Manifest artifacts** — `pbr_*` keys recorded and included in run bundles.
- R5. **Pipeline stage** — orchestrator `pbr` stage `succeeded` when sidecar declares maps.
- R6. **Tests** — Unit tests for writers; update cpu-demo orchestrator expectations.

---

## Key Technical Decisions

- **Reference tier honesty** — Notes explicitly state maps are input-derived reference factors, not neural bakes.
- **Full quad pack** — Export all four slots; normal flat, default metallic-roughness, white AO.
- **Gradio deferral** — Map download rows omitted; maps ship in manifest + ZIP (same pattern as pre-P-UI delivery formats).

---

## Out of Scope

- Neural paint / Hunyuan texture tower outputs
- Gradio PBR map download widgets
- Hosted smoke required PBR keys (follow-on)
