---
title: "refactor: Simplify vertical slice and anchor STRATEGY.md"
type: refactor
status: completed
date: 2026-05-23
origin: docs/ideation/2026-05-23-next-focus-ideation.md
---

# refactor: Simplify vertical slice and anchor STRATEGY.md

## Summary

Reduce complexity in the landed vertical slice (app.py CSS/HTML helpers, deploy_assets, exporters) without behavior change, write repo-root STRATEGY.md from grounded project intent, and refresh the active living plan with post-slice deltas. Hosted E2E remains deferred.

---

## Problem Frame

PR #1 merged KB + deploy/UI work but skipped STRATEGY.md, left dead CSS/helpers from the UI rewrite, and deferred P10. Before the next feature pass, the branch needs a simplification pass and a durable strategy anchor for ce-plan/ce-ideate.

---

## Requirements

- R1. Simplification preserves 55+ unittest pass and compileall green
- R2. Remove dead code/CSS confirmed unused in branch diff scope
- R3. STRATEGY.md exists at repo root with required sections 1–5
- R4. Active plan receives 3-delta living-plan update
- R5. No hosted validation claims added without execution

---

## Scope Boundaries

- Hosted HF Space E2E (P10) — deferred
- Composer layout reorder — deferred unless trivial CSS-only win emerges
- Committing `docs/ideation/` — optional

---

## Implementation Units

- U1. **Simplify branch diff code**

**Goal:** Apply ce-simplify-code + maintainability/simplicity review fixes on `origin/main...HEAD` diff.

**Requirements:** R1, R2

**Files:**
- Modify: `app.py`, `src/imageezgen3d/deploy_assets.py`, `src/imageezgen3d/exporters.py` (only if reviewers find issues)

**Verification:** unittest discover + compileall pass

---

- U2. **Write STRATEGY.md**

**Goal:** Anchor product direction from project-intent and ideation docs.

**Requirements:** R3

**Files:**
- Create: `STRATEGY.md`

**Verification:** Template sections 1–5 populated; assumptions noted for unconfirmed interview gaps

---

- U3. **Living plan delta**

**Goal:** Update active plan with landed/partial/next after this pass.

**Requirements:** R4

**Files:**
- Modify: `docs/plans/2026-05-23-002-fix-vertical-slice-deploy-ui-plan.md` (delta section) or append to plan 003

**Verification:** 3-delta block present

---

- U4. **Review + ship**

**Goal:** ce-code-review autofix, browser smoke, commit/push PR update.

**Requirements:** R1, R5

**Dependencies:** U1–U3

**Verification:** PR updated; tests green

---

## Sources & References

- `docs/knowledgebase/project-intent.md`
- `docs/ideation/2026-05-23-next-focus-ideation.md`
- PR #1 residual: P10 hosted E2E
