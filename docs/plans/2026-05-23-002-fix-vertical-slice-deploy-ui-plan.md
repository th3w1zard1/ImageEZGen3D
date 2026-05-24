---
title: "fix: Land deploy parity and UI fidelity vertical slice"
type: fix
status: completed
date: 2026-05-23
origin: docs/ideation/2026-05-23-next-focus-ideation.md
---

# fix: Land deploy parity and UI fidelity vertical slice

## Summary

Repair deploy pipeline syntax blockers (P4/P5), re-render deploy templates with port 7865, and land the in-flight UI/export/config slice with tests and parity register updates. Hosted Space E2E is deferred to a follow-up pass after deploy scripts compile.

---

## Problem Frame

Nine modified files sit uncommitted while `compileall` fails on deploy scripts. Parity register marks P4/P5 **BLOCKED**. UI fidelity CSS improvements from design review are partial. The slice must compile, test, and document before any hosted validation claims.

---

## Requirements

- R1. `scripts/render_deploy_assets.py` and `src/imageezgen3d/deploy_assets.py` parse and pass `compileall`
- R2. Deploy templates render with `container_port=7865`
- R3. Existing unittest suite passes (`tests/test_app.py`, `tests/test_deploy_assets.py`)
- R4. UI fidelity CSS changes preserve truthful-output behavior (no fake artifacts pre-run)
- R5. Parity register reflects P4/P5 resolution and P8 KB/code alignment

---

## Scope Boundaries

- Hosted HF Space E2E (P10) — follow-up after this PR lands
- Composer layout reorder (brief/upload before starters) — follow-up UI pass
- STRATEGY.md authorship — out of scope
- Committing `docs/ideation/` — optional, not required for slice

### Deferred to Follow-Up Work

- Hosted Block/Vase E2E validation and P10 evidence template
- Composer-above-fold layout reorder in `app.py`

---

## Key Technical Decisions

- **Fix corruption minimally:** Remove stray `7865` tokens; do not refactor deploy module structure
- **CSS-only UI fidelity:** Rail compaction and empty-state shrink stay in `_CSS`; no behavioral changes to export gating
- **Separate PR from doc-only #1:** Code slice opens new PR or expands scope on branch with clear test plan

---

## Implementation Units

- U1. **Fix deploy syntax blockers (P4/P5)**

**Goal:** Restore parseable deploy scripts.

**Requirements:** R1

**Dependencies:** None

**Files:**
- Modify: `scripts/render_deploy_assets.py`
- Modify: `src/imageezgen3d/deploy_assets.py`
- Test: `tests/test_deploy_assets.py`

**Test scenarios:**
- Happy path: `compileall` succeeds on both files
- Happy path: `test_deploy_assets` passes with `container_port=7865`

**Verification:**
- `python -m compileall -q scripts/render_deploy_assets.py src/imageezgen3d/deploy_assets.py` exits 0

---

- U2. **Re-render deploy templates**

**Goal:** Propagate port 7865 to rendered deploy outputs.

**Requirements:** R2

**Dependencies:** U1

**Files:**
- Modify: `deploy/helm/`, `deploy/kubernetes/`, `deploy/nomad/`, `deploy/podman/` (via render script)

**Test scenarios:**
- Happy path: rendered templates contain port 7865

**Verification:**
- Render script completes; grep deploy outputs for 7865

---

- U3. **Land UI fidelity CSS slice**

**Goal:** Compact rail headers, empty artifact states, Model3D empty selector fix.

**Requirements:** R4

**Dependencies:** None

**Files:**
- Modify: `app.py` (`_CSS` block)

**Test scenarios:**
- Happy path: `tests/test_app.py` passes including mode summary test
- Edge case: pre-run state shows no fake GLB/OBJ paths (manual/browser)

**Verification:**
- Unittests green; local app loads on configured port

---

- U4. **Update parity register**

**Goal:** Close P4/P5; note P8 partial alignment.

**Requirements:** R5

**Dependencies:** U1, U2, U3

**Files:**
- Modify: `docs/knowledgebase/40-operational-risk/source-runtime-parity-register.md`

**Test expectation:** none — documentation only

**Verification:**
- P4/P5 rows no longer BLOCKED; P10 remains OPEN

---

- U5. **Full validation gate**

**Goal:** CI-parity checks before PR.

**Requirements:** R3

**Dependencies:** U1–U4

**Files:**
- Test: `tests/`

**Test scenarios:**
- Happy path: full unittest discover passes
- Happy path: `check_python_style.py` passes

**Verification:**
- All validation commands exit 0

---

## Sources & References

- **Origin:** `docs/ideation/2026-05-23-next-focus-ideation.md`
- Parity register: `docs/knowledgebase/40-operational-risk/source-runtime-parity-register.md`
- UI checklist: `docs/knowledgebase/50-execution/ui-fidelity-implementation-checklist-2026-05-18.md`
- AGENTS.md hosted validation contract

---

### Delta Update (2026-05-23)

- **Landed:** P4/P5 deploy fixes, port 7865 slice, UI fidelity CSS, STRATEGY.md, dead hero-idea CSS removed (~70 lines)
- **Partial:** P10 hosted E2E `[OPEN]`; composer above-fold reorder deferred
- **Next:** HF deploy + Block/Vase E2E; composer layout reorder; export-guide audit
