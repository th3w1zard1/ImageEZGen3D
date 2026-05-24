---
title: "feat: Knowledgebase orchestration pass"
type: feat
status: completed
date: 2026-05-23
origin: ce-ideate + kb-orchestrator + kb-repo-archaeologist synthesis
---

# feat: Knowledgebase orchestration pass

## Summary

Expand ImageEZGen3D's knowledgebase with a navigable index, agent operating contract, source-runtime parity register, mode-specific validation matrix, and ideation-to-PR pipeline doc — then refresh stale intent claims. This pass is documentation-only; it reconciles KB authority with `AGENTS.md`, recent UI/export changes, and the partially adopted layered taxonomy.

---

## Problem Frame

The repo has 27 KB documents but only three live in numbered taxonomy folders. `project-intent.md` is stale (denies `AGENTS.md`), navigation relies on ad hoc cross-links, and drift between source, deploy assets, and hosted validation is named but not tracked. Agents and implementers need a single-pass KB refresh that compounds into the ideation → plan → implement → review → PR workflow.

---

## Requirements

- R1. Add `docs/knowledgebase/README.md` as the canonical index mapping all docs to taxonomy layers with purpose and authority hints.
- R2. Add `docs/knowledgebase/00-intent/agent-operating-contract.md` unifying `AGENTS.md`, evidence labels, and mode-specific reporting.
- R3. Add `docs/knowledgebase/40-operational-risk/source-runtime-parity-register.md` as a living drift log with initial rows for config, deploy, and KB surfaces.
- R4. Extend validation coverage via `docs/knowledgebase/40-operational-risk/mode-validation-matrix.md` distinguishing local CPU, local GPU, hosted CPU fallback, and hosted ZeroGPU.
- R5. Add `docs/knowledgebase/50-execution/ideation-to-pr-pipeline.md` mapping CE skills to KB entry/exit criteria.
- R6. Update `docs/knowledgebase/project-intent.md` to acknowledge `AGENTS.md`, refresh Source Basis, and link new authority docs.

---

## Scope Boundaries

- No mass rename/move of 24 flat KB files in this pass (index links only).
- No adapter enablement or Hunyuan implementation docs beyond pointers.
- No hosted Space browser validation execution in this pass — mark unverified surfaces `[OPEN]`.
- No code changes to `app.py`, exporters, or deploy assets unless required for doc accuracy citations only.

### Deferred to Follow-Up Work

- Full taxonomy migration of flat docs into numbered folders: separate pass after index stabilizes.
- Evidence-label retrofit across all 22 legacy docs: follow-on curation pass.
- `10-architecture-runtime/export-artifact-contract.md`: after exporters diff lands.

---

## Context & Research

### Relevant Code and Patterns

- `docs/knowledgebase/knowledgebase-authoring-playbook.md` — evidence labels, taxonomy, source priority
- `docs/knowledgebase/knowledgebase-builder-agent-spec.md` — builder contract, validation minimums
- `AGENTS.md` — hosted validation DoD, mode reporting, Space payload hygiene
- `docs/knowledgebase/verification.md` — local validation ladder
- `docs/knowledgebase/project-intent.md` — current intent anchor (stale on AGENTS.md)

### Institutional Learnings

- Partial taxonomy adoption: `00-intent/`, `30-product-ux/`, `50-execution/` each have one dated slice
- Two evidence formats coexist: prose Source Basis vs bracket tags

### External References

- Gradio/HF Spaces/ZeroGPU: defer to existing `zerogpu-runtime.md`, `deployment-hf-cli.md` unless drift detected

---

## Key Technical Decisions

- **Index-first, migrate-later:** Create `README.md` with layer map linking flat files by path rather than renaming 24 files in one PR.
- **Operational risk home for parity + validation:** Place parity register and mode matrix under `40-operational-risk/` per playbook taxonomy.
- **Cross-link, don't duplicate AGENTS.md:** Agent operating contract expands with evidence labels and pipeline hooks; `AGENTS.md` stays the live agent runbook.
- **Mark unverified hosted paths `[OPEN]`:** Do not claim Space validation without executed evidence.

---

## Open Questions

### Resolved During Planning

- **Which six docs for one pass?** Merged kb-orchestrator priority list with ce-ideate top 5; adapter runbook deferred to keep pass focused on navigation + validation authority.
- **Taxonomy migration scope?** Index links only; physical moves deferred.

### Deferred to Implementation

- Whether port 7865 is deployed on live HF Space: record in parity register as `[OPEN]`.
- Whether `deploy_assets.py` corruption affects rendered templates: verify during parity register seeding.

---

## Implementation Units

- U1. **KB index and taxonomy map**

**Goal:** Provide navigable authority map for all 27+ KB documents.

**Requirements:** R1

**Dependencies:** None

**Files:**
- Create: `docs/knowledgebase/README.md`

**Approach:**
- Map docs to playbook layers (00-intent through 90-meta)
- One-line purpose per doc; mark canonical vs dated-slice vs frontier
- Link to new authority docs (U2–U5)

**Patterns to follow:**
- `docs/knowledgebase/knowledgebase-builder-agent-spec.md` index requirement
- `docs/knowledgebase/project-intent.md` companion doc lists

**Test scenarios:**
- Happy path: every existing KB file appears in index with layer assignment
- Edge case: dated slices (`*-2026-05-18`) marked with authority rank

**Verification:**
- No broken relative links from README to listed docs
- `git diff --check` clean

---

- U2. **Agent operating contract**

**Goal:** Unify agent-facing rules with KB evidence discipline.

**Requirements:** R2

**Dependencies:** U1

**Files:**
- Create: `docs/knowledgebase/00-intent/agent-operating-contract.md`

**Approach:**
- Source basis listing `AGENTS.md`, playbook, verification.md
- Evidence label contract; source priority; mode-specific reporting table
- Cross-link to parity register and mode matrix

**Patterns to follow:**
- `AGENTS.md`
- `docs/knowledgebase/knowledgebase-authoring-playbook.md`

**Test scenarios:**
- Happy path: all AGENTS.md hosted-validation bullets represented or cross-linked
- Integration: contract links to verification ladder and parity register

**Verification:**
- Every substantive claim has `[REPO]` or `[OFFICIAL]` label
- Links resolve from README (U1)

---

- U3. **Source-runtime parity register**

**Goal:** Operational drift log for config/deploy/KB/hosted surfaces.

**Requirements:** R3

**Dependencies:** U1

**Files:**
- Create: `docs/knowledgebase/40-operational-risk/source-runtime-parity-register.md`

**Approach:**
- Table: surface, source of truth, last verified, observed delta, action, status
- Seed rows: pyproject port 7865, Dockerfile, .env.example, deploy_assets, AGENTS.md vs project-intent, requirements.txt vs pyproject
- Mark unverified hosted Space as `[OPEN]`

**Patterns to follow:**
- `docs/knowledgebase/verification.md` §Source-Versus-Runtime Parity
- Playbook gotcha on drift

**Test scenarios:**
- Happy path: at least 8 parity surfaces documented with owner action
- Edge case: in-flight uncommitted diff (`deploy_assets.py`) noted with `[OPEN]`

**Verification:**
- Register cites repo paths for each surface
- No unlabeled factual claims

---

- U4. **Mode-specific validation matrix**

**Goal:** Four-mode honesty matrix for validation reporting.

**Requirements:** R4

**Dependencies:** U2

**Files:**
- Create: `docs/knowledgebase/40-operational-risk/mode-validation-matrix.md`

**Approach:**
- Matrix rows: local CPU, local GPU, hosted CPU fallback, hosted ZeroGPU
- Columns: required checks, honest reporting rules, do-not-claim boundaries, sample inputs (Block/Vase)
- Hosted E2E evidence template as appendix section

**Patterns to follow:**
- `AGENTS.md` §Mode-Specific Reporting
- `docs/knowledgebase/verification.md`

**Test scenarios:**
- Happy path: each mode has explicit "do not claim validated when…" language
- Integration: cross-link from agent operating contract (U2)

**Verification:**
- Matrix distinguishes fallback success from ZeroGPU validation
- Template includes run id, adapter, fallback reason, artifact checklist fields

---

- U5. **Ideation-to-PR pipeline doc**

**Goal:** Map CE workflow stages to KB entry/exit criteria.

**Requirements:** R5

**Dependencies:** U1, U2

**Files:**
- Create: `docs/knowledgebase/50-execution/ideation-to-pr-pipeline.md`

**Approach:**
- Table: stage (ideate, brainstorm, plan, work, review, test, PR), skill, entry artifact, exit criteria, KB doc pointers (≤3 each)
- Note LFG pipeline ordering and residual handoff expectations

**Patterns to follow:**
- `docs/knowledgebase/knowledgebase-builder-agent-spec.md`
- kb-orchestrator pipeline mapping

**Test scenarios:**
- Happy path: each stage links to at most 3 KB docs
- Integration: review stage points to verification + failure modes + mode matrix

**Verification:**
- All linked KB paths exist
- Pipeline doc listed in README index

---

- U6. **Refresh project-intent.md**

**Goal:** Fix stale authority claims and link new docs.

**Requirements:** R6

**Dependencies:** U1–U5

**Files:**
- Modify: `docs/knowledgebase/project-intent.md`

**Approach:**
- Update Source Basis: acknowledge `AGENTS.md`, note multi-commit history
- Add links to README, agent operating contract, parity register, mode matrix, pipeline doc
- Refresh non-goals if needed for textured CPU demo boundary (cite `[REPO]` only if confirmed in code)

**Patterns to follow:**
- Existing project-intent structure (Source Basis, companion docs sections)

**Test scenarios:**
- Happy path: no claim that AGENTS.md is absent
- Edge case: shallow-history caveat preserved where still accurate

**Verification:**
- `git diff --check` clean
- New docs linked from intent doc

---

## System-Wide Impact

- **Interaction graph:** KB index becomes navigation entry for agents, ce-plan, ce-work, and review personas
- **Unchanged invariants:** Application code, tests, CI workflows — doc-only pass
- **API surface parity:** N/A (no code API changes)

---

## Risks & Dependencies

| Risk | Mitigation |
|------|------------|
| Docs describe in-flight uncommitted code inaccurately | Cite `[OPEN]` for unverified; reference file paths not behavior claims where diff is active |
| Index rot as flat files remain | README is single authority; defer physical migration |
| Over-claiming hosted validation | Mode matrix + parity register enforce honest reporting |

---

## Documentation / Operational Notes

- Run `git diff --check` on all touched markdown before declaring complete
- No pytest required (doc-only); validation ladder step 1 applies

---

## Sources & References

- **Origin synthesis:** ce-ideate, kb-orchestrator, kb-repo-archaeologist agent outputs (2026-05-23)
- Related code: `AGENTS.md`, `pyproject.toml`, `docs/knowledgebase/`
- Related docs: `knowledgebase-authoring-playbook.md`, `verification.md`
