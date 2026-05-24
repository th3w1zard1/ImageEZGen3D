---
title: "feat: Bootstrap docs/solutions institutional learnings store"
type: feat
status: completed
date: 2026-05-23
origin: /ce-learnings-researcher — docs/solutions/ empty; compound recent session work
---

# feat: Bootstrap docs/solutions institutional learnings store

## Summary

Create `docs/solutions/` with YAML-frontmatter learning docs compound from recent ImageEZGen3D work (CI fixes, HF staged deploy, port env chain, CI vs E2E honesty). Wire discoverability into `AGENTS.md` and KB index so `ce-learnings-researcher` and LFG passes find institutional memory on the next invocation.

---

## Problem Frame

`[REPO]` Ideation doc and KB both note: **no `docs/solutions/` directory**. Institutional direction lives in KB plans and runbooks, but solved problems from commits `7605a13`, `904beb1`, and `997ff19` are not searchable by frontmatter. `ce-learnings-researcher` returns empty on every pass until this store exists.

---

## Requirements

- R1. Create `docs/solutions/` with category subdirs per ce-compound schema
- R2. Add ≥4 learning docs with valid YAML frontmatter (bug + knowledge tracks)
- R3. Add `docs/solutions/README.md` index with search guidance
- R4. Update `AGENTS.md` to reference `docs/solutions/` before implementing deploy/CI/runtime changes
- R5. Link solutions store from `docs/knowledgebase/README.md` and `50-execution/ideation-to-pr-pipeline.md`
- R6. Do not duplicate full KB runbooks — solutions are concise compound artifacts with pointers to KB authority docs

---

## Scope Boundaries

- Hosted E2E execution (plan 005) — out of scope; document as `[OPEN]` in applies_when
- No hosted validation evidence claims

---

## Implementation Units

### U1. CI lint/style learning (bug track)

**Source:** commit `7605a13`, PR #1 CI failures

**File:** `docs/solutions/build-errors/ci-ruff-and-style-guard-2026-05-23.md`

**Topics:** F401 unused import; `check_python_style.py` requires `from __future__ import annotations` as first line in root scripts

---

### U2. HF staged payload CI deploy (knowledge track)

**Source:** commits `904beb1`, plan 006

**File:** `docs/solutions/architecture-patterns/hf-space-staged-payload-ci-deploy-2026-05-23.md`

**Topics:** `hf-space.yml` branch + `v*` tag triggers; `stage_space_payload()`; legacy `sync-hf-space.yml` manual-only

---

### U3. CI upload vs hosted E2E (knowledge track)

**Source:** plan 007, mode matrix update

**File:** `docs/solutions/best-practices/ci-upload-vs-hosted-e2e-2026-05-23.md`

---

### U4. Gradio port env precedence on Spaces (knowledge track)

**Source:** commit `904beb1`, `config.py`

**File:** `docs/solutions/tooling-decisions/gradio-port-env-precedence-2026-05-23.md`

---

### U5. Discoverability wiring

**Files:** `docs/solutions/README.md`, `AGENTS.md`, `docs/knowledgebase/README.md`, `docs/knowledgebase/50-execution/ideation-to-pr-pipeline.md`

---

## Validation

- Frontmatter enums match `ce-compound` schema
- `git diff --check` clean
- Grep `docs/solutions/` returns ≥4 files with `problem_type:`

## Sources

- ce-learnings-researcher gap analysis (empty store)
- commits `7605a13`, `904beb1`, `997ff19`
- `docs/knowledgebase/10-architecture-runtime/release-deploy-surfaces.md`
