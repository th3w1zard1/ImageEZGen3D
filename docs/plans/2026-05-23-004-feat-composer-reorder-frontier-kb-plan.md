---
title: "feat: Composer-above-fold reorder and frontier KB track"
type: feat
status: completed
date: 2026-05-23
origin: STRATEGY.md
---

# feat: Composer-above-fold reorder and frontier KB track

## Summary

Reorder Create-tab layout so brief, upload, and Generate Mesh appear above starter cards at common desktop widths, capture Tier-3 frontier research in the knowledgebase, and add a regression test for layout order. Hosted E2E remains deferred.

---

## Problem Frame

Design review measured Generate Mesh ~634px below fold because hero + starter cards precede the composer grid. STRATEGY Track "Creator UI fidelity" requires the creation path to win the page. Frontier trends should be tracked without changing product truth.

---

## Requirements

- R1. `composer-grid` renders before `starter-card-row` in Create tab DOM
- R2. Existing event wiring for template buttons unchanged
- R3. Unittests pass; add test asserting layout block order in `build_demo` source or structure
- R4. New KB doc under `docs/knowledgebase/` for Tier-3 frontier tracking with evidence labels
- R5. Living plan delta updated; no false hosted validation claims

---

## Scope Boundaries

- Hosted HF Space E2E (P10) — deferred
- Image thumbnails on starter cards — deferred
- Hunyuan adapter enablement — out of scope

---

## Implementation Units

- U1. **Reorder composer layout**

**Goal:** Move starter cards below brief/upload/controls.

**Requirements:** R1, R2

**Files:**
- Modify: `app.py` (Create tab layout ~743–900)

**Test scenarios:**
- Happy path: template apply buttons still wired after reorder
- Regression: layout order test

**Verification:** Browser smoke shows Generate Mesh higher on page

---

- U2. **Compact hero + starter row CSS**

**Goal:** Reduce above-fold height after reorder.

**Requirements:** R1

**Files:**
- Modify: `app.py` `_CSS`

**Verification:** Visual check at 1440×900

---

- U3. **Frontier KB doc**

**Goal:** Record Tier-3 research from kb-frontier-researcher.

**Requirements:** R4

**Files:**
- Create: `docs/knowledgebase/20-theory/frontier-image-to-3d-2026-05-23.md`
- Modify: `docs/knowledgebase/README.md` (index link)

**Verification:** Doc labeled Tier 3 / non-current truth

---

- U4. **Tests + ship**

**Requirements:** R3, R5

**Files:**
- Modify: `tests/test_app.py`

**Verification:** 56+ tests pass

---

## Sources & References

- `docs/knowledgebase/50-execution/ui-fidelity-implementation-checklist-2026-05-18.md`
- `STRATEGY.md` Creator UI fidelity track
- kb-frontier-researcher output (this pass)

---

## Living plan delta (2026-05-23)

**Landed**

- U1–U2: Create tab reordered — `composer-grid` before `starter-card-row`; compact hero CSS in composer panel.
- U3: Tier-3 frontier doc at `docs/knowledgebase/20-theory/frontier-image-to-3d-2026-05-23.md`; README index updated.
- U4: `test_create_tab_places_composer_before_starter_cards`; 56 tests pass.

**Partial / uncertain**

- P10 hosted HF Space E2E (Block/Vase) — still `[OPEN]` per parity register.
- Visual validation at 1440×900 — browser smoke only, not measured pixel audit.

**Next steps**

- Run hosted deploy + default sample E2E when HF CLI path is ready.
- Optional: image-led starter thumbnails; Hunyuan adapter after license gate.
