# Configuration Guide

This note explains how configuration resolves in the current scaffold and how to change behavior without turning runtime decisions into hidden magic.

## Source Basis

This note is based on:

- `pyproject.toml`;
- `src/imageezgen3d/config.py`;
- `src/imageezgen3d/runtime.py`;
- `src/imageezgen3d/orchestrator.py`;
- `.env.example` and the current VS Code task and debug setup.

## Canonical Source Of Truth

`pyproject.toml` is the canonical committed configuration file.

The app reads the `[tool.imageezgen3d.*]` tables by default and uses them to define:

- app identity and default adapter routing;
- launch host, port, queue size, and concurrency;
- storage retention behavior;
- generation defaults such as quality, seed, texture size, and decimation target;
- preprocessing thresholds;
- runtime and ZeroGPU strategy;
- export formats;
- release automation defaults for forge mirrors, registry publishing, and deploy artifacts.

This keeps package metadata, runtime behavior, and analysis settings in one auditable place instead of spreading them across multiple partially authoritative files.

## Configuration Precedence

When the app uses the normal `load_config()` path, effective settings resolve in this order, with later layers winning:

1. built-in dataclass defaults in `config.py`;
2. `[tool.imageezgen3d.*]` values from `pyproject.toml` or the file named by `IMAGEEZ_CONFIG`;
3. `.env` values loaded from the repo root;
4. process environment variables already present at launch.

Nuance:

- `IMAGEEZ_CONFIG` can point to an alternate TOML file;
- if code calls `load_config(path)` directly, `.env` is not auto-loaded by `config.py`, but environment variables already present in the process still override supported values;
- not every TOML value currently has an environment-variable override, which is intentional.

## Current Configuration Surfaces

### App

- `title`: UI title;
- `output_dir`: root for run folders and manifests;
- `adapter`: default adapter request, usually `auto`;
- `cpu_adapter`: current safe local fallback, `cpu-demo`;
- `zerogpu_adapter`: preferred hosted adapter when the runtime is actually available.

### Launch

- `host` and `port` control the Gradio bind address;
- `[REPO]` effective port resolves in order: `PORT` → `GRADIO_SERVER_PORT` → `IMAGEEZ_PORT` → `[tool.imageezgen3d.app].port` (default **7865** for local dev);
- `[SYNTH]` Hugging Face Gradio Spaces typically set `GRADIO_SERVER_PORT`; local `.vscode` tasks use pyproject default unless overridden;
- `share` controls public Gradio sharing behavior;
- `queue_max_size` and `default_concurrency_limit` shape the hosted request lane.

### Storage

- `retention_runs` limits how many run folders are kept;
- `keep_failed_runs` preserves failure evidence instead of hiding it.

### Generation

- `seed` and `quality` define the default request shape;
- `texture_size` and `decimation_target` describe the intended asset budget;
- `preserve_intermediates` keeps inspection artifacts available.

### Preprocessing

- `target_size` defines the normalized working size;
- `minimum_short_side` and `maximum_long_side` gate extreme inputs;
- blur and contrast thresholds feed input-quality reporting.

### Runtime

- `mode` may be `auto`, `cpu`, or future hosted modes;
- `prefer_zerogpu` and `fallback_to_cpu` define the automatic selection policy;
- `force_cpu` is the explicit local escape hatch.

### ZeroGPU

- `enabled` controls whether the app will even consider ZeroGPU;
- duration settings define expected GPU windows for default and texture-heavy work;
- `size` captures the intended GPU size class;
- `require_spaces_runtime` prevents the app from pretending local execution is a real ZeroGPU environment.

### Exports

- `default_format` is currently `glb`;
- `formats` lists the allowed export families.

### Release Automation

- `release.repository` can override the owner and repo name used for mirror and registry defaults;
- `release.branches` defines which branches are treated as default publication branches;
- `release.tags` defines the `latest`, `sha-*`, and `pr-*` tag behavior;
- `release.forge.gitlab`, `release.forge.codeberg`, and `release.forge.huggingface` define target repo defaults and enablement;
- `release.registry.ghcr`, `release.registry.dockerhub`, and `release.registry.gitlab` define target image names and opt-in registries;
- `release.artifacts` controls Helm, raw Kubernetes, Nomad, Podman, and GitHub release asset generation.

## Supported Environment Overrides

The code currently supports these environment-level overrides.

### Config Source And App Identity

- `IMAGEEZ_CONFIG`
- `IMAGEEZ_TITLE`
- `IMAGEEZ_OUTPUT_DIR`
- `IMAGEEZ_ADAPTER`
- `IMAGEEZ_CPU_ADAPTER`
- `IMAGEEZ_ZEROGPU_ADAPTER`

### Launch

- `IMAGEEZ_HOST`
- `IMAGEEZ_PORT`
- `PORT` and `GRADIO_SERVER_PORT` (hosted Spaces inject the latter; see port precedence below)
- `IMAGEEZ_SHARE`
- `IMAGEEZ_QUEUE_MAX_SIZE`
- `IMAGEEZ_DEFAULT_CONCURRENCY_LIMIT`

### Preprocessing

- `IMAGEEZ_PREPROCESS_TARGET_SIZE`
- `IMAGEEZ_MINIMUM_SHORT_SIDE`
- `IMAGEEZ_MAXIMUM_LONG_SIDE`
- `IMAGEEZ_BLUR_EDGE_VARIANCE_THRESHOLD`
- `IMAGEEZ_LOW_CONTRAST_THRESHOLD`

### Runtime And ZeroGPU

- `IMAGEEZ_RUNTIME`
- `IMAGEEZ_PREFER_ZEROGPU`
- `IMAGEEZ_FALLBACK_TO_CPU`
- `IMAGEEZ_FORCE_CPU`
- `IMAGEEZ_ZEROGPU_ENABLED`
- `IMAGEEZ_ZEROGPU_SIZE`
- `IMAGEEZ_ZEROGPU_REQUIRE_SPACES_RUNTIME`

### Release Automation

- `IMAGEEZ_RELEASE_OWNER`
- `IMAGEEZ_RELEASE_REPO`
- `IMAGEEZ_RELEASE_PRIMARY_BRANCH`
- `IMAGEEZ_RELEASE_FALLBACK_BRANCHES`
- `IMAGEEZ_RELEASE_PUBLISH_LATEST_BRANCHES`
- `IMAGEEZ_RELEASE_DEFAULT_IMAGE_TAG`
- `IMAGEEZ_RELEASE_IMAGE_TAG`
- `IMAGEEZ_RELEASE_CREATE_MISSING_TARGETS`
- `IMAGEEZ_RELEASE_GITLAB_ENABLED`
- `IMAGEEZ_RELEASE_CODEBERG_ENABLED`
- `IMAGEEZ_RELEASE_HF_ENABLED`
- `IMAGEEZ_RELEASE_GHCR_ENABLED`
- `IMAGEEZ_RELEASE_DOCKERHUB_ENABLED`
- `IMAGEEZ_RELEASE_GITLAB_REGISTRY_ENABLED`

Notable limitation:

- storage retention, generation defaults, and export formats are currently committed-config surfaces, not ad hoc environment toggles.
- advanced release overrides such as per-target owner, repo, visibility, namespace, or registry host are still committed-config first and should only move into environment overrides when you have a real multi-environment need.

## Manifest Visibility

The app does not just load config and hope the operator infers what happened.

Before generation, the orchestrator records at least these decision surfaces into the manifest:

- requested adapter;
- selected adapter;
- quality;
- seed;
- runtime status fields;
- fallback reason when automatic routing did not use the preferred hosted path.

That is the core anti-magic rule for this repo: configuration may be flexible, but the selected behavior should still be inspectable after the run.

## Recommended Usage Patterns

### Use `pyproject.toml` For Shared Defaults

Put stable team defaults here:

- default adapter strategy;
- output format policy;
- preprocessing thresholds;
- retention behavior;
- queue and launch defaults.

### Use `.env` For Machine-Specific Overrides

Good `.env` use cases:

- local port changes;
- forcing CPU on a development machine;
- alternate output directories;
- token locations or local secrets handled outside source.

### Use One-Off Environment Variables For Experiments

These are useful for:

- quickly forcing CPU during local debugging;
- temporarily disabling ZeroGPU consideration;
- checking launch behavior under a different port or queue size.

If an override becomes normal team behavior, move it back into `pyproject.toml`.

## Common Operational Patterns

### Local CPU-Only Development

Prefer one of these:

- set `IMAGEEZ_FORCE_CPU=true`;
- set `IMAGEEZ_RUNTIME=cpu`.

The first is the stronger escape hatch because it disables ZeroGPU consideration completely.

### Alternate Config File

Use `IMAGEEZ_CONFIG=/path/to/other.toml` when you want a different committed config profile without editing the main repo defaults.

### Output Isolation

Set `IMAGEEZ_OUTPUT_DIR` when you want test runs or experiments to write somewhere other than the default `outputs/` tree.

On Hugging Face Spaces, when `SPACE_ID` (or related Space env markers) is set and `/data` is writable, the app defaults run storage to `/data/outputs` so History and exports survive restarts. Set `IMAGEEZ_OUTPUT_DIR` explicitly to override that behavior.

### Runtime Tuning For Hosted Environments

Adjust launch queue and concurrency intentionally rather than letting multiple implicit knobs drift:

- `IMAGEEZ_QUEUE_MAX_SIZE`
- `IMAGEEZ_DEFAULT_CONCURRENCY_LIMIT`
- `IMAGEEZ_ZEROGPU_SIZE`

## Gotchas

- setting `IMAGEEZ_ZEROGPU_ENABLED=true` does not make local execution a real ZeroGPU environment;
- `prefer_zerogpu=true` still falls back when the Spaces runtime is absent or the configured hosted adapter is not enabled;
- too many `.env` overrides can make behavior hard to reason about even if the app records outcomes correctly;
- if `IMAGEEZ_CONFIG` points elsewhere, repo readers may incorrectly assume `pyproject.toml` is still the live source unless the run manifest is checked;
- configuration changes that affect UX or runtime policy should usually be reflected in the relevant knowledgebase docs, not only in TOML.
