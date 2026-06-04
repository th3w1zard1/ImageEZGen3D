---
title: "feat: Hunyuan neural capstone --strict parity gate (Phase AZ)"
type: feat
status: completed
date: 2026-06-03
origin: docs/brainstorms/2026-06-03-hunyuan-neural-capstone-strict-parity-phase-az-requirements.md
---

# feat: Hunyuan neural capstone --strict parity gate (Phase AZ)

## Summary

Extend `--strict` on the neural enablement capstone CLI to fail when `parity_ok` is false, completing the capstone strict parity chain after Phase AY.

## Implementation Units

### U1. Neural strict parity exit + test

**Files:** `scripts/hunyuan_neural_enablement_preflight_bundle.py`, `tests/test_hunyuan_neural_enablement_preflight_bundle.py`

### U2. Docs

**Files:** `docs/solutions/best-practices/hunyuan-pre-g7-stack-2026-05-28.md`, `docs/knowledgebase/hunyuan-g9-enablement-runbook.md`

**Dependencies:** U1
