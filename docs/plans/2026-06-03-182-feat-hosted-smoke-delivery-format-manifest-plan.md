---
title: "feat: hosted smoke delivery format manifest validation (Plan 180 follow-up)"
type: feat
status: completed
date: 2026-06-03
origin: docs/plans/2026-06-03-180-feat-meshy-fbx-usdz-delivery-exports-plan.md
---

# feat: hosted smoke delivery format manifest validation (Plan 180 follow-up)

## Summary

Fix hosted smoke Gradio `/generate` artifact index drift after FBX/USDZ UI slots landed, and validate optional delivery format consistency between manifest artifacts and export sidecar `delivery_formats` metadata.

---

## Problem Frame

Plan 180 added FBX/USDZ exports; Plan 181 inserted two Gradio outputs before export sidecar, but `hosted_golden_smoke.py` still reads sidecar at index 7 (now FBX). Plan 180 also deferred hosted smoke checks for delivery formats.

---

## Requirements

- R1. **Index fix** — Update `_GENERATE_EXPORT_SIDECAR_INDEX` (and document artifact indices) to match `app.py` generate outputs after FBX/USDZ slots.
- R2. **Delivery validation** — When export sidecar is available, verify `delivery_formats` ↔ manifest artifact keys and on-disk files for exported FBX/USDZ.
- R3. **Backward compatible** — Missing `delivery_formats` on legacy sidecars produces no new failures.
- R4. **Tests** — Unit tests for validation helpers and index contract against `app.py`.

---

## Key Technical Decisions

- **Optional formats stay optional in golden required keys** — Validation runs when sidecar declares `delivery_formats`; does not add FBX/USDZ to `REQUIRED_ARTIFACT_KEYS`.
- **Resolve sidecar from manifest** — `validate_run_manifest` loads sidecar from `sidecar_path` or manifest `artifacts.export_sidecar` path when readable.

---

## Implementation Units

### U1. Delivery format manifest validator

**Files:** `src/imageezgen3d/delivery_exports.py`, `src/imageezgen3d/hosted_golden_smoke.py`

**Test scenarios:** exported=true requires artifact key + file; exported=false forbids artifact key; legacy sidecar without block passes.

### U2. Generate output index fix + contract test

**Files:** `src/imageezgen3d/hosted_golden_smoke.py`, `tests/test_hosted_golden_smoke.py`

**Test scenarios:** Sidecar index is 9 in generate.click outputs; export_sidecar appears after fbx/usdz.

### U3. Manifest validation integration tests

**Files:** `tests/test_hosted_export_tier_smoke.py`

**Verification:** Full unittest suite green; CI green.

---

## Scope Boundaries

- Golden sample required-key expansion (deferred)
- Space `requirements.txt` usd-core opt-in (deferred)

---

## Sources & Research

- `docs/plans/2026-06-03-180-feat-meshy-fbx-usdz-delivery-exports-plan.md`
- `docs/plans/2026-06-03-181-feat-meshy-fbx-usdz-gradio-downloads-plan.md`
- `src/imageezgen3d/hosted_golden_smoke.py` — `validate_run_manifest`
