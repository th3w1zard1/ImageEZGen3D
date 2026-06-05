---
title: "feat: Space requirements.txt usd-core opt-in (Plan 180 follow-up)"
type: feat
status: completed
date: 2026-06-03
origin: docs/plans/2026-06-03-180-feat-meshy-fbx-usdz-delivery-exports-plan.md
---

# feat: Space requirements.txt usd-core opt-in (Plan 180 follow-up)

## Summary

Complete the Plan 180 deferred payload audit and add `usd-core` to the Hugging Face Space `requirements.txt` so hosted runs can produce USDZ delivery exports matching local `[mesh-delivery]` parity. Lock the change with requirements parity tests and parity-register documentation.

---

## Problem Frame

Plan 180 gated USDZ behind the optional `mesh-delivery` extra and deliberately omitted `usd-core` from Space `requirements.txt` until a payload audit. Plans 181–182 landed Gradio USDZ download slots and hosted smoke delivery-format validation, but hosted Space still skips USDZ because `usd_core_available()` is false at build time. Creators on the live Space see empty USDZ downloads despite config listing `usdz` in export formats.

---

## Requirements

- R1. **Payload audit record** — Document measured `usd-core` install footprint and accept/reject rationale before changing Space deps.
- R2. **Space install contract** — Add `usd-core>=24.0` to `requirements.txt`, aligned with `pyproject.toml` `[project.optional-dependencies].mesh-delivery`.
- R3. **Parity test** — Extend `test_requirements_are_self_contained_for_space_builds` (or sibling) to assert mesh-delivery deps present and no editable install lines.
- R4. **Docs** — Update export-guide and parity register P6 to reflect Space USDZ availability.
- R5. **No smoke contract break** — Hosted golden/export-tier smoke remain tolerant of optional USDZ; no required-key expansion in this slice.

---

## Key Technical Decisions

- **Add usd-core after audit, not before** — Audit documents ~150 MB Linux wheel footprint; acceptable versus Hunyuan stack and already-shipped trimesh mesh deps on Space.
- **Pin lower bound only** — Use `usd-core>=24.0` in requirements to match pyproject; let pip resolve current wheel (26.x on supported platforms).
- **Keep CI mesh-delivery extra** — CI already installs `.[mesh-delivery]`; requirements change targets Space build path only.
- **Defer golden required-key expansion** — USDZ stays optional in golden sample until hosted attestation confirms USDZ bytes on live Space.

---

## Implementation Units

### U1. Payload audit artifact

**Goal:** Record audit evidence that justifies enabling usd-core on Space.

**Requirements:** R1

**Files:**
- `docs/knowledgebase/space-dependency-audit.md` (create)

**Approach:** Document Linux wheel size (~149 MB pxr module), comparison to existing mesh deps, and decision to opt in. Note HF requirements-first build order constraint.

**Test scenarios:**
- Test expectation: none — documentation-only unit.

**Verification:** Audit doc exists with size figure and opt-in decision.

### U2. requirements.txt + parity test

**Goal:** Add usd-core to Space requirements and lock parity in tests.

**Requirements:** R2, R3

**Dependencies:** U1

**Files:**
- `requirements.txt` (modify)
- `tests/test_config.py` (modify)

**Approach:** Append `usd-core>=24.0` after mesh deps. Extend requirements self-contained test to assert line present and still no `-e` install.

**Test scenarios:**
- `test_requirements_are_self_contained_for_space_builds` asserts `usd-core>=24.0` in parsed lines.
- Existing trimesh/fast-simplification assertions remain green.

**Verification:** `tests/test_config.py` passes.

### U3. Export guide + parity register

**Goal:** Align docs with Space USDZ availability.

**Requirements:** R4

**Dependencies:** U2

**Files:**
- `docs/knowledgebase/export-guide.md` (modify)
- `docs/knowledgebase/40-operational-risk/source-runtime-parity-register.md` (modify)

**Approach:** Note Space `requirements.txt` includes usd-core; update P6 row last-verified date and delta note.

**Test scenarios:**
- Test expectation: none — documentation-only unit.

**Verification:** Docs mention Space USDZ path; P6 row updated.

---

## Scope Boundaries

- Golden sample required-key expansion for FBX/USDZ (deferred)
- Dynamic Gradio artifact rows from config (deferred)
- Hosted smoke changing USDZ from optional to required (deferred until live attestation)

### Deferred to Follow-Up Work

- Golden sample / hosted smoke required-key expansion after live Space USDZ attestation
- Dynamic Gradio artifact row generation from config

---

## Sources & Research

- `docs/plans/2026-06-03-180-feat-meshy-fbx-usdz-delivery-exports-plan.md` — deferred Space opt-in
- `requirements.txt` — current Space install contract
- `pyproject.toml` — `[project.optional-dependencies].mesh-delivery`
- `tests/test_config.py` — `test_requirements_are_self_contained_for_space_builds`
- `docs/knowledgebase/40-operational-risk/source-runtime-parity-register.md` — P6 row
