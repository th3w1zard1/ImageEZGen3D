---
date: 2026-05-24
topic: next-runtime-slice
focus: Break ship-only loop — pick work with a product/runtime driver
mode: repo-grounded
---

# Ideation: Next Runtime / UX Slice (post–guardrail)

## Context

- Guardrail track complete on `main` (Plans 037–048, PRs #20–#31).
- **G1 legal audit** documented (Plan 049) — Hunyuan still **not enabled** (`configured=False`).
- Ship-only loops (merge PR → KB paragraph) are done; further value needs a **runtime or UX driver**.

## Ranked next slices (product-driven)

### 1. **G2 — Weight access & Space secrets plan** (recommended next)

**Driver:** Cannot wire Hunyuan inference without documented HF download path, cache size, and Space secret handling.

**Deliverables:**

- Run and record `hf download tencent/Hunyuan3D-2.1 --dry-run` (size, file list, auth expectations).
- Document `HF_TOKEN` / gated-file handling in `docs/knowledgebase/deployment-hf-cli.md` + admission G2 row.
- No weights in git; no `configured=True`.

**Why first:** Natural sequence after G1; unblocks G3 dependency pinning with real install attempt.

### 2. **G4 — ZeroGPU wiring scaffold (no enablement)**

**Driver:** Hosted Space already exposes ZeroGPU runtime; adapter stub should isolate GPU work per `zerogpu-runtime.md`.

**Deliverables:**

- `@spaces.GPU` decorator shell on future `generate()` path; keep `configured=False`.
- Tests that adapter refuses generation until gates close.

**Why second:** Code shape without legal/weight risk if G2 still in flight.

### 3. **Creator UX — “What backend ran?” chip hardening**

**Driver:** Trust metric — users must see cpu-demo vs neural without reading manifest JSON.

**Deliverables:**

- Surface adapter + fallback reason in Project Rail from latest manifest on Create/History.
- Hosted smoke asserts visible backend string.

**Why third:** Improves honesty without Hunyuan weights.

## Explicitly not next

- Flipping `configured=True` without G2–G8 evidence
- More ship-only KB paragraphs without runtime change
- Marketplace / collaboration / quota

## Evidence

- `[REPO]` `hunyuan-admission-gates.md` — G1 PASS, G2–G8 OPEN
- `[REPO]` `license-audit.md` — G1 audit record 2026-05-24
- `[OFFICIAL]` Tencent Hunyuan 3D 2.1 Community License (pinned in license audit)
