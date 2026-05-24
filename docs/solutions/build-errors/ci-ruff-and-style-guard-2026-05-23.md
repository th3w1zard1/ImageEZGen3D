---
title: CI ruff F401 and Python style guard failures on PR
date: 2026-05-23
category: build-errors
module: ci
problem_type: build_error
component: testing_framework
symptoms:
  - "CI / lint fails with ruff F401 unused import"
  - "CI / test matrix fails on scripts/check_python_style.py"
root_cause: incomplete_setup
resolution_type: code_fix
severity: medium
tags: [ci, ruff, lint, style-guard, future-annotations]
---

# CI ruff F401 and Python style guard failures on PR

## Problem

PR #1 CI failed on lint and all Python version test jobs despite unittest passing locally. Lint reported an unused import; style guard rejected four root-level scripts.

## Symptoms

- `[REPO]` **CI / lint:** `ruff` F401 — unused import `zero_gpu_runtime_available` in `src/imageezgen3d/orchestrator.py:15`
- `[REPO]` **CI / test (3.10–3.14):** `scripts/check_python_style.py` failed because these files lacked `from __future__ import annotations` as the **first** line:
  - `fix_cpu_demo.py`
  - `fix_gltf.py`
  - `fix_uvs.py`
  - `update_exporters.py`

## What Didn't Work

- Assuming unittest green meant CI green — style guard runs after tests in the workflow
- Adding future import below docstrings or imports — guard requires line 1

## Solution

1. Remove unused import from `orchestrator.py`
2. Add `from __future__ import annotations` as first line in each failing root script

Commit: `7605a13` — `fix(ci): resolve lint and style-check failures on PR #1`

## Why This Works

Ruff F401 is strict about imports that are never referenced. The style guard enforces a repo-wide convention that every Python file under tracked paths starts with future annotations for consistent typing behavior.

## Prevention

- Run before push:

```bash
ruff check src tests scripts
PYTHONPATH=src python scripts/check_python_style.py
```

- When adding root-level scripts, put future annotations on line 1
- Remove imports when refactoring removes their use sites

## Related

- `.github/workflows/ci.yml`
- `docs/knowledgebase/verification.md` §Narrow Automated Checks
