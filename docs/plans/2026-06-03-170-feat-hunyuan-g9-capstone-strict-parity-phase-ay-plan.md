---
title: "feat: Hunyuan G9 capstone --strict parity gate (Phase AY)"
type: feat
status: completed
date: 2026-06-03
origin: docs/brainstorms/2026-06-03-hunyuan-g9-capstone-strict-parity-phase-ay-requirements.md
---

# feat: Hunyuan G9 capstone --strict parity gate (Phase AY)

## Summary

Align `--strict` exit codes on G9 evidence capstone CLIs with documented `parity_ok` requirement.

## Implementation Units

### U1. Strict parity exit codes + tests

**Goal:** Fail `--strict` when `parity_ok` is false even if preflight flags pass.

**Files:** `scripts/hunyuan_admission_g9_enablement_evidence_bundle.py`, `scripts/hunyuan_g9_enablement_evidence_bundle.py`, `tests/test_hunyuan_admission_g9_enablement_evidence_bundle.py`, `tests/test_hunyuan_g9_enablement_evidence_bundle.py`

### U2. Docs

**Goal:** Document strict parity semantics in stack index and runbook.

**Files:** `docs/solutions/best-practices/hunyuan-pre-g7-stack-2026-05-28.md`, `docs/knowledgebase/hunyuan-g9-enablement-runbook.md`

**Dependencies:** U1
