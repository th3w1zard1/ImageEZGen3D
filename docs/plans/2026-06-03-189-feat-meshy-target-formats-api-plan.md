---
title: "feat: target_formats on job payload and export API (Phase R)"
type: feat
status: active
date: 2026-06-03
origin: docs/plans/2026-06-03-185-feat-meshy-parity-gap-program-plan.md
---

# feat: target_formats on job payload and export API (Phase R)

## Summary

Add Meshy-style `target_formats` to automation job requests so clients can request a subset of configured delivery formats. Resolve against deployment config, record resolved formats in run manifests, and thread through orchestrator → adapters → `export_all()`.

---

## Problem Frame

`export_all()` already accepts a `formats` tuple, but adapters always pass `load_config().exports.formats`. Automation clients (HTTP job API, JSONL batch) cannot request format subsets like Meshy's `target_formats`. Phase Q landed 3MF/BLEND sidecar honesty; Phase R closes the API parity gap without new writers.

---

## Requirements

- R1. **JobRequest field** — Optional `target_formats: list[str]` on job payload (Meshy API name).
- R2. **Resolution helper** — `resolve_target_export_formats()` validates tokens, rejects unknown/disabled formats, preserves caller order.
- R3. **Orchestrator threading** — Accept `target_formats`, resolve to `export_formats`, store both in manifest parameters, pass to `GenerationRequest`.
- R4. **Adapter wiring** — cpu-demo, text-demo, and Hunyuan finalize path use `request.export_formats` instead of reloading config.
- R5. **Early validation** — Invalid `target_formats` fail at job submit (HTTP 400) before queue execution.
- R6. **Tests** — Unit tests for resolver; job + HTTP integration proving subset export and error paths.

---

## Key Technical Decisions

- **Configured ceiling** — `target_formats` must be a subset of `config.exports.formats`; requesting disabled formats raises `ValueError`.
- **GLB not forced** — Caller may request delivery-only subsets (e.g. `fbx` only); sidecar still records honest delivery metadata.
- **Manifest keys** — `parameters.target_formats` (request) and `parameters.export_formats` (resolved tuple used for export).
- **Backward compatible** — Omitting `target_formats` preserves full config export set.

---

## Implementation Units

### U1. resolve_target_export_formats

**Files:** `src/imageezgen3d/delivery_exports.py`

### U2. JobRequest + JobService validation

**Files:** `src/imageezgen3d/jobs/models.py`, `src/imageezgen3d/jobs/service.py`

### U3. Orchestrator + GenerationRequest

**Files:** `src/imageezgen3d/orchestrator.py`, `src/imageezgen3d/adapters/base.py`, adapters, `hunyuan_inference.py`

### U4. Tests + program index update

**Files:** `tests/test_delivery_exports.py`, `tests/test_jobs.py`, `tests/test_jobs_http_api.py`, gap program plan

---

## Out of Scope

- Gradio UI format picker (config-driven UI remains full set)
- Public hosted REST hardening (Phase Y)
- BLEND writer (Phase Q deferral unchanged)
