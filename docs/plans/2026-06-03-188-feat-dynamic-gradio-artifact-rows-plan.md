---
title: "feat: Dynamic Gradio artifact rows from export config (Phase P-UI)"
type: feat
status: completed
date: 2026-06-03
origin: docs/plans/2026-06-03-185-feat-meshy-parity-gap-program-plan.md
---

# feat: Dynamic Grigrado artifact rows from export config (Phase P-UI)

## Summary

Drive Create and History download slots from `exports.formats` via a shared layout module so new delivery formats (e.g. 3MF) appear in Gradio without hand-wiring each `gr.File` and brittle output-index tests. Centralize generate output indices for hosted smoke.

---

## Problem Frame

Plans 180–187 added FBX, USDZ, and 3MF exports but Gradio still hard-codes per-format `gr.File` widgets and `run_generate` return tuples. Each new format requires `app.py`, `test_app.py`, and `hosted_golden_smoke.py` index churn. Phase Q landed 3MF without a UI slot.

---

## Requirements

- R1. **Layout module** — `gradio_artifact_layout.py` resolves download keys, row layout, labels, and generate output indices from config formats.
- R2. **Dynamic Create UI** — Build artifact `gr.File` rows from layout; include 3MF when configured.
- R3. **Dynamic History UI** — Mirror Create keys on History artifact panel.
- R4. **Handler wiring** — `run_generate` / `open_history_run` / error paths return artifact paths via layout helpers.
- R5. **Hosted smoke indices** — Import indices from layout module; extend delivery validation for 3MF when sidecar declares it.
- R6. **Tests** — Unit tests for layout; update app/smoke contract tests.

---

## Key Technical Decisions

- **Fixed prefix/suffix, dynamic delivery middle** — manifest→stl fixed; fbx/usdz/3mf from config; export_sidecar/raw_glb/bundle fixed tail.
- **BLEND excluded from UI** — No download widget; sidecar honesty only (Phase Q).
- **Component naming** — `3mf` maps to `threemf_file` / `history_threemf` (invalid Python identifier otherwise).
- **Backend rail index** — `create_history_summary` index computed from artifact count (fixes drift when slots added).

---

## Implementation Units

### U1. gradio_artifact_layout module

**Files:** `src/imageezgen3d/gradio_artifact_layout.py` (create)

**Test scenarios:** Default config includes 3mf slot; blend absent; indices monotonic.

### U2. app.py refactor

**Files:** `app.py`

**Dependencies:** U1

### U3. hosted_golden_smoke + tests

**Files:** `hosted_golden_smoke.py`, `tests/test_gradio_artifact_layout.py`, `tests/test_app.py`, `tests/test_hosted_golden_smoke.py`

**Dependencies:** U2

---

## Scope Boundaries

- Gradio Model3D preview path unchanged
- Job API payload format keys (Phase R deferred)

---

## Sources & Research

- Plan 185 Phase P-UI
- `app.py` generate.click outputs
- `pyproject.toml` `[tool.imageezgen3d.exports].formats`
