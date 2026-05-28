---
title: G8 admission gate section alignment (Plan 066)
status: completed
created: 2026-05-27
---

# Plan 066 — Align G8 admission gate with section-scoped validation

## Problem

Plan 065 added `## G8 validation` with `G8_STATUS: OPEN`, but `hunyuan_admission.py` still marks G8 **pass** using whole-document heuristics (`fallback` + `preview disclaimer` anywhere in hosted-validation). That contradicts the admission table and enablement preflight (`g8_enablement_validation_passed`).

## Scope

- Merge PR #47 (Plan 065) to `main` before implementation branch.
- Change `g8_status` to use `g8_enablement_validation_passed(hosted_text)` only.
- Reject `G8_STATUS: OPEN` in `g8_enablement_validation_passed` (mirror G7).
- Tests + KB Plan 066 note.
- Link G9 runbook from `AGENTS.md`.

## Out of scope

- Hunyuan `configured=True`, weights, or live ZeroGPU enablement (G9).

## Implementation units

### Unit 1 — G8 validator + admission

**Files:** `src/imageezgen3d/hunyuan_g8_preflight.py`, `src/imageezgen3d/hunyuan_admission.py`

- Import/use `g8_enablement_validation_passed` for `g8_status`.
- In `g8_enablement_validation_passed`: return False if section contains `G8_STATUS: OPEN`.

### Unit 2 — Tests

**Files:** `tests/test_hunyuan_g8_preflight.py`, `tests/test_hunyuan_admission.py`

- Placeholder section with `G8_STATUS: OPEN` does not pass.
- Admission report shows G8 open when only placeholder exists.

### Unit 3 — Docs

**Files:** `docs/knowledgebase/40-operational-risk/hosted-validation-2026-05-23.md`, `AGENTS.md`

- Plan 066 validation bullets.
- AGENTS.md pointer to `docs/knowledgebase/hunyuan-g9-enablement-runbook.md`.

## Test scenarios

1. `g8_enablement_validation_passed` returns True only when `## G8 validation` contains `G8_STATUS: PASS` and not `OPEN`.
2. `build_hunyuan_admission_report()` lists G8 as open with current hosted-validation doc.
3. `validate_g8_cpu_fallback_status` unchanged (interim smoke honesty).

## Risks

- Admission audit may report more open gates (correct).
