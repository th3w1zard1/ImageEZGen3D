---
title: "feat: Ship PR #45 + enablement preflight on scheduled hosted smoke"
type: feat
status: completed
date: 2026-05-27
origin: docs/plans/2026-05-27-063-feat-ship-pr44-enablement-preflight-plan.md
---

# feat: Ship PR #45 + enablement preflight on scheduled hosted smoke

## Summary

Squash-merge PR #45 (unified enablement preflight), then record enablement snapshot JSON on scheduled hosted smoke and document the command in AGENTS.md.

## Requirements

- R1. Squash-merge PR #45
- R2. `hunyuan_enablement_preflight.py --record` for CI artifacts
- R3. `hosted-golden-smoke.yml` runs enablement preflight + uploads JSON
- R4. `AGENTS.md` + `hunyuan-enablement-preflight.md` pointer doc
- R5. Tests; hosted golden smoke still passes

## Scope boundaries

- Do not enable Hunyuan adapter
- Do not claim G7 closed

## Files

- Modify: `scripts/hunyuan_enablement_preflight.py`
- Modify: `.github/workflows/hosted-golden-smoke.yml`
- Modify: `AGENTS.md`, `tests/test_workflows.py`
- Add: `docs/knowledgebase/hunyuan-enablement-preflight.md`
