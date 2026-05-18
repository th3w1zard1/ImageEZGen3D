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

## Upload App

```bash
hf upload YOUR_USERNAME/ImageEZGen3D . . --repo-type=space --exclude='.git/**' --exclude='.venv/**' --exclude='**/__pycache__/**' --exclude='**/*.pyc' --exclude='.pytest_cache/**' --exclude='.ruff_cache/**' --exclude='build/**' --exclude='dist/**' --exclude='tmp/**' --exclude='outputs/**' --exclude='.env*' --exclude='src/imageezgen3d.egg-info/**' --commit-message='Deploy ImageEZGen3D'
```

Important details:

- keep local virtualenvs, caches, build outputs, and egg-info metadata out of Space uploads;
- keep `outputs/` out of deployments;
- keep `.env` and any secret-bearing files out of deployments;
- do not vendor model caches, generated outputs, or local artifacts into the Space repo;
- use a commit message that makes the deployment intent clear.

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
