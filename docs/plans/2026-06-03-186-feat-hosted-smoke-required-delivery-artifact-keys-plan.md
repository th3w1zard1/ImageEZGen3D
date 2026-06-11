---
title: "feat: hosted smoke required delivery artifact keys (Phase O)"
type: feat
status: completed
date: 2026-06-03
origin: docs/plans/2026-06-03-185-feat-meshy-parity-gap-program-plan.md
---

# feat: hosted smoke required delivery artifact keys (Phase O)

## Summary

Extend hosted export-tier smoke manifest validation to require FBX (and USDZ when sidecar declares `usdz.available`) in manifest artifacts and on-disk files when `delivery_formats` is present, plus optional Gradio output path checks during live `/generate`.

---

## Problem Frame

Phase N tightened local golden-sample CI for FBX/USDZ. Hosted export-tier smoke (`validate_manifest=True`) still passes when manifest omits `fbx`/`usdz` unless sidecar `delivery_formats` claims export parity. Plan 183 added Space `usd-core`; hosted runs should now prove delivery tiers on live Space, not only sidecar consistency when keys happen to be present.

---

## Requirements

- R1. **Manifest required keys** — When export sidecar includes `delivery_formats`, require `fbx` in manifest artifacts with non-empty on-disk file.
- R2. **USDZ conditional** — When `delivery_formats.usdz.available` is true, require `usdz` artifact key and non-empty file.
- R3. **Legacy tolerance** — Sidecars without `delivery_formats` block produce no new failures.
- R4. **Gradio path checks** — When `validate_manifest=True`, verify non-empty FBX/USDZ paths in generate outputs when required.
- R5. **Tests** — Unit tests for required-key failures and legacy sidecar pass-through.

---

## Key Technical Decisions

- **Gate on `delivery_formats` presence** — Same backward-compat rule as Plan 182 parity validation.
- **USDZ keyed on sidecar `available`** — Reflects Space install contract without probing local `usd_core_available()` on CI runner.
- **Golden smoke script unchanged** — Export-tier smoke remains the manifest-validation path; golden smoke stays status-only unless later opted in.

---

## Implementation Units

### U1. Required delivery artifact validation

**Goal:** Enforce manifest FBX/USDZ keys when sidecar declares delivery formats.

**Requirements:** R1–R3

**Files:**
- `src/imageezgen3d/hosted_golden_smoke.py` (modify)

**Approach:** Add `_validate_required_delivery_artifact_keys()`; call from `validate_run_manifest` after loading sidecar when `delivery_formats` present.

**Test scenarios:**
- Sidecar with `delivery_formats.fbx.exported=true` and manifest missing `fbx` fails.
- Sidecar with `usdz.available=true` and missing `usdz` fails.
- Legacy sidecar without `delivery_formats` unchanged.

### U2. Gradio output path checks

**Goal:** Fail live smoke when generate outputs omit required delivery download paths.

**Requirements:** R4

**Dependencies:** U1

**Files:**
- `src/imageezgen3d/hosted_golden_smoke.py` (modify)

**Approach:** In `run_hosted_golden_smoke`, when `validate_manifest` and sidecar readable, assert indices 7/8 paths exist.

### U3. Tests and program index

**Requirements:** R5

**Dependencies:** U1, U2

**Files:**
- `tests/test_hosted_export_tier_smoke.py` (modify)
- `tests/test_hosted_golden_smoke.py` (modify if needed)
- `docs/plans/2026-06-03-185-feat-meshy-parity-gap-program-plan.md` (modify phase table)

**Verification:** Full unittest suite green; CI green.

---

## Scope Boundaries

- Golden smoke script `--validate-manifest` opt-in (deferred)
- Dynamic Gradio artifact rows (Phase P-UI)

---

## Sources & Research

- `docs/plans/2026-06-03-182-feat-hosted-smoke-delivery-format-manifest-plan.md`
- `docs/plans/2026-06-03-184-feat-golden-sample-delivery-artifact-keys-plan.md`
- `src/imageezgen3d/golden_sample.py` — `resolve_golden_required_artifact_keys` pattern
