---
title: "feat: 3MF delivery export + honest BLEND deferral (Phase Q)"
type: feat
status: completed
date: 2026-06-03
origin: docs/plans/2026-06-03-185-feat-meshy-parity-gap-program-plan.md
---

# feat: 3MF delivery export + honest BLEND deferral (Phase Q)

## Summary

Add pure-Python **3MF** mesh delivery export for print-oriented workflows and record **BLEND** as an honestly unavailable delivery tier in the export sidecar until a Blender runtime path exists. Extends the Plan 180 delivery export pattern without new Gradio slots (deferred to Phase P-UI).

---

## Problem Frame

Meshy exports seven production formats including **3MF** (modern print) and **BLEND** (Blender-native). ImageEZGen3D ships GLB/OBJ/PLY/STL/FBX/USDZ but lacks 3MF and cannot truthfully emit native `.blend` without Blender. Creators targeting slicers expect 3MF; sidecar must not imply BLEND parity when no writer exists.

---

## Requirements

- R1. **3MF writer** — ZIP-packaged 3MF core XML triangle mesh from `SimpleMesh`.
- R2. **Config wiring** — Add `3mf` to default `exports.formats`; wire through `export_all()` and sidecar `delivery_formats`.
- R3. **BLEND honesty** — When `blend` is requested, sidecar records `available: false` with explicit notes; no fake `.blend` path.
- R4. **Mesh checks** — Record `3mf_bytes`; validate ZIP magic for 3MF packages.
- R5. **Tests** — Unit tests for 3MF writer, export_all wiring, sidecar blocks, manifest validation.
- R6. **Docs** — Update export-guide; note BLEND deferral.

---

## Key Technical Decisions

- **3MF via pure Python** — ZIP + 3D/3dmodel.model XML; no new pip dependency on Space.
- **BLEND deferred, not stubbed** — Native BLEND requires Blender/bpy; sidecar honesty matches USDZ-without-usd-core pattern.
- **Gradio slots deferred** — Manifest/ZIP carry 3MF; UI download rows remain Phase P-UI.
- **Golden/hosted smoke unchanged** — 3MF not added to golden required keys this slice.

---

## Implementation Units

### U1. 3MF writer + BLEND sidecar honesty

**Goal:** Implement `write_3mf()` and extend `DELIVERY_FORMATS` / `build_delivery_formats_block`.

**Requirements:** R1, R3

**Files:**
- `src/imageezgen3d/delivery_exports.py` (modify)

**Test scenarios:**
- 3MF output is ZIP (`PK` magic) containing `3D/3dmodel.model`.
- Sidecar lists `blend.available=false` when blend in requested formats.

### U2. export_all + mesh_checks + config

**Goal:** Wire 3MF through export pipeline.

**Requirements:** R2, R4

**Dependencies:** U1

**Files:**
- `src/imageezgen3d/exporters.py` (modify)
- `src/imageezgen3d/mesh_checks.py` (modify)
- `pyproject.toml` (modify)

### U3. Tests and docs

**Requirements:** R5, R6

**Dependencies:** U2

**Files:**
- `tests/test_delivery_exports.py` (modify)
- `docs/knowledgebase/export-guide.md` (modify)
- `docs/plans/2026-06-03-185-feat-meshy-parity-gap-program-plan.md` (update phase table)

---

## Scope Boundaries

- Gradio 3MF/BLEND download slots (Phase P-UI)
- Golden sample 3MF required keys (deferred)
- Blender subprocess / bpy integration for BLEND (future)

---

## Sources & Research

- Meshy API `target_formats` includes `3mf`; BLEND in product marketing
- `src/imageezgen3d/delivery_exports.py` — FBX/USDZ pattern
- Plan 185 Phase Q
