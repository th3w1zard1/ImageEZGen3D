---
title: "feat: Knowledgebase refresh after release deploy and port fixes"
type: feat
status: active
date: 2026-05-23
origin: /build-knowledgebase + plans 005/006 landed context
---

# feat: Knowledgebase refresh after release deploy and port fixes

## Summary

Refresh the ImageEZGen3D knowledgebase to reflect landed work from plans 005–006: HF Space auto-deploy on default branch and `v*` tags, hosted port env precedence (`PORT` → `GRADIO_SERVER_PORT` → `IMAGEEZ_PORT`), and `STRATEGY.md` as a product anchor. Close documentation drift in parity register, configuration guide, and KB index without claiming hosted E2E validation that has not executed.

---

## Problem Frame

Plan 001 established KB index, parity register, and mode matrix. Since then, code landed for HF release-tag CI deploy, staged Space payload hygiene, and Gradio port binding — but parity register rows P1/P3 still describe an unverified 7865-only story, `configuration.md` omits the new env chain, and the index caveats are stale. Ideation and plan 005 remain untracked. A build-knowledgebase pass must reconcile docs with repo evidence while preserving `[OPEN]` honesty for P10 hosted E2E.

---

## Requirements

- R1. Update `source-runtime-parity-register.md` for port env precedence and HF CI deploy surface
- R2. Document port precedence in `configuration.md` with `[REPO]` evidence
- R3. Add `10-architecture-runtime/release-deploy-surfaces.md` covering branch/tag HF deploy, staged payload, legacy sync escape hatch
- R4. Refresh `README.md` index: link `STRATEGY.md`, new runtime doc, updated caveats
- R5. Update `project-intent.md` to reference `STRATEGY.md` and recent deploy automation
- R6. Clarify in `verification.md` or mode matrix that CI Space upload ≠ hosted E2E validation
- R7. Track untracked `docs/ideation/` and plan 005 in repo
- R8. All claims use evidence labels; hosted ZeroGPU/E2E remain `[OPEN]`

---

## Scope Boundaries

- No hosted browser E2E execution in this pass
- No mass migration of flat KB files into numbered folders
- No adapter enablement documentation beyond existing gates

### Deferred to Follow-Up Work

- Plan 005 hosted E2E execution and evidence template fill
- Full taxonomy migration of 24 flat KB files
- Evidence-label retrofit across all legacy docs

---

## Key Technical Decisions

- **New doc under `10-architecture-runtime/`** rather than bloating `release-automation.md` — separates CI contract from operator CLI runbook
- **Parity register additive rows** for HF CI deploy (P11) instead of overloading P10
- **Do not close P10** until Block/Vase E2E on live Space

---

## Implementation Units

### U1. Parity register refresh

**Requirements:** R1

**Files:** `docs/knowledgebase/40-operational-risk/source-runtime-parity-register.md`

**Changes:**
- P1: note `config.py` honors `PORT` / `GRADIO_SERVER_PORT` / `IMAGEEZ_PORT` / pyproject default
- Add P11: HF Space CI deploy via `hf-space.yml` (branch + `v*` tag, staged payload)
- Update caveats: local browser smoke only; P10 still open

---

### U2. Configuration port precedence

**Requirements:** R2

**Files:** `docs/knowledgebase/configuration.md`

**Changes:** Document launch port env chain with `[REPO]` citation to `config.py`

---

### U3. Release deploy surfaces doc

**Requirements:** R3

**Files:** `docs/knowledgebase/10-architecture-runtime/release-deploy-surfaces.md` (new)

**Content:** Branch/tag triggers, `hf_space_sync.py` staged payload, `sync-hf-space.yml` manual-only, secrets, relationship to `deployment-hf-cli.md`

---

### U4. KB index and intent updates

**Requirements:** R4, R5

**Files:** `docs/knowledgebase/README.md`, `docs/knowledgebase/project-intent.md`

---

### U5. Verification honesty note

**Requirements:** R6

**Files:** `docs/knowledgebase/40-operational-risk/mode-validation-matrix.md`

**Changes:** CI upload success does not satisfy hosted E2E row

---

### U6. Track ideation and plan 005

**Requirements:** R7

**Files:** `docs/ideation/2026-05-23-next-focus-ideation.md`, `docs/plans/2026-05-23-005-feat-hosted-e2e-best-practices-plan.md`

---

## Validation

- `git diff --check` on all markdown changes
- No `[OFFICIAL]` claims without source
- P10 remains `[OPEN]`

## Sources

- `docs/plans/2026-05-23-006-feat-hf-space-release-auto-deploy-plan.md`
- `docs/plans/2026-05-23-005-feat-hosted-e2e-best-practices-plan.md`
- `STRATEGY.md`, `src/imageezgen3d/config.py`, `.github/workflows/hf-space.yml`
