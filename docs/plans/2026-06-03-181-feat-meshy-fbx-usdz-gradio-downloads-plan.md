---
title: "feat: Gradio FBX/USDZ download slots (Plan 180 follow-up)"
type: feat
status: completed
date: 2026-06-03
origin: docs/plans/2026-06-03-180-feat-meshy-fbx-usdz-delivery-exports-plan.md
---

# feat: Gradio FBX/USDZ download slots (Plan 180 follow-up)

## Summary

Expose FBX and USDZ delivery exports in the Create and History Gradio artifact panels, wiring verified download outputs through `generate.click` and `history_open.click` with matching `test_app.py` ordering contracts.

---

## Problem Frame

Plan 180 landed FBX/USDZ writers and manifest/ZIP artifacts but deferred dedicated Gradio download slots to avoid brittle output-order churn. Creators still cannot download FBX/USDZ from the UI without opening the ZIP bundle.

---

## Requirements

- R1. **Create tab** — Add `gr.File` components labeled FBX and USDZ after STL, before export sidecar.
- R2. **History tab** — Mirror FBX/USDZ download slots in history artifacts panel.
- R3. **Generate wiring** — `run_generate` and error/stale paths populate FBX/USDZ from verified artifacts; session state stores keys.
- R4. **History open** — `open_history_run` returns verified FBX/USDZ paths when present.
- R5. **Tests** — Extend `test_create_and_history_tabs_expose_export_tier_downloads` for labels and output ordering (STL → FBX → USDZ → export sidecar → RAW GLB → bundle).

---

## Key Technical Decisions

- **Ordering matches export tier sequence** — STL, then FBX, USDZ, then sidecar/RAW/bundle; keeps mesh formats grouped before metadata exports.
- **Optional artifacts stay verified-only** — Missing FBX/USDZ (e.g. usd-core absent on Space) yield `None` via existing `_verified_artifact_state`; no fake paths.
- **No golden/smoke changes** — Required keys unchanged in this slice.

---

## Implementation Units

### U1. Gradio UI components

**Goal:** Add FBX/USDZ file widgets on Create and History tabs.

**Files:** `app.py`

**Test scenarios:** Source scan finds `label="FBX"` and `label="USDZ"` in both Create and History sections.

### U2. Handler and click wiring

**Goal:** Thread fbx/usdz through generate, history open, and session state.

**Files:** `app.py`

**Test scenarios:** Output order test passes; verified artifact filtering unchanged for missing optional keys.

### U3. App contract tests

**Goal:** Lock ordering and label contracts.

**Files:** `tests/test_app.py`

**Verification:** `tests/test_app.py` green; full suite green.

---

## Scope Boundaries

- Space `requirements.txt` usd-core opt-in (deferred)
- Hosted smoke manifest expansion (deferred)
- Dynamic artifact row generation from config (deferred — explicit slots for now)

---

## Sources & Research

- `docs/plans/2026-06-03-180-feat-meshy-fbx-usdz-delivery-exports-plan.md` — deferred UI follow-up
- `app.py` — existing artifact row pattern
- `tests/test_app.py` — generate.click ordering contract
