---
title: "HF Space demo export and port 7860 binding"
date: 2026-05-24
category: tooling-decisions
problem_type: deployment
component: huggingface-spaces
symptoms:
  - Space stuck in APP_STARTING for minutes
  - Gradio logs show binding to port 7865 instead of platform port
  - GRADIO_HOT_RELOAD warning about demo not found in __main__
root_cause: App bound to local pyproject default port 7865; no module-level demo for Spaces Gradio launcher
solution: Export module-level demo = build_demo(); default launch port to 7860 when SPACE_ID set without port env vars; omit server_port in launch() on Spaces
commits:
  - e2f0708
related_docs:
  - docs/knowledgebase/deployment-hf-cli.md
  - docs/knowledgebase/40-operational-risk/hosted-validation-2026-05-23.md
applies_when:
  - Hugging Face Space stays APP_STARTING
  - Deploying Gradio app to hf.space
---

# HF Space demo export and port 7860 binding

## Problem

After staged deploy, Space remained `APP_STARTING`. Runtime logs showed Gradio on `http://0.0.0.0:7865` while HF health checks expect **7860**. Launcher also warned it could not find `demo` in `__main__`.

## Fix

1. **`app.py`:** `demo = build_demo()` at module scope; pass `server_port` to `launch()` only when not on Spaces.
2. **`config.py`:** `_resolve_launch_port()` returns **7860** when Space env markers are present and no `PORT` / `GRADIO_SERVER_PORT` / `IMAGEEZ_PORT` override.

## Verification

- Space reached `RUNNING` after deploy commit `3ad22d80`
- Hosted Block E2E run `20260524-084947-19c70f8f` on live Space

## Do not confuse with

- Local dev default port **7865** in `pyproject.toml` — still correct for local Gradio
- CI upload success — still requires browser/API E2E per `AGENTS.md`
