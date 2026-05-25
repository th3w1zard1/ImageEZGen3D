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
- **G2 weight access** documented (Plan 050) — 14.9 GB dry-run + Space secrets plan; still **not enabled**.
- Ship-only loops (merge PR → KB paragraph) are done; further value needs a **runtime or UX driver**.

## Ranked next slices (product-driven)

### 1. **G4 — ZeroGPU wiring scaffold (no enablement)** (recommended next)

**Driver:** Hosted Space already exposes ZeroGPU runtime; adapter stub should isolate GPU work per `zerogpu-runtime.md`.

**Deliverables:**

- `@spaces.GPU` decorator shell on future `generate()` path; keep `configured=False`.
- Tests that adapter refuses generation until gates close.

**Why first:** Code shape without downloading 14.9 GB into the repo.

### 2. **G3 — Dependency audit (install smoke)**

**Driver:** Hunyuan integration needs pinned Python/CUDA deps with known redistribution rights before Space install.

**Deliverables:**

- Constraints or lockfile slice for Hunyuan-only optional extra (not enabled by default).
- CI job or documented install smoke on target Python (3.11 Space baseline).
- Update admission G3 row with evidence.

**Why second:** Requires knowing which packages the G4 GPU path will import.

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

- `[REPO]` `hunyuan-admission-gates.md` — G1–G2 PASS, G3–G8 OPEN
- `[REPO]` `hunyuan-weight-access.md` — G2 dry-run 2026-05-24
- `[REPO]` `license-audit.md` — G1 audit record 2026-05-24
- `[OFFICIAL]` Tencent Hunyuan 3D 2.1 Community License (pinned in license audit)
