---
title: "feat: Hosted E2E validation and HF deploy best-practices KB"
type: feat
status: completed
date: 2026-05-23
origin: docs/ideation/2026-05-23-next-focus-ideation.md
---

# feat: Hosted E2E validation and HF deploy best-practices KB

## Summary

Close parity register P10 by executing the AGENTS.md hosted validation loop: HF CLI deploy, live Space Block/Vase E2E, evidence recorded in mode matrix template. Refresh `deployment-hf-cli.md` with current official HF CLI and Space best practices from docs-researcher and ce-best-practices-researcher findings.

---

## Problem Frame

P4/P5 deploy blockers and composer/KB slices are landed. The highest remaining trust gap is **unverified hosted runtime** (P10). AGENTS.md forbids claiming hosted success without browser E2E on a live `hf.space` app. Existing deployment runbook may lag current `hf` CLI and Space build-order guidance.

---

## Requirements

- R1. Deploy current branch to HF Space via `hf` CLI with minimal payload (exclude venv, outputs, caches)
- R2. Confirm Space loads without build error
- R3. Run Block or Vase sample end-to-end on live Space
- R4. Record evidence: run id, adapter/fallback, manifest + GLB + OBJ verified
- R5. Update parity register P1/P3/P10 and mode-validation matrix with dated evidence
- R6. Refresh `docs/knowledgebase/deployment-hf-cli.md` with `[OFFICIAL]`-labeled best practices (upload excludes, requirements-first, ZeroGPU constraints)
- R7. Commit ideation doc if still untracked and referenced by plan origin
- R8. Do not claim hosted ZeroGPU if CPU fallback ran

---

## Scope Boundaries

- Hunyuan adapter enablement — out of scope
- Automated CI attestation of hosted runs — deferred
- Helm/K8s deploy validation — deferred (P4 OK for templates only)

---

## Implementation Units

### U1. Research current HF deploy best practices

**Goal:** Ground deploy steps in current official docs.

**Requirements:** R6

**Agents:** docs-researcher, ce-best-practices-researcher

**Deliverable:** Evidence-labeled notes merged into deployment runbook refresh.

---

### U2. Preflight and deploy

**Goal:** Push minimal Space payload and confirm build starts.

**Requirements:** R1, R2

**Files:**
- Use: `scripts/hf_space_check.py`, `src/imageezgen3d/hf_cli.py`
- Verify: `requirements.txt`, `README.md` frontmatter, `.env.example`

**Test scenarios:**
- Happy path: `hf auth whoami` succeeds
- Happy path: upload excludes venv/outputs
- Failure: missing token → stop with actionable error (no false success claim)

---

### U3. Hosted E2E browser validation

**Goal:** Block or Vase generation on live Space.

**Requirements:** R3, R4, R8

**Verification:** mode-validation-matrix evidence template filled

---

### U4. KB and parity updates

**Goal:** Durable record of validation and refreshed runbook.

**Requirements:** R5, R6, R7

**Files:**
- Modify: `docs/knowledgebase/40-operational-risk/source-runtime-parity-register.md`
- Modify: `docs/knowledgebase/40-operational-risk/mode-validation-matrix.md` (evidence section or hosted record)
- Modify: `docs/knowledgebase/deployment-hf-cli.md`
- Add: `docs/knowledgebase/40-operational-risk/hosted-validation-2026-05-23.md` (evidence record)
- Modify: `docs/knowledgebase/README.md` (index link if new doc)
- Add: `docs/ideation/2026-05-23-next-focus-ideation.md` (if still untracked)

---

## Sources & References

- `AGENTS.md` hosted validation rules
- `docs/ideation/2026-05-23-next-focus-ideation.md` survivor #2
- `docs/knowledgebase/deployment-hf-cli.md`
- Official HF Spaces / ZeroGPU / `hf` CLI docs (via docs-researcher)

---

## Risks

- HF token unavailable → document blocker, do not claim P10 closed
- Space build failure → iterate fix/deploy loop until load succeeds or report blocker
- Long GPU queue on ZeroGPU → report actual mode (likely hosted CPU fallback)
