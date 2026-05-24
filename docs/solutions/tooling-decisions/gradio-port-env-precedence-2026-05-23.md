---
title: Gradio port environment precedence for Hugging Face Spaces
date: 2026-05-23
category: tooling-decisions
module: configuration
problem_type: tooling_decision
component: development_workflow
severity: medium
applies_when:
  - "Space stuck in APP_STARTING"
  - "Binding Gradio on Hugging Face Spaces vs local dev"
  - "Hardcoded port in app launch"
tags: [gradio, port, hf-space, gradio-server-port, config]
---

# Gradio port environment precedence for Hugging Face Spaces

## Context

Local default port is **7865** in `pyproject.toml`. Hugging Face Gradio Spaces inject `GRADIO_SERVER_PORT` (commonly 7860). Hardcoding local port caused hosted apps to listen on the wrong interface/port and remain in `APP_STARTING`.

## Guidance

`[REPO]` `load_config()` resolves launch port in order:

1. `PORT`
2. `GRADIO_SERVER_PORT`
3. `IMAGEEZ_PORT`
4. `[tool.imageezgen3d.app].port` (pyproject default **7865**)

Always launch Gradio with `load_config().launch.port` — never a literal port constant in `app.py`.

## Why This Matters

Dockerfile `EXPOSE 7865` applies to container images; hosted Spaces override via platform env. Parity register P1/P3 stay `[OPEN]` until live Space binding is confirmed in browser E2E.

## When to Apply

- Changing launch code or Dockerfile ports
- Debugging Space startup failures
- Writing deploy docs — distinguish local default from hosted injection

## Examples

**Before:** App always bound to 7865; Space expected 7860.

**After (commit `904beb1`):** Config reads `GRADIO_SERVER_PORT` when present.

## Related

- `src/imageezgen3d/config.py`
- `docs/knowledgebase/configuration.md` §Launch
- `tests/test_config.py` — port precedence tests
- `docs/knowledgebase/deployment-hf-cli.md` §Port And Launch
