---
title: "feat: Hunyuan admission audit in hosted golden smoke workflow"
type: feat
status: completed
date: 2026-05-24
origin: docs/plans/2026-05-24-043-feat-ship-pr25-hunyuan-ci-gate-main-plan.md
---

# feat: Hunyuan admission audit in hosted golden smoke workflow

## Summary

Merge PR #26 (Plan 043 docs), run Hunyuan admission audit in the scheduled `hosted-golden-smoke` workflow alongside golden and export-tier smokes, and document the check in `AGENTS.md`.

## Requirements

- R0. Squash-merge PR #26; sync `main`
- R1. `hosted-golden-smoke.yml` runs `scripts/hunyuan_admission_audit.py --json` and uploads `hunyuan-admission-audit.json`
- R2. `AGENTS.md` notes admission audit in hosted/CI validation path
- R3. `tests/test_workflows.py` or extend existing test — assert workflow contains admission audit step
- R4. 116+ tests pass; ruff clean
- R5. Mark Plan 044 `status: completed`

## Scope Boundaries

- Hunyuan enablement — deferred
- No Space redeploy required

## Files

- Modify: `.github/workflows/hosted-golden-smoke.yml`
- Modify: `AGENTS.md`
- Add or modify: `tests/test_workflows.py`
