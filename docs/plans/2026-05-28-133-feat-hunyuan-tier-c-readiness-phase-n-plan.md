---
title: "feat: Hunyuan tier-C readiness gate (Phase N, pre-G7)"
type: feat
status: completed
date: 2026-05-28
origin: docs/plans/2026-05-28-132-feat-hunyuan-runtime-probe-phase-m-plan.md
---

# feat: Hunyuan tier-C readiness gate (Phase N, pre-G7)

## Summary

Add tier B/C readiness evaluation, weight-backend env gate, and operator CLI so integrators can warm weights and verify imports before inference wiring — without enabling the adapter or claiming G7 PASS.

## Problem Frame

Phase M added import probes and weight warm CLIs. Phase N unifies readiness into `prepare_tier_c_runtime()` and wires `WeightVerifiedHunyuanBackend` behind `IMAGEEZ_HUNYUAN_WEIGHT_BACKEND` so local runs fail honestly when tier C is missing or inference is unwired.

## Requirements

- R1. `evaluate_tier_c_readiness()` reports tier B/C gaps and optional weight cache status.
- R2. `prepare_tier_c_runtime()` raises `TierCReadinessError` or `NotImplementedError` before neural claims.
- R3. `IMAGEEZ_HUNYUAN_WEIGHT_BACKEND` resolves `WeightVerifiedHunyuanBackend` (dev backend takes precedence).
- R4. `scripts/hunyuan_tier_c_readiness.py` exposes readiness report (informational exit 0).
- R5. Admission preflight bundle remains exit 0 with `configured=False`.

## Key Technical Decisions

- Dev backend (`IMAGEEZ_HUNYUAN_DEV_BACKEND`) wins over weight backend when both set — preview path stays local-only.
- Weight backend stops at `NotImplementedError` even when tier C is satisfied — no false neural success.
- `resolve_shape_checkpoint()` extracted for reuse from weight warm validation.

## Implementation Units

### U1. Tier-C runtime module

**Goal:** Centralize readiness evaluation and preparation gate.

**Files:** `src/imageezgen3d/hunyuan_tier_c_runtime.py`, `tests/test_hunyuan_tier_c_runtime.py`

**Test scenarios:** skip-weight-warm report; missing tier C raises `TierCReadinessError`; satisfied deps raise `NotImplementedError`; CLI smoke.

### U2. Weight backend config + backend wiring

**Goal:** Env-gated weight backend integrated into inference resolution.

**Files:** `src/imageezgen3d/config.py`, `pyproject.toml`, `src/imageezgen3d/hunyuan_backend.py`, `src/imageezgen3d/hunyuan_inference.py`, `src/imageezgen3d/hunyuan_weights.py`, `tests/test_hunyuan_backend.py`

**Test scenarios:** weight backend env raises on missing tier C; dev backend precedence; metadata `tier_c_shell` when applicable.

### U3. Operator CLI + solutions doc

**Goal:** Document Phase N in pre-G7 stack learning doc.

**Files:** `scripts/hunyuan_tier_c_readiness.py`, `docs/solutions/best-practices/hunyuan-pre-g7-stack-2026-05-28.md`, `docs/solutions/README.md`

## Out of scope

- Tencent tier-C inference runner implementation
- `IMAGEEZ_HUNYUAN_CONFIGURED=true` on Space
- G7 hosted attestation update

## Verification

- `PYTHONPATH=src python scripts/check_python_style.py`
- `PYTHONPATH=src python -m unittest discover -s tests -q`
- `PYTHONPATH=src python scripts/hunyuan_preflight_bundle.py`
