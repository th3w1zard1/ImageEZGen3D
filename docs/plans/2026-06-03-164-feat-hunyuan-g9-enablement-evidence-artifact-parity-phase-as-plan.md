---
title: "feat: Hunyuan G9 enablement evidence ↔ neural artifact parity (Phase AS)"
type: feat
status: completed
date: 2026-06-03
origin: docs/brainstorms/2026-06-03-hunyuan-g9-enablement-evidence-artifact-parity-phase-as-requirements.md
---

# feat: Hunyuan G9 enablement evidence ↔ neural artifact parity (Phase AS)

## Summary

When `g9-enablement-evidence.json` coexists with neural preflight JSON, require enablement-ready alignment for `ok=true` evidence records and wire parity into the G9 evidence capstone.

## Requirements

| ID | Requirement |
| --- | --- |
| R1 | `verify_g9_enablement_evidence_neural_artifact_parity()` enforces neural alignment when evidence `ok=true` |
| R2 | Optional check in `verify_neural_enablement_artifact_files()` when evidence JSON present |
| R3 | `run_g9_enablement_evidence_bundle()` reports `parity_ok` after parity pass |
| R4 | Schema verify before compare |
| R5 | Adapter stays disabled |

## Implementation Units

### U1. Parity module + G9 bundle wiring

**Goal:** Cross-artifact parity function and capstone integration.

**Files:** `src/imageezgen3d/hunyuan_neural_enablement_artifact_parity.py`, `src/imageezgen3d/hunyuan_g9_enablement_evidence_bundle.py`, `scripts/verify_neural_enablement_artifact_parity.py`, `tests/test_hunyuan_neural_enablement_artifact_parity.py`, `tests/test_hunyuan_g9_enablement_evidence_bundle.py`

**Test scenarios:**
- Pass when evidence and neural flags match (ready fixture pair)
- Fail when evidence `ok=true` but neural not ready
- `verify_files` includes optional evidence JSON when present
- G9 bundle sets `parity_ok=true` on matching CI-like run

### U2. Docs

**Goal:** Update stack index and G9 runbook parity note.

**Files:** `docs/solutions/best-practices/hunyuan-pre-g7-stack-2026-05-28.md`, `docs/knowledgebase/hunyuan-g9-enablement-runbook.md`

**Dependencies:** U1
