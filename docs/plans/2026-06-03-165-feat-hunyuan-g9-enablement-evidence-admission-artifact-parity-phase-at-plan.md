---
title: "feat: Hunyuan G9 enablement evidence ↔ admission audit artifact parity (Phase AT)"
type: feat
status: active
date: 2026-06-03
origin: docs/brainstorms/2026-06-03-hunyuan-g9-enablement-evidence-admission-artifact-parity-phase-at-requirements.md
---

# feat: Hunyuan G9 enablement evidence ↔ admission audit artifact parity (Phase AT)

## Summary

When `g9-enablement-evidence.json` coexists with admission audit JSON in one `--record-dir`, enforce the adapter-disabled safety guard and optional admission CI parity before enablement PR reviewers trust the evidence record.

## Requirements

| ID | Requirement |
| --- | --- |
| R1 | `verify_g9_enablement_evidence_admission_artifact_parity()` blocks `ok=true` evidence when `adapter_configured=true` |
| R2 | Optional check in `verify_neural_enablement_artifact_files()` when evidence + admission audit both present |
| R3 | Delegate `verify_hunyuan_ci_artifact_parity` when admission preflight JSON also present |
| R4 | Schema verify before compare |
| R5 | Adapter stays disabled |

## Implementation Units

### U1. Parity module extension

**Goal:** Cross-artifact parity between G9 evidence and admission audit JSON.

**Files:** `src/imageezgen3d/hunyuan_neural_enablement_artifact_parity.py`, `scripts/verify_neural_enablement_artifact_parity.py`, `tests/test_hunyuan_neural_enablement_artifact_parity.py`

**Test scenarios:**
- Pass when evidence `ok=false` and audit `adapter_configured=false`
- Fail when evidence `ok=true` but audit `adapter_configured=true`
- `verify_files` runs admission parity when both evidence and audit JSON present
- CI parity delegated when enablement preflight JSON also present

### U2. Docs

**Goal:** Update stack index and G9 runbook.

**Files:** `docs/solutions/best-practices/hunyuan-pre-g7-stack-2026-05-28.md`, `docs/knowledgebase/hunyuan-g9-enablement-runbook.md`

**Dependencies:** U1
