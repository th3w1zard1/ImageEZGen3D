---
title: "feat: Hunyuan admission + G9 enablement evidence preflight bundle (Phase AU)"
type: feat
status: active
date: 2026-06-03
origin: docs/brainstorms/2026-06-03-hunyuan-admission-g9-enablement-evidence-bundle-phase-au-requirements.md
---

# feat: Hunyuan admission + G9 enablement evidence preflight bundle (Phase AU)

## Summary

One operator command chains admission preflight bundle with the G9 enablement evidence capstone so enablement PR reviewers get admission audit JSON and `g9-enablement-evidence.json` from a single `--record-dir` run.

## Requirements

| ID | Requirement |
| --- | --- |
| R1 | `run_admission_g9_enablement_evidence_bundle()` chains preflight bundle + G9 evidence capstone |
| R2 | `admission_g9_enablement_evidence_ok` when both layers pass |
| R3 | Forward neural capstone flags to G9 evidence bundle |
| R4 | CLI `--record-dir`, `--skip-weight-warm`, `--strict`, `--json` |
| R5 | Adapter stays disabled |

## Implementation Units

### U1. Bundle module + CLI

**Goal:** Orchestrate admission preflight then G9 evidence capstone.

**Files:** `src/imageezgen3d/hunyuan_admission_g9_enablement_evidence_bundle.py`, `scripts/hunyuan_admission_g9_enablement_evidence_bundle.py`, `tests/test_hunyuan_admission_g9_enablement_evidence_bundle.py`

**Test scenarios:**
- CI-like skip: admission ok, evidence not ready, bundle reports honestly
- Mocked G9 capstone: admission failure surfaces in issues
- Script subprocess exit 0 on default CI path

### U2. Docs

**Goal:** Stack index + G9 runbook one-command path.

**Files:** `docs/solutions/best-practices/hunyuan-pre-g7-stack-2026-05-28.md`, `docs/knowledgebase/hunyuan-g9-enablement-runbook.md`

**Dependencies:** U1
