---
title: "feat: Ship PR #38 + hosted golden smoke backend rail assertion"
type: feat
status: completed
date: 2026-05-27
origin: docs/plans/2026-05-27-056-feat-ship-pr37-backend-rail-deploy-main-plan.md
---

# feat: Ship PR #38 + hosted golden smoke backend rail assertion

## Summary

Merge PR #38 (Plan 056 deploy docs), then add hosted golden smoke validation that `/generate` returns Project Rail HTML containing **What backend ran** (product-driven follow-up from Plan 055).

## Requirements

- R1. Squash-merge PR #38
- R2. `validate_backend_rail_html()` + check generate output index 15
- R3. Unit tests (no live network in unit tests)
- R4. `unittest discover` + optional live smoke
- R5. Plan 057 KB section; mark completed

## Scope Boundaries

- G7 Hunyuan enablement — deferred
- Space redeploy — only if smoke fails on stale Space (chip already deployed in Plan 056)

## Files

- Modify: `src/imageezgen3d/hosted_golden_smoke.py`
- Modify: `tests/test_hosted_golden_smoke.py`
- Modify: `docs/knowledgebase/40-operational-risk/hosted-validation-2026-05-23.md`

## Test scenarios

- `validate_backend_rail_html` accepts chip HTML, rejects missing marker
- Mocked `run_hosted_golden_smoke` includes rail check when result tuple long enough
