---
title: ImageEZGen3D
emoji: 🧊
colorFrom: green
colorTo: indigo
sdk: gradio
sdk_version: 6.1.0
app_file: app.py
pinned: false
---

## Overview

ImageEZGen3D is a ZeroGPU-first Gradio image-to-3D workspace scaffold. It prefers Hugging Face ZeroGPU when that runtime and an enabled GPU adapter are available, and falls back to the CPU demo path only when ZeroGPU is not selected, not available, or not fully configured.

The design leaves clean adapter slots for heavier Hunyuan3D, TRELLIS, and Pixal3D style backends without making local development depend on CUDA, native compilation, model weights, or Hugging Face ZeroGPU quota.

## Current Capabilities

- Single-image and labeled multi-view intake in one page.
- Input validation for resolution, blur/soft focus risk, alpha/background, crop, and likely material risks.
- Per-run output folders with manifests and atomic writes to avoid data loss during conversion.
- Auto backend selection: ZeroGPU first, CPU fallback with an explicit manifest reason.
- CPU demo generation with valid `.glb`, `.obj`, `.ply`, and `.stl` artifacts.
- Inline Gradio `Model3D` preview path for supported environments.
- Knowledgebase docs for capture, failure modes, model/license decisions, exports, deployment, and verification.
- `hf` CLI deployment runbook without storing tokens in source.

## Local Setup

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
python -m pip install -e ".[app]"
cp .env.example .env
python app.py
```

If you only want to run the standard-library-heavy tests:

```bash
PYTHONPATH=src python -m unittest discover -s tests
```

## Configuration

`pyproject.toml` is the source of truth for app defaults, launch settings, dependency metadata, Pyright analysis settings, runtime strategy, ZeroGPU behavior, preprocessing thresholds, export formats, and storage limits. `.env` is a local override file generated from `.env.example` and is ignored by git.

See [docs/knowledgebase/configuration.md](docs/knowledgebase/configuration.md).

## Hugging Face Spaces / ZeroGPU Notes

ZeroGPU is Gradio-only and GPU access must be isolated behind `@spaces.GPU` decorated functions. This scaffold keeps CPU preprocessing, storage, validation, and export integrity outside GPU sections. The default backend is `auto`: it tries the configured ZeroGPU adapter first, then uses the CPU demo only when ZeroGPU cannot be used. The current Hunyuan adapter remains intentionally disabled until the license and dependency gates are complete.

Future GPU adapters should:

- keep GPU-only work in explicit adapter functions;
- use dynamic `@spaces.GPU(duration=...)` when runtime varies;
- avoid `torch.compile` on ZeroGPU;
- provide shape-only fallback when texture generation is unavailable;
- fail with actionable messages when model weights, licenses, memory, or CUDA-only wheels are missing.

## Deployment With `hf`

See [docs/knowledgebase/deployment-hf-cli.md](docs/knowledgebase/deployment-hf-cli.md).

## Automation

The repo now includes three deployment-oriented GitHub Actions workflows in addition to CI.

- `Forge Mirrors` plans GitLab and Codeberg repository sync on pull requests and creates or reuses those repos on `main`, `master`, or `workflow_dispatch` when credentials are present.
- `Hugging Face Space` shows the exact `hf` commands on pull requests and performs create-or-upload on default-branch pushes or manual dispatch when `HF_TOKEN` is available.
- `Runtime Artifacts` resolves one image tag, builds one OCI image, renders Helm/Kubernetes/Nomad/Podman assets from that same image reference, and publishes to enabled registries.

The default behavior matches the rest of the repo: pull requests are dry-run only, default-branch pushes use intuitive defaults such as `latest`, and missing credentials cause a clear skip instead of hidden partial failure unless a target is explicitly made required.

See [docs/knowledgebase/release-automation.md](docs/knowledgebase/release-automation.md).

## VS Code

Use the tasks in [.vscode/tasks.json](.vscode/tasks.json) for setup, `.env` creation, testing, compile checks, style checks, the Gradio app, `hf` and `gh` helper output, release dry-run previews, forge mirror previews, and deploy-asset rendering. Debug configurations live in [.vscode/launch.json](.vscode/launch.json).

## Verification

See [docs/knowledgebase/verification.md](docs/knowledgebase/verification.md).

## License And Source Use

This scaffold does not vendor code, model weights, generated outputs, or assets from Hunyuan3D, TRELLIS, or Pixal3D. Before porting any implementation detail beyond public interface ideas, complete the license audit in [docs/knowledgebase/license-audit.md](docs/knowledgebase/license-audit.md).
