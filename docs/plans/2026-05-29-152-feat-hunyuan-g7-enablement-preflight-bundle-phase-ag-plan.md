---
title: "feat: Hunyuan G7 enablement preflight bundle (Phase AG)"
type: feat
status: completed
date: 2026-05-29
origin: docs/brainstorms/2026-05-29-hunyuan-g7-enablement-preflight-bundle-phase-ag-requirements.md
---

# feat: Hunyuan G7 enablement preflight bundle (Phase AG)

## Summary

Chain G9 workstation preflight bundle with in-repo G7 readiness (G1–G6) for enablement operators.

## Implementation Units

### U1. G7 enablement preflight bundle module

**Files:** `src/imageezgen3d/hunyuan_g7_enablement_preflight_bundle.py`, `tests/test_hunyuan_g7_enablement_preflight_bundle.py`

**Test scenarios:** CI-like skip exits 0 with `g7_enablement_ready=false`; G7 readiness fails when G1–G6 mock fails; strict exit 1 without evidence.

### U2. CLI and docs

**Files:** `scripts/hunyuan_g7_enablement_preflight_bundle.py`, `docs/solutions/best-practices/g7-enablement-readiness-2026-05-28.md`, `docs/solutions/best-practices/hunyuan-pre-g7-stack-2026-05-28.md`

**Dependencies:** U1
