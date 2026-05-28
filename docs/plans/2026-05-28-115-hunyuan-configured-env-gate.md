---
title: Hunyuan configured env gate (Plan 115)
type: feat
status: completed
date: 2026-05-28
---

# Plan 115 — Hunyuan `configured` env gate

## Summary

Wire `HunyuanPlaceholderAdapter.configured` from `AppConfig` / `IMAGEEZ_HUNYUAN_CONFIGURED` (default **false**) so enablement PRs can flip the flag via Space secrets without code edits. GPU inference remains `NotImplementedError` until a follow-on slice wires models.

## Problem Frame

G7 readiness docs point at enablement, but `configured` is hard-coded `False` on the class. Operators need a config seam that preserves admission safety (default off) and honest errors when enabled without inference.

## Requirements

- R1. `HunyuanSettings.configured` in `AppConfig`, env `IMAGEEZ_HUNYUAN_CONFIGURED`, pyproject default false.
- R2. Orchestrator passes configured into `HunyuanPlaceholderAdapter`.
- R3. When configured true, `generate()` reaches GPU shell and raises `NotImplementedError` (not “intentionally disabled”).
- R4. Default remains false; no G7 PASS claims; do not set on live Space in this PR.
- R5. Tests for config + adapter behavior; `.env.example` + KB note.

## Scope Boundaries

- Hunyuan model inference implementation.
- Setting `IMAGEEZ_HUNYUAN_CONFIGURED=true` on hosted Space.
- Closing G7/G8/G9 gates.

## Implementation Units

- U1. **Config + adapter seam**

**Files:** `src/imageezgen3d/config.py`, `src/imageezgen3d/adapters/hunyuan.py`, `src/imageezgen3d/orchestrator.py`, `pyproject.toml`, `.env.example`

**Test scenarios:**
- Happy path: default `hunyuan.configured` is false.
- Happy path: `IMAGEEZ_HUNYUAN_CONFIGURED=true` → adapter configured true.
- Error path: configured true → `generate()` raises `NotImplementedError`.

**Verification:** `tests/test_config.py`, `tests/test_hunyuan_adapter.py` pass.

- U2. **Docs + KB**

**Files:** `docs/solutions/best-practices/g7-enablement-readiness-2026-05-28.md`, `docs/knowledgebase/hunyuan-g7-preflight.md`, `docs/knowledgebase/40-operational-risk/hosted-validation-2026-05-23.md`

**Verification:** Plan 115 section; readiness doc mentions env gate + inference blocker.
