---
title: "feat: Hunyuan admission G9 bundle record ↔ evidence artifact parity (Phase AW)"
type: feat
status: completed
date: 2026-06-03
origin: docs/brainstorms/2026-06-03-hunyuan-admission-g9-evidence-bundle-record-evidence-parity-phase-aw-requirements.md
---

# feat: Hunyuan admission G9 bundle record ↔ evidence artifact parity (Phase AW)

## Summary

When `admission-g9-enablement-evidence-bundle.json` coexists with `g9-enablement-evidence.json`, enforce nested evidence alignment and gitignore local enablement JSON artifacts.

## Requirements

| ID | Requirement |
| --- | --- |
| R1 | Parity function compares bundle nested `evidence` to standalone G9 evidence JSON |
| R2 | Optional check in `verify_neural_enablement_artifact_files()` |
| R3 | AU bundle reports `parity_ok` after bundle evidence parity |
| R4 | Gitignore local enablement JSON artifacts |
| R5 | Adapter stays disabled |

## Implementation Units

### U1. Parity module + AU bundle wiring

**Goal:** Cross-artifact parity and capstone integration.

**Files:** `src/imageezgen3d/hunyuan_neural_enablement_artifact_parity.py`, `src/imageezgen3d/hunyuan_admission_g9_enablement_evidence_bundle.py`, `scripts/verify_neural_enablement_artifact_parity.py`, `tests/test_hunyuan_neural_enablement_artifact_parity.py`, `tests/test_hunyuan_admission_g9_enablement_evidence_bundle.py`

**Test scenarios:**
- Pass when nested evidence matches standalone file
- Fail when nested evidence dict differs
- `verify_files` includes optional bundle record when both JSON present
- AU bundle sets `parity_ok=false` on mismatch (mocked)

### U2. Gitignore + docs

**Goal:** Ignore local JSON artifacts; update stack index and runbook.

**Files:** `.gitignore`, `docs/solutions/best-practices/hunyuan-pre-g7-stack-2026-05-28.md`, `docs/knowledgebase/hunyuan-g9-enablement-runbook.md`

**Dependencies:** U1
