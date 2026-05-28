---
title: G8 preflight and audit artifact visibility (Plan 067)
status: completed
created: 2026-05-27
---

# Plan 067 — G8 visibility in preflight reports and admission audit JSON

## Problem

Plan 066 aligned G8 admission with `## G8 validation`, but operators still lack parity with G7 in CI artifacts:

- `format_enablement_preflight_report()` omits `g8_enablement_documented` (present only in JSON `to_dict()`).
- `hunyuan-admission-audit.json` has `g7_readiness` but no structured `g8_enablement` block.

## Scope

- Merge PR #48 (Plan 066) first.
- Add `evaluate_g8_enablement_status()` in `hunyuan_g8_preflight.py`.
- Wire into enablement preflight text report and admission audit JSON.
- Tests + KB Plan 067 note.

## Out of scope

- Hunyuan enablement (`configured=True`) or live ZeroGPU runs.

## Implementation units

### Unit 1 — G8 status evaluator

**File:** `src/imageezgen3d/hunyuan_g8_preflight.py`

- `G8EnablementStatus` with `documented`, `section_present`, `interim_open`, `gate_status`.
- `evaluate_g8_enablement_status(hosted_text, gates=None)`.

### Unit 2 — Reports and audit JSON

**Files:** `src/imageezgen3d/hunyuan_enablement_preflight.py`, `scripts/hunyuan_admission_audit.py`

- Use evaluator for `g8_enablement_documented`.
- Print `g8_enablement_documented=` in text report.
- Emit `g8_enablement` in audit payload.

### Unit 3 — Tests and docs

**Files:** `tests/test_hunyuan_g8_preflight.py`, `tests/test_hunyuan_admission.py`, `tests/test_hunyuan_enablement_preflight.py`, `docs/knowledgebase/hunyuan-enablement-preflight.md`, hosted-validation Plan 067 section.

## Test scenarios

1. Placeholder `G8_STATUS: OPEN` → `documented=False`, `interim_open=True`.
2. `G8_STATUS: PASS` in section → `documented=True`.
3. Admission audit JSON includes `g8_enablement` with expected fields.
4. Enablement preflight text report includes `g8_enablement_documented=`.
