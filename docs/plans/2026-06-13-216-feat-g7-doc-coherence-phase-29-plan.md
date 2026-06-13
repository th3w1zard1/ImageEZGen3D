---
status: completed
execution: ops
phase: "29"
program: hunyuan-g7-readiness
---

# G7 readiness doc coherence pass (Phase 29)

## Problem

`ce-coherence-reviewer` scored Phases 20–28 docs **6.5/10**: deploy hash over-scoping (`a149111` vs `e368ad8`), stale plan status, attestation index section title drift, and ambiguous `/lfg` resume guidance.

## Requirements

| ID | Requirement |
| --- | --- |
| R1 | Fix deploy attribution: `e368ad8` (Phases 20–24) vs `a149111` (Phases 25–27) |
| R2 | Rename/split hosted-live-attestation Phase 20–28 index; update solutions README |
| R3 | Mark Phase 28 + Meshy Phase 19 plans `completed`; clarify AGENTS.md pause/resume |
| R4 | Do **not** claim G7 PASS or re-run hosted smokes |

## Verification

```bash
PYTHONPATH=src python scripts/hunyuan_admission_audit.py
PYTHONPATH=src python scripts/verify_meshy_parity_bundle.py
```
