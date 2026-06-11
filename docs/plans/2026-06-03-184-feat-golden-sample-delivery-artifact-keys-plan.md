---
title: "feat: Golden sample FBX/USDZ artifact attestation (Plan 180 follow-up)"
type: feat
status: completed
date: 2026-06-03
origin: docs/plans/2026-06-03-180-feat-meshy-fbx-usdz-delivery-exports-plan.md
---

# feat: Golden sample FBX/USDZ artifact attestation (Plan 180 follow-up)

## Summary

Extend local golden-sample CI attestation to require FBX delivery exports always and USDZ when `usd-core` is installed, aligning the Block → cpu-demo contract with Meshy-class delivery tiers now proven in CI and Space requirements.

---

## Problem Frame

Plans 180–183 landed FBX/USDZ writers, Gradio slots, hosted smoke sidecar checks, and Space `usd-core` install. Golden sample attestation still validates only `manifest`, `glb`, `obj`, and `export_sidecar`, so CI can pass while delivery-format regressions slip through.

---

## Requirements

- R1. **FBX required** — Golden sample attestation requires non-empty `fbx` artifact with minimum byte threshold.
- R2. **USDZ conditional** — When `usd_core_available()`, attestation requires non-empty `usdz` artifact; skip when absent (dev installs without mesh-delivery).
- R3. **Sidecar honesty** — When export sidecar present, validate `delivery_formats` manifest parity for required delivery keys via `validate_delivery_formats_manifest`.
- R4. **Tests** — Extend `tests/test_golden_sample.py` for new keys and mocked missing-artifact failures.
- R5. **Docs** — Update golden-sample / P12 parity notes; note FBX always, USDZ when usd-core present.

---

## Key Technical Decisions

- **FBX unconditional in golden sample** — Pure-Python writer; cpu-demo always exports when configured.
- **USDZ gated on import probe** — Reuse `usd_core_available()` from `delivery_exports`; CI golden job already installs `.[mesh-delivery]`.
- **Conservative byte floors** — FBX min 200, USDZ min 100 based on draft Block sample measurements (~1425 / ~599 bytes).
- **Hosted smoke unchanged** — This slice tightens local CI only; hosted optional-key policy stays until live attestation follow-up.

---

## Implementation Units

### U1. Golden sample required keys

**Goal:** Expand attestation to FBX and conditional USDZ with byte floors.

**Requirements:** R1, R2

**Files:**
- `src/imageezgen3d/golden_sample.py` (modify)

**Approach:** Add `resolve_golden_required_artifact_keys()` returning base keys + `fbx` + optional `usdz`. Extend `MIN_ARTIFACT_BYTES`. Loop uses resolved keys.

**Test scenarios:**
- Successful attestation includes `fbx` in artifacts map.
- When usd-core installed, successful attestation includes `usdz`.
- Missing `fbx` fails attestation.

**Verification:** Golden attestation passes locally with mesh-delivery installed.

### U2. Sidecar delivery_formats validation

**Goal:** Cross-check manifest artifacts against sidecar delivery metadata.

**Requirements:** R3

**Dependencies:** U1

**Files:**
- `src/imageezgen3d/golden_sample.py` (modify)

**Approach:** After artifact size checks, load export sidecar JSON and call `validate_delivery_formats_manifest(raw_artifacts, sidecar)`.

**Test scenarios:**
- Successful attestation has no delivery_formats parity issues.

**Verification:** Attestation fails if sidecar claims exported format missing from artifacts (covered by unit test with mock if needed).

### U3. Tests and docs

**Goal:** Lock contracts and document P12 scope expansion.

**Requirements:** R4, R5

**Dependencies:** U1, U2

**Files:**
- `tests/test_golden_sample.py` (modify)
- `docs/knowledgebase/space-dependency-audit.md` (modify)
- `docs/knowledgebase/40-operational-risk/source-runtime-parity-register.md` (modify)

**Test scenarios:**
- `test_attestation_succeeds_with_repo_block_sample` asserts `fbx` present; `usdz` when available.
- Missing-artifact mock includes fbx in failure messages.

**Verification:** `tests/test_golden_sample.py` green; full suite green.

---

## Scope Boundaries

- Hosted smoke required-key expansion (deferred)
- Dynamic Gradio artifact rows from config (deferred)
- Hunyuan manifest parity artifact keys (unchanged)

### Deferred to Follow-Up Work

- Hosted golden/export-tier smoke required-key expansion after live Space USDZ attestation
- Dynamic Gradio artifact row generation from config

---

## Sources & Research

- `src/imageezgen3d/golden_sample.py` — current `REQUIRED_ARTIFACT_KEYS`
- `src/imageezgen3d/delivery_exports.py` — `usd_core_available`, `validate_delivery_formats_manifest`
- `.github/workflows/ci.yml` — golden-sample job installs mesh-delivery
- `docs/plans/2026-06-03-180-feat-meshy-fbx-usdz-delivery-exports-plan.md` — original deferral
