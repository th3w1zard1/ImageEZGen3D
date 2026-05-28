---
title: G7 false-neural guard institutional learning (Plan 081)
status: completed
created: 2026-05-28
---

# Plan 081 — Compound learning for G7 golden smoke guard

## Problem

Plan 080 adds `validate_g7_not_false_neural_claim` to hosted golden smoke, but there is no `docs/solutions/` entry for agents to find before changing smoke or G7 validators.

## Scope

- Add `docs/solutions/best-practices/g7-false-neural-golden-smoke-guard-2026-05-28.md` with frontmatter.
- Index it in `docs/solutions/README.md`.
- One-line pointer in `AGENTS.md` under hosted validation / Hunyuan preflight.

## Out of scope

- Hunyuan enablement, workflow changes, merging PRs #58/#59.

## Test scenarios

1. Solution doc frontmatter valid; README index links resolve.
2. No code regressions; `tests.test_hosted_golden_smoke` still passes on branch.
