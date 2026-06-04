---
title: "feat: Hunyuan G9 preflight bundle (Phase AF, pre-G7)"
type: feat
status: completed
date: 2026-05-29
origin: docs/brainstorms/2026-05-29-hunyuan-g9-preflight-bundle-phase-af-requirements.md
---

# feat: Hunyuan G9 preflight bundle (Phase AF, pre-G7)

## Summary

Add G9 workstation preflight bundle and cross-artifact parity verify so tier-C operators and CI share one auditable command after Phase AE.

## Problem Frame

Phase AD–AE produce multiple JSON records in `--record-dir`. Admission layer already has bundle + parity (`hunyuan_preflight_bundle.py`). G9 workstation layer needs the same closure.

## Requirements

| ID | Requirement |
| --- | --- |
| R1 | `verify_g9_workstation_artifact_parity()` compares G9 bundle enablement to standalone enablement record |
| R2 | `scripts/hunyuan_g9_preflight_bundle.py` orchestrates bundle + record verify + parity |
| R3 | `scripts/verify_g9_workstation_artifact_parity.py` standalone CLI |
| R4 | CI uses G9 preflight bundle; fixture verify retained |
| R5 | Gitignore local workstation JSON artifacts |

## Key Technical Decisions

- Reuse `verify_hunyuan_ci_artifact_parity` for audit/preflight — do not duplicate G7/G8 parity rules.
- Keep `run_g9_workstation_bundle()` unchanged; wrap via subprocess like `hunyuan_preflight_bundle.py`.
- `--strict` maps to `workstation_evidence_ready=false` exit 1 (tier-C operator only).

## Implementation Units

### U1. G9 workstation artifact parity module

**Goal:** Parity verify across G9 bundle, enablement, and admission JSON.

**Files:** `src/imageezgen3d/hunyuan_g9_workstation_artifact_parity.py`, `tests/test_hunyuan_g9_workstation_artifact_parity.py`

**Test scenarios:**
- Happy path: matching enablement nested in G9 bundle and standalone file
- Mismatch: enablement dict differs → issues non-empty
- Missing files → descriptive issues
- `adapter_configured=true` in audit → issue

### U2. G9 preflight bundle CLI

**Goal:** One-shot operator command.

**Files:** `scripts/hunyuan_g9_preflight_bundle.py`, `scripts/verify_g9_workstation_artifact_parity.py`, `tests/test_hunyuan_g9_preflight_bundle.py`

**Dependencies:** U1

**Test scenarios:**
- CI-like subprocess exit 0, stdout contains `g9_preflight_bundle_ok=True`
- `--strict` exit 1 on CI-like env
- Mocked bundle failure → exit 1

### U3. CI, docs, gitignore

**Goal:** Wire CI and document Phase AF.

**Files:** `.github/workflows/ci.yml`, `docs/solutions/best-practices/hunyuan-pre-g7-stack-2026-05-28.md`, `docs/knowledgebase/hunyuan-g9-enablement-runbook.md`, `.gitignore`, `tests/test_workflows.py`

**Dependencies:** U2

## Out of scope

- Adapter enablement on Space
- G7 hosted neural E2E
