---
title: "feat: Hunyuan neural capstone live-probe wiring (Phase AN)"
type: feat
status: completed
date: 2026-05-29
origin: docs/brainstorms/2026-05-29-hunyuan-neural-capstone-live-probe-phase-an-requirements.md
---

# feat: Hunyuan neural capstone live-probe wiring (Phase AN)

## Summary

One operator command can run the neural enablement capstone and record hosted G7 live-probe JSON for artifact parity.

## Implementation Units

### U1. G7 live-probe record helper

**Files:** `src/imageezgen3d/hunyuan_g7_preflight.py`, `scripts/hunyuan_g7_preflight.py`

### U2. Neural capstone wiring

**Files:** `src/imageezgen3d/hunyuan_neural_enablement_preflight_bundle.py`, `scripts/hunyuan_neural_enablement_preflight_bundle.py`, tests, stack docs, G9 runbook

**Dependencies:** U1
