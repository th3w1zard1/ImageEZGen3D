---
status: completed
execution: code
phase: "8"
program: meshy-parity-closure
---

# Meshy parity program closure (Phase 8)

## Problem

Phases U–7 merged but `docs/reference/meshy/PARITY-MATRIX.md` still lists capabilities as "planned (Phase N)". Agents and reviewers cannot trust the matrix for current parity.

## Scope

**In:** Refresh PARITY-MATRIX statuses to match landed code; add AGENTS.md pointer to `verify_meshy_parity_bundle.py`; note remaining gaps (viewer action wiring, multi-color print task, UV/boolean job routes).

**Out:** New features, Hunyuan enablement, viewer button wiring.

## Files

- `docs/reference/meshy/PARITY-MATRIX.md`
- `AGENTS.md` (Meshy verify one-liner)

## Verification

- Manual review: every row reflects grep-able module presence
- `PYTHONPATH=src python scripts/verify_meshy_parity_bundle.py`
