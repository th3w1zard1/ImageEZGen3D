---
title: Hugging Face Space staged payload CI deploy
date: 2026-05-23
category: architecture-patterns
module: release-automation
problem_type: architecture_pattern
component: tooling
severity: high
applies_when:
  - "Automating Hugging Face Space uploads from GitHub Actions"
  - "Avoiding full-repo mirror timeouts and junk files on Spaces"
  - "Shipping on default branch merge or v* release tag"
tags: [hf-space, ci, staged-payload, release, huggingface]
---

# Hugging Face Space staged payload CI deploy

## Context

ImageEZGen3D had two competing Space deploy paths: a full-repo mirror (`sync-hf-space.yml` + `huggingface/hub-sync`) and a minimal staged upload. Full mirror risked uploading venvs, docs, tests, and outputs. Release tag pushes did not trigger Space updates.

## Guidance

**Single automatic path:** `.github/workflows/hf-space.yml`

| Trigger | Behavior |
|---------|----------|
| Push `main`/`master` | Plan + sync when `HF_TOKEN` set |
| Push tag `v*` | Same staged upload; commit message includes tag |
| Pull request | Plan/summary only — no Space mutation |
| `workflow_dispatch` | Manual sync |

**Execution chain:**

1. `release_workflow_outputs.py` → `huggingface_action=push` when credentialed
2. `hf_space_sync.py --execute` → `stage_space_payload()` → `hf upload` with `--delete` patterns
3. Tag builds use `deploy_commit_message()` → `Deploy ImageEZGen3D v1.2.3`

**Legacy escape hatch:** `sync-hf-space.yml` is **manual dispatch only** — do not re-enable automatic push on `main`.

## Why This Matters

- Aligns with `AGENTS.md` Space payload hygiene
- `[OFFICIAL]` Spaces install `requirements.txt` before source copy — staged payload keeps requirements self-contained
- One workflow owns one deliverable (see `release-automation.md`)

## When to Apply

- Adding new CI deploy triggers → extend `hf-space.yml`, not a second mirror workflow
- Local dry-run before workflow edits: `PYTHONPATH=src python scripts/hf_space_sync.py`

## Examples

**Before (problem):** Two workflows; tag release did not refresh Space; full mirror uploaded `.venv/` and `docs/`.

**After (commit `904beb1`):** Tag trigger + staged dir only; legacy mirror manual.

## Related

- `docs/knowledgebase/10-architecture-runtime/release-deploy-surfaces.md`
- `docs/plans/2026-05-23-006-feat-hf-space-release-auto-deploy-plan.md`
- `src/imageezgen3d/hf_cli.py` — `stage_space_payload`, `deploy_commit_message`
