# ZeroGPU Runtime Strategy

This note describes how the repo currently treats ZeroGPU: as a preferred hosted runtime when it is genuinely available, not as a vague synonym for "somehow use GPU."

## Source Basis

This note is based on:

- `src/imageezgen3d/runtime.py`;
- `src/imageezgen3d/orchestrator.py`;
- `src/imageezgen3d/config.py`;
- the current `pyproject.toml` runtime defaults;
- current official platform guidance already incorporated elsewhere in the knowledgebase.

## Core Policy

The default backend is `auto`.

That means:

- prefer the configured hosted path when the environment truly supports it;
- otherwise use the CPU-safe fallback only when policy allows it;
- if fallback is disallowed, fail honestly with an actionable reason.

This is not a "GPU if possible, shrug if not" model. It is an explicit runtime-selection policy.

## Resolution Order

1. If an explicit adapter is selected, use it.
2. If `auto` is selected and ZeroGPU is usable, choose the configured ZeroGPU adapter.
3. If the ZeroGPU path is unavailable, disabled, or not fully configured, use CPU only when `fallback_to_cpu = true`.
4. If CPU fallback is disabled, fail with an actionable error.

## What Counts As ZeroGPU Usable

The runtime checks currently require all of the following:

- ZeroGPU is enabled in config;
- CPU is not forced;
- Hugging Face Space runtime markers are present when `require_spaces_runtime = true`;
- the optional `spaces` package is importable.

This is intentionally stricter than "the code imported and maybe a GPU exists somewhere."

## What Does Not Count

The repo should not claim ZeroGPU is available merely because:

- the code is running on a powerful local machine;
- CUDA happens to exist locally;
- a future adapter name is configured in TOML;
- a developer expects the hosted path to be present later.

Local execution is not a real ZeroGPU environment when the required Spaces markers and package support are absent.

## Current Reason Model

The current runtime logic can explain outcomes such as:

- CPU mode selected explicitly;
- CPU forced by config or environment;
- ZeroGPU runtime available and preferred;
- ZeroGPU disabled by configuration;
- local execution falling back because a real Spaces runtime is required;
- `spaces` support not being importable;
- general ZeroGPU unavailability.

These reasons should not stay internal. They belong in the manifest and near the UI progress surface.

## Current Adapter State

- `hunyuan-zerogpu`: preferred future hosted adapter, intentionally unconfigured — see [hunyuan-admission-gates.md](hunyuan-admission-gates.md);
- **G4 scaffold (Plan 051):** `src/imageezgen3d/adapters/hunyuan.py` routes future inference through `_run_hunyuan_inference_on_gpu`, decorated with `spaces.GPU` when the package is importable (identity decorator locally). Adapter remains `configured=False`.
- `cpu-demo`: fallback adapter for local development, tests, and no-GPU environments.

The important point is that the hosted path is a future real target, not current theater.

## Hosted Design Rules

- ZeroGPU is Gradio-only;
- GPU work should live inside `@spaces.GPU`-decorated functions;
- CPU preprocessing, manifests, validation, and export checks should remain outside GPU-only sections;
- model placement and warm-up behavior should be designed intentionally rather than moved naively inside every request call;
- the default shared-runtime duration is short, so long monolithic GPU stages are a poor fit.

## Future Heavy-Adapter Rules

- decorate GPU-dependent functions with `@spaces.GPU`;
- keep CPU preprocessing, manifests, validation, and export checks outside GPU sections;
- do not use `torch.compile` on ZeroGPU;
- record GPU duration, model revision, seed, settings, and fallback reason in the manifest;
- never silently fall back to CPU without telling the user why;
- separate shape generation from texture or refinement when the heavy stage materially changes runtime cost.

## Queue And Duration Guidance

- prefer shorter declared GPU durations when possible because queue priority is generally better for shorter tasks;
- use dynamic duration calculation when runtime varies materially with user settings;
- treat larger allocations such as `xlarge`-style choices as exceptional because they consume more quota and usually increase queue pressure;
- expect free or shared Spaces to sleep when idle and design the app so cold starts remain understandable rather than mysterious.

## Operator-Facing Expectations

If the user triggers generation, the app should make it clear:

- whether the hosted path was actually used;
- whether CPU fallback was triggered;
- why that decision happened;
- whether the current output should be interpreted as a draft or a fuller path result.

Without that visibility, runtime selection becomes hidden behavior again.

## Security And Secret Handling

- keep secrets in Space settings, not in source;
- do not make a ZeroGPU path depend on hardcoded tokens or manual local hacks;
- if gated weights become necessary, reflect that requirement in deployment and license docs as well.

## Practical Rule

ZeroGPU should be treated as a scoped hosted execution lane with clear eligibility rules, not as an excuse to blur local, hosted, CPU, and GPU behaviors together.
