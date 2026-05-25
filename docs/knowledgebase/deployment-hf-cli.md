# Hugging Face CLI Deployment Runbook

This note focuses on the current deployment path the scaffold is actually shaped around: a Gradio Space deployed with the `hf` CLI, using ZeroGPU only when the hosted runtime and adapter gating make that legitimate.

## Source Basis

This note is based on:

- `README.md`;
- `requirements.txt` and `pyproject.toml`;
- `src/imageezgen3d/hf_cli.py`;
- `scripts/hf_space_check.py`;
- the current ZeroGPU strategy reflected elsewhere in the knowledgebase.

## Deployment Intent

The repo is not trying to make deployment look magical.

The intended shape is:

- local development remains CPU-safe and weight-free by default;
- the hosted app is a Gradio Space;
- ZeroGPU is preferred only when it is truly available;
- heavy adapters remain blocked until licensing, dependency, and runtime constraints are cleared;
- tokens and secrets stay out of source.

## Preflight

Use `hf` where practical.

Basic checks:

```bash
hf auth whoami
hf env
hf cache ls
```

The helper script `scripts/hf_space_check.py` exists to print the currently recommended `hf` commands without modifying the repo.

## Local Verification Before Upload

Do not treat Spaces builds as the first validator.

Run the local checks first:

```bash
PYTHONPATH=src .venv/bin/python -m unittest discover -s tests
PYTHONPATH=src .venv/bin/python -m compileall -q app.py src tests scripts
PYTHONPATH=src .venv/bin/python scripts/check_python_style.py
```

If UI or runtime behavior changed, also run the app locally before pushing.

## Create Or Reuse A Gradio Space

```bash
hf repo create YOUR_USERNAME/ImageEZGen3D --repo-type space --space-sdk gradio --exist-ok
```

The repo front matter and the Space creation command should agree that the SDK is `gradio`.

## Dry-Run Model Downloads

These are useful only as audit and planning tools while heavy adapters remain gated.

```bash
hf download tencent/Hunyuan3D-2.1 --dry-run
hf cache verify tencent/Hunyuan3D-2.1
```

Use dry runs to inspect size, cache behavior, and access expectations before pretending a model is ready for hosted use.

**Recorded dry-run (G2, 2026-05-24):** `tencent/Hunyuan3D-2.1` — 30 files, **14.9 GB** total; Hub `gated=false`; see [hunyuan-weight-access.md](hunyuan-weight-access.md).

### Hunyuan Space secrets (when adapter is enabled)

Until G3–G8 close, do **not** enable Hunyuan inference. When enabled:

| Secret | Purpose |
| --- | --- |
| `HF_TOKEN` | Hub download / cache for `tencent/Hunyuan3D-2.1` at runtime |
| (optional) `HF_HOME` | Pin hub cache directory on Space persistent storage if disk is tight |

Set via Hugging Face Space **Settings → Repository secrets**. Never commit token values to git or `requirements.txt`.

## Upload App

**Prefer staged minimal payload** — full-repo uploads can timeout or include workspace junk. `[REPO]` `stage_space_payload()` in `src/imageezgen3d/hf_cli.py` copies only Space-required paths (~30 files).

```bash
PYTHONPATH=src python -c "
from pathlib import Path
from imageezgen3d.hf_cli import stage_space_payload
stage_space_payload(Path('/tmp/imageezgen3d-space-payload'))
"
hf upload YOUR_USERNAME/ImageEZGen3D /tmp/imageezgen3d-space-payload . \
  --repo-type=space \
  --commit-message='Deploy ImageEZGen3D'
```

Full-repo upload (discouraged for large workspaces):

```bash
hf upload YOUR_USERNAME/ImageEZGen3D . . --repo-type=space --exclude='.git/**' --exclude='.venv/**' --exclude='**/__pycache__/**' --exclude='**/*.pyc' --exclude='.pytest_cache/**' --exclude='.ruff_cache/**' --exclude='build/**' --exclude='dist/**' --exclude='tmp/**' --exclude='outputs/**' --exclude='.env*' --exclude='src/imageezgen3d.egg-info/**' --exclude='deploy/**' --exclude='docs/plans/**' --commit-message='Deploy ImageEZGen3D'
```

Important details:

- keep local virtualenvs, caches, build outputs, and egg-info metadata out of Space uploads;
- keep `outputs/` out of deployments;
- keep `.env` and any secret-bearing files out of deployments;
- do not vendor model caches, generated outputs, or local artifacts into the Space repo;
- use a commit message that makes the deployment intent clear;
- `[REPO]` CI uploads via `.github/workflows/hf-space.yml` on default-branch pushes and `v*` release tags when `HF_TOKEN` is configured; tag builds use `Deploy ImageEZGen3D <tag>` commit messages;
- `[OFFICIAL]` Spaces install `requirements.txt` before copying full source — keep it self-contained (no editable `-e .[app]`).

## Port And Launch

- `[REPO]` Local default port is **7865** in `pyproject.toml`.
- `[OFFICIAL]` Hugging Face Gradio Spaces inject `GRADIO_SERVER_PORT` (commonly `7860`). The config loader honors `PORT` → `GRADIO_SERVER_PORT` → `IMAGEEZ_PORT` → pyproject default.
- `[REPO]` When Space env markers are present and no port env vars are set, `load_config()` defaults launch port to **7860** (see `_resolve_launch_port()` in `config.py`).
- `[REPO]` Export a module-level `demo = build_demo()` in `app.py` so the Spaces Gradio launcher can bind the queued app; omit explicit `server_port` in `launch()` on Spaces.
- If a Space stays in `APP_STARTING`, verify the app binds to the platform port (7860), not the local pyproject default alone.

## Package Contract

`requirements.txt` intentionally lists the runtime dependencies directly because Spaces installs it before the full repo source is copied into the build context.

That means deployment hygiene depends on keeping these aligned:

- `pyproject.toml` optional dependency set for `app`;
- `requirements.txt` runtime dependency list;
- `README.md` setup instructions;
- runtime assumptions documented in the knowledgebase.

If these drift, the repo may look correct in source while the hosted Space fails differently.

## Secrets And Auth

- use `hf auth login` or equivalent local auth flow instead of hardcoding tokens;
- do not paste tokens into tracked files;
- use Space secrets or environment settings for hosted credentials when they become necessary;
- document any future hosted secret requirement in both deployment docs and verification docs.

## ZeroGPU Notes

- ZeroGPU requires a Gradio Space;
- GPU work must be isolated behind `@spaces.GPU` decorated functions;
- CPU preprocessing, storage, validation, and export work should stay outside GPU-only sections;
- default GPU duration is 60 seconds and longer windows should be justified, not habitual;
- `torch.compile` is not supported on ZeroGPU;
- larger GPU size increases quota pressure;
- the current app strategy is still `auto`: prefer hosted GPU when truly available, otherwise fall back with an explicit reason.

## What Should Ship In The Current Phase

Safe current deployment contents are the scaffold itself:

- `app.py` and `src/`;
- `pyproject.toml` and `requirements.txt`;
- docs and scripts that support the scaffold;
- the CPU-safe default behavior and knowledgebase guidance.

Unsafe current-phase deployment assumptions would be:

- pretending the Hunyuan placeholder is a finished hosted adapter;
- bundling gated model assets into source;
- making the hosted app require CUDA-only local setup to develop;
- hiding fallback-to-CPU reasons from users.

## First-Run Verification After Upload

Once the Space is live, verify more than just page availability.

- confirm the Space SDK is Gradio;
- confirm the app starts without secret leakage or missing-package surprises;
- confirm a sample image can be uploaded and processed;
- confirm runtime status and fallback reasons are visible;
- confirm manifests and exports are written coherently;
- confirm hosted behavior still matches the current verification and ZeroGPU docs.

## Common Failure Classes

### Build Succeeds But Runtime Intent Drifted

Typical cause:

- `pyproject.toml`, `requirements.txt`, README setup guidance, and deployed runtime assumptions stopped matching.

### ZeroGPU Never Activates

Typical cause:

- not actually running inside a qualifying Spaces runtime;
- `spaces` support missing;
- hosted adapter configured but not enabled.

### Upload Included Local Junk

Typical cause:

- forgetting to exclude `outputs/`, `.env`, caches, or other machine-local artifacts.

### Heavy Adapter Expectations Jumped Ahead Of Audit

Typical cause:

- trying to deploy future-model assumptions before the license and dependency gates are complete.

## Operational Rule

Use Spaces deployment to validate a hosted slice of the scaffold, not to bypass the scaffold's own legal, runtime, or verification gates.
