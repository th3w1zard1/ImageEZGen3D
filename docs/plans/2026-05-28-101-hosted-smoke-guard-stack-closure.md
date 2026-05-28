---
title: Hosted smoke guard stack closure (Plan 101)
status: completed
created: 2026-05-28
---

# Plan 101 — Close hosted smoke guard stack (Plans 078–100)

## Problem

Plans 078–100 landed G7 false-neural guard, per-artifact JSON verify CLIs, bundle verify, and G7 live-probe verify on `main`, but agents must jump across four solutions docs. Ideation is stale (missing PR #66 / Plans 099–100). `verify_hosted_smoke_artifacts.py` lacks a subprocess exit-1 contract test.

## Scope

- Add `docs/solutions/best-practices/hosted-smoke-guard-stack-2026-05-28.md` indexing the full scheduled-smoke verify chain.
- README index row; extend `AGENTS.md` with `verify_hosted_smoke_artifacts.py` and stack doc link.
- Negative subprocess test in `tests/test_hosted_smoke_artifacts.py`.
- Refresh ideation completed list (PR #66, Plans 097–100) and guardrail-track note.
- KB Plan 101 section in `hosted-validation-2026-05-23.md`.

## Out of scope

- Hunyuan enablement or G7 gate closure.

## Test scenarios

1. Subprocess: invalid golden record → `verify_hosted_smoke_artifacts.py` exits 1.
2. Stack solutions doc links golden, export-tier, G7 guard, G7 live-probe learnings.

## Files

- `docs/plans/2026-05-28-101-hosted-smoke-guard-stack-closure.md`
- `docs/solutions/best-practices/hosted-smoke-guard-stack-2026-05-28.md`
- `docs/solutions/README.md`
- `AGENTS.md`
- `tests/test_hosted_smoke_artifacts.py`
- `docs/ideation/2026-05-24-post-trust-slice-refresh.md`
- `docs/knowledgebase/40-operational-risk/hosted-validation-2026-05-23.md`
