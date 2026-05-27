---
title: "feat: Ship PR #42 + G7 preflight in PR CI"
type: feat
status: completed
date: 2026-05-27
origin: docs/plans/2026-05-27-060-feat-ship-pr41-hunyuan-g7-preflight-plan.md
---

# feat: Ship PR #42 + G7 preflight in PR CI

## Summary

Squash-merge PR #42 (G7 preflight harness), then enforce G1–G6 readiness on every PR via `ci.yml`, embed `g7_readiness` in admission audit JSON, and wire G7 gate closure to `G7_STATUS: PASS` in hosted-validation (future enablement run).

## Requirements

- R1. Squash-merge PR #42
- R2. `ci.yml` `hunyuan-admission-audit` job runs `hunyuan_g7_preflight.py`
- R3. `hunyuan_admission_audit.py` emits `g7_readiness`; exits 1 if not ready
- R4. `evaluate_admission_gates()` G7 passes only on `G7_STATUS: PASS` in hosted-validation (not preflight READY)
- R5. Tests for workflow contract + G7 status parsing
- R6. Hosted golden smoke still passes

## Scope boundaries

- Do not enable Hunyuan adapter
- Do not claim G7 closed without real hosted neural run

## Files

- Modify: `.github/workflows/ci.yml`
- Modify: `scripts/hunyuan_admission_audit.py`
- Modify: `src/imageezgen3d/hunyuan_admission.py`
- Modify: `tests/test_workflows.py`, `tests/test_hunyuan_admission.py`
