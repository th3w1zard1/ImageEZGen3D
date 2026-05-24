---
title: "feat: Manifest-driven UI components"
type: feat
status: completed
date: 2026-05-24
origin: docs/ideation/2026-05-23-next-focus-ideation.md #4
---

# feat: Manifest-driven UI components

## Summary

Extract manifest-driven HTML/Markdown renderers (RunStatusCard, FallbackBanner, ArtifactStrip, DraftQualityBadge) into `src/imageezgen3d/manifest_ui.py` and reuse them on Create and History surfaces.

---

## Requirements

- R1. `manifest_ui.py` exposes renderers driven by manifest/summary dicts
- R2. Create rail fallback notice uses FallbackBanner from manifest parameters
- R3. History **Open Run** shows RunStatusCard + ArtifactStrip from manifest
- R4. `app.py` delegates to manifest_ui (no duplicate copy logic)
- R5. Unit tests for manifest_ui renderers
- R6. Full unittest suite passes

---

## Scope Boundaries

- Full history compare UI — deferred
- Hunyuan enablement — out of scope

---

## Files

- Add: `src/imageezgen3d/manifest_ui.py`, `tests/test_manifest_ui.py`
- Modify: `app.py`
