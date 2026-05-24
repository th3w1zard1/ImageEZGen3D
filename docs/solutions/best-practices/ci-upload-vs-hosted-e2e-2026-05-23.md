---
title: CI Space upload success is not hosted E2E validation
date: 2026-05-23
category: best-practices
module: verification
problem_type: best_practice
component: documentation
severity: high
applies_when:
  - "Reporting deploy or release validation status"
  - "hf-space.yml sync job succeeds"
  - "Closing parity register P10"
tags: [hosted-e2e, verification, hf-space, agents-md, honesty]
---

# CI Space upload success is not hosted E2E validation

## Context

`hf-space.yml` can upload staged files and trigger a Space rebuild without proving the live app loads, generates meshes, or reports honest adapter/fallback status. `AGENTS.md` requires browser validation on a live `hf.space` URL.

## Guidance

| Check | Proves | Does **not** prove |
|-------|--------|-------------------|
| `hf-space.yml` sync green | Files reached Hub; build may start | App loads; Block/Vase E2E; artifact downloads |
| Local unittest + Gradio smoke | Local CPU path | Hosted runtime |
| Browser on live Space + sample run | Hosted mode per matrix | — |

**Reporting rules:**

1. Name the mode from [mode-validation-matrix.md](../../knowledgebase/40-operational-risk/mode-validation-matrix.md)
2. Use Block or Vase unless task requires another built-in sample
3. Record run id, adapter/fallback, manifest + GLB + OBJ in evidence template
4. Hosted CPU fallback success is **not** ZeroGPU validation

## Why This Matters

Claiming "deploy validated" after CI upload alone violates the agent operating contract and leaves P10 open while looking green in GitHub Actions.

## When to Apply

- Every PR touching Gradio, exports, runtime, or deploy workflows
- Before closing parity register P10
- After adding tag-triggered deploys (upload still ≠ E2E)

## Examples

**Wrong:** "HF Space deploy validated — hf-space.yml passed."

**Right:** "HF Space CI upload succeeded (P11 OK). Hosted E2E `[OPEN]` — Block sample not run on live Space yet."

## Related

- `AGENTS.md` §Runtime and Deployment Validation
- `docs/knowledgebase/40-operational-risk/mode-validation-matrix.md`
- `docs/plans/2026-05-23-005-feat-hosted-e2e-best-practices-plan.md` — execution still pending
