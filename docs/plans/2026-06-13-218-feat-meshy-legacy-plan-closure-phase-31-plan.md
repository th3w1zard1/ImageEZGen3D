---
status: completed
execution: code
phase: "31"
program: meshy-parity-closure
---

# Meshy legacy plan closure — Phase 31

## Problem

Five June 2026 Meshy gap-program plans (`185`, `189`–`192`) still show `status: active` though preview/refine lanes, `target_formats`, PBR map exports, and retexture demo hooks are on `main`. Agents treat them as open work.

## Scope

**In:**

- Mark legacy Meshy plans `completed` (185 superseded by Phases 19–30)
- Extend `tests/test_meshy_parity_matrix.py` with explicit legacy plan filename guard
- Clarify `workstation_evidence_ready` vs `g9_enablement_evidence_ready` in enablement runbook
- Phase 31 note in meshy closure learning doc

**Out:** Hunyuan G7 enablement, new Meshy features, hosted redeploy

## Verification

```bash
PYTHONPATH=src python scripts/verify_meshy_parity_bundle.py
PYTHONPATH=src python -m pytest tests/test_meshy_parity_matrix.py -q
```
