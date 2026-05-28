---
title: "feat: Text neural adapter skeleton (Phase D licensed-model seam)"
type: feat
status: completed
date: 2026-05-28
origin: docs/plans/2026-05-28-119-feat-meshy-class-platform-foundation-plan.md
---

# feat: Text neural adapter skeleton (Phase D licensed-model seam)

## Summary

Add a **`text-neural`** adapter seam behind the Plan 119 generation contract — inference skeleton, admission-controlled `configured` flag, orchestrator auto-routing for text modality, and honest fallback to `text-demo` when disabled. Does **not** ship a licensed model or claim neural reconstruction on hosted Space.

---

## Requirements

- R1. **`text_neural_inference.py`** — documents text-conditioned shape flow; raises `NotImplementedError` without backend; mock backend for tests.
- R2. **`text-neural` adapter** — `configured=False` by default; env `IMAGEEZ_TEXT_NEURAL_CONFIGURED` gate.
- R3. **Orchestrator text routing** — `auto` prefers `text-neural` when configured, else `text-demo` with explicit fallback reason + stub disclaimer.
- R4. **UI labels** — manifest_ui backend label for `text-neural`.
- R5. **Tests** — inference module, adapter gate, orchestrator routing, config env.
- R6. **Trust** — no Space enablement; stub disclaimer only on `text-demo` path.

---

## Scope Boundaries

- Licensed text-to-3D model weights or inference
- ZeroGPU/Space enablement for text neural
- Async job API (Phase E)
- Replacing `text-demo` as default when neural disabled

---

## Implementation Units

- U1. Inference skeleton + tests
- U2. Adapter + config gate
- U3. Orchestrator + manifest_ui
- U4. pyproject.toml section + plan completion

---

## Key Technical Decisions

- Single-stage **shape** neural path for text (texture skipped with note until paint adapter exists).
- Injectable mock backend for unit tests only.
- `preview_disclaimer` = stub disclaimer only when `text-demo` executes (including auto fallback).
