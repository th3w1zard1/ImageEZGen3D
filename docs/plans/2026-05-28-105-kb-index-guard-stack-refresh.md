---
title: KB index refresh for hosted smoke guard stack (Plan 105)
status: completed
created: 2026-05-28
---

# Plan 105 — Knowledgebase index refresh (Plans 078–104)

## Problem

`docs/knowledgebase/README.md` last updated 2026-05-23 and omits Hunyuan G7 preflight, enablement runbook, and the hosted smoke guard stack (Plans 078–104 on `main`). Agents starting from the index miss P14 and solutions stack guidance.

## Scope

- Refresh index **Last updated**, quick entry for guard stack + Hunyuan preflight.
- Add layer rows for `hunyuan-g7-preflight.md`, `hunyuan-g9-enablement-runbook.md`.
- Update caveats: scheduled smoke guard stack on `main`; G7 still OPEN.
- KB Plan 105 note in `hosted-validation-2026-05-23.md`.

## Out of scope

- Hunyuan enablement or physical KB file moves.

## Test scenarios

1. Index links to `hosted-smoke-guard-stack-2026-05-28.md` and `hunyuan-admission-gates.md`.
2. Caveats distinguish golden CI vs scheduled smoke vs G7 closure.

## Files

- `docs/plans/2026-05-28-105-kb-index-guard-stack-refresh.md`
- `docs/knowledgebase/README.md`
- `docs/knowledgebase/40-operational-risk/hosted-validation-2026-05-23.md`
