---
title: "feat: Hunyuan G7 live-probe ↔ neural artifact parity (Phase AM)"
type: feat
status: active
date: 2026-05-29
origin: docs/brainstorms/2026-05-29-hunyuan-g7-live-probe-neural-artifact-parity-phase-am-requirements.md
---

# feat: Hunyuan G7 live-probe ↔ neural artifact parity (Phase AM)

## Summary

When `hunyuan-g7-live-probe.json` coexists with neural enablement artifacts, verify `readiness` alignment with the neural record's nested `g7_readiness`.

## Implementation Units

### U1. Live-probe ↔ neural parity module

**Files:** extend `src/imageezgen3d/hunyuan_neural_enablement_artifact_parity.py`, `tests/test_hunyuan_neural_enablement_artifact_parity.py`, fixture JSON

### U2. Docs

**Files:** `docs/solutions/best-practices/hunyuan-pre-g7-stack-2026-05-28.md`, G9 runbook optional note

**Dependencies:** U1
