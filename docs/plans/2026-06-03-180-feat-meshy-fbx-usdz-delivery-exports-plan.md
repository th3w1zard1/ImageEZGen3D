---
title: "feat: FBX/USDZ delivery exports (Plan 119 U-follow-5)"
type: feat
status: completed
date: 2026-06-03
origin: docs/plans/2026-05-28-119-feat-meshy-class-platform-foundation-plan.md
---

# feat: FBX/USDZ delivery exports (Plan 119 U-follow-5)

## Summary

Add optional FBX and USDZ mesh delivery exports alongside existing GLB/OBJ/PLY/STL writers, wire `config.exports.formats`, and record honest delivery metadata in the export sidecar. GLB remains the canonical PBR carrier; FBX/USDZ are geometry-first delivery tiers for DCC/game and iOS AR targets.

---

## Problem Frame

Plan 119 deferred FBX/USDZ until the PBR sidecar stabilized (Phase C landed). Meshy-class parity expects GLB + FBX + USDZ delivery formats. ImageEZGen3D today exports GLB/OBJ/PLY/STL from `export_all()` but `ExportSettings.formats` is unused. Creators targeting Unity/Unreal (FBX) or iOS AR Quick Look (USDZ) must manually convert GLB.

---

## Requirements

- R1. **FBX export** — Static mesh ASCII FBX written from `SimpleMesh` without claiming rig/animation/PBR map packaging.
- R2. **USDZ export** — Geometry-first USDZ via `usd-core` when the optional dependency is installed; skip gracefully when absent.
- R3. **Config-driven formats** — `export_all()` respects `load_config().exports.formats`; pyproject lists `fbx` and `usdz`.
- R4. **Sidecar honesty** — Export sidecar includes `delivery_formats` block documenting availability and material fidelity limits per format.
- R5. **Validation** — `inspect_artifacts()` records byte sizes; missing optional formats do not fail export stage when core GLB/OBJ pass.
- R6. **Tests** — Unit tests for FBX writer, USDZ when `usd-core` present (skip otherwise), config wiring, and sidecar block.
- R7. **Docs** — Brief `export-guide.md` section on FBX/USDZ fidelity limits.

---

## Key Technical Decisions

- **FBX via pure-Python ASCII writer**: trimesh lacks FBX without Assimp; a focused ASCII FBX 7.4 static-mesh writer avoids native deps and keeps Space builds lean.
- **USDZ via usd-core optional extra**: `UsdUtils.CreateNewUsdzPackage` from an intermediate USDA layer; gated behind `[mesh-delivery]` extra, not default Space `requirements.txt`.
- **Do not extend golden/smoke required keys**: FBX/USDZ remain optional manifest artifacts until Space-proven; ZIP bundle auto-includes files under run exports.
- **Defer Gradio download slots**: Manifest + ZIP carry new artifacts; dedicated `gr.File` rows deferred to avoid brittle output-order churn in `test_app.py`.

---

## Implementation Units

### U1. Delivery export writers

**Goal:** Add FBX ASCII and USDZ writers plus format availability probes.

**Files:**
- `src/imageezgen3d/delivery_exports.py` (create)
- `src/imageezgen3d/exporters.py` (modify)

**Approach:** `write_fbx()` emits FBX 7.4 ASCII triangle mesh; `write_usdz()` uses usd-core when importable. Extend `export_all()` with `formats` parameter filtering outputs.

**Test scenarios:**
- FBX output is non-empty and contains `FBXVersion` and `Geometry`.
- USDZ output is a ZIP (`PK` magic) when usd-core installed; skip test otherwise.
- `export_all(..., formats=("glb","fbx"))` omits obj/ply/stl.

**Verification:** Unit tests pass; FBX/USDZ files parseable at header level.

### U2. Sidecar delivery metadata + config wiring

**Goal:** Record honest delivery format metadata and wire adapters to config formats.

**Files:**
- `src/imageezgen3d/export_tiers.py` (modify)
- `src/imageezgen3d/adapters/cpu_demo.py` (modify)
- `src/imageezgen3d/adapters/text_demo.py` (modify)
- `src/imageezgen3d/config.py` (modify if needed)
- `pyproject.toml` (modify)

**Approach:** Add `build_delivery_formats_block()`; merge into sidecar before write. Adapters pass `load_config().exports.formats` to `export_all()`. Add `[mesh-delivery]` optional dep for `usd-core`.

**Test scenarios:**
- Sidecar includes `delivery_formats.fbx.available=true` when FBX exported.
- Sidecar notes state geometry-only / factor-only limits.
- Config `formats = ['glb','obj']` limits outputs.

**Verification:** `tests/test_export_tiers.py` extended; config test unchanged behavior for defaults.

### U3. Mesh checks, docs, CI extra

**Goal:** Basic artifact metrics for new formats; document limits; CI installs mesh-delivery for USDZ tests.

**Files:**
- `src/imageezgen3d/mesh_checks.py` (modify)
- `docs/knowledgebase/export-guide.md` (modify)
- `.github/workflows/ci.yml` (modify)
- `tests/test_delivery_exports.py` (create)

**Test scenarios:**
- `inspect_artifacts` records `fbx_bytes` / `usdz_bytes` when present.
- CI workflow installs `.[app,dev,mesh,mesh-delivery]`.

**Verification:** Full unittest suite green locally and in CI.

---

## Scope Boundaries

- Gradio dedicated FBX/USDZ download components (deferred)
- Golden sample / hosted smoke required-key expansion (deferred)
- Hunyuan neural path export parity (inherits shared `export_all` automatically when adapters call it)
- Rigged FBX, animation, or full PBR map packaging in FBX/USDZ

### Deferred to Follow-Up Work

- UI download slots + `test_app.py` output order update
- Space `requirements.txt` opt-in for `usd-core` after payload audit
- Hosted smoke manifest checks for optional delivery formats

---

## Sources & Research

- `docs/plans/2026-05-28-119-feat-meshy-class-platform-foundation-plan.md` — U-follow-5
- `docs/knowledgebase/competitive-product-benchmark-2026.md` — Tier 1 gap #3
- `src/imageezgen3d/exporters.py` — existing writer hub
- `docs/solutions/best-practices/meshy-class-automation-stack-2026-05-28.md` — trust boundaries
