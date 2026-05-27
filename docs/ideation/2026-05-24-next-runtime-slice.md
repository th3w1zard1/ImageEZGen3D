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
- **G4 ZeroGPU wiring** scaffold (Plan 051) — `spaces.GPU` shell in `hunyuan.py`; still **not enabled**.
- **G3 dependency audit** (Plan 052) — `hunyuan-pins.txt`, `.[hunyuan-audit]`, CI smoke; still **not enabled**.
- **G5 resource fit** (Plan 053 / PR #35) — VRAM/disk budget + G1 LICENSE CI verify on `main`; still **not enabled**.

## Ranked next slices (product-driven)

### 1. **G7 — Hosted E2E (real Hunyuan path)** (recommended next)

**Driver:** Prove real `hunyuan-zerogpu` generation on live Space (not cpu-demo fallback).

**Deliverables:**

- Block/Vase sample run with adapter enabled after G5 closes.
- Entry in `hosted-validation-2026-05-23.md` with run id + manifest/GLB/OBJ.
- Update admission G7 row.

### 2. **Creator UX — “What backend ran?” chip hardening** — **shipped (Plan 055 / PR #37)**

**Driver:** Trust metric — users must see cpu-demo vs neural without reading manifest JSON.

**Delivered:** `backend_rail_chips_html` on live Space after deploy `9ad3eb74` (Plan 056 verified).

**Follow-up:** Optional hosted smoke HTML assertion; History tab parity if needed.

## Explicitly not next

- Flipping `configured=True` without G2–G8 evidence
- More ship-only KB paragraphs without runtime change
- Marketplace / collaboration / quota

## Evidence

- `[REPO]` `hunyuan-admission-gates.md` — G1–G5 PASS, G6–G7 OPEN
- `[REPO]` `hunyuan-resource-fit.md` — G5 budget 2026-05-25
- `[REPO]` `scripts/hunyuan_g1_legal_verify.py` — automated G1 clause check
- `[REPO]` `hunyuan-dependencies.md` — G3 audit 2026-05-24
- `[REPO]` `hunyuan-weight-access.md` — G2 dry-run 2026-05-24
- `[REPO]` `license-audit.md` — G1 audit record 2026-05-24
- `[OFFICIAL]` Tencent Hunyuan 3D 2.1 Community License (pinned in license audit)
