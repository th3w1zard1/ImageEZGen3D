# ZeroGPU Runtime Strategy

The default backend is `auto`.

Resolution order:

1. If an explicit adapter is selected, use it.
2. If `auto` is selected and ZeroGPU is usable, choose the configured ZeroGPU adapter.
3. If the ZeroGPU adapter is unavailable, disabled, or not fully configured, use CPU only when `fallback_to_cpu = true`.
4. If CPU fallback is disabled, fail with an actionable error.

## What Counts As ZeroGPU Usable

The runtime checks:

- ZeroGPU is enabled in config.
- CPU is not forced.
- Hugging Face Space runtime markers are present when `require_spaces_runtime = true`.
- The optional `spaces` package is importable.

## Current Adapter State

- `hunyuan-zerogpu`: preferred future adapter, intentionally unconfigured pending license/dependency/ZeroGPU work.
- `cpu-demo`: fallback adapter for local development, tests, and no-GPU environments.

## Future Heavy Adapter Rules

- Decorate GPU-dependent functions with `@spaces.GPU`.
- Keep CPU preprocessing, manifests, validation, and export checks outside GPU sections.
- Do not use `torch.compile` on ZeroGPU.
- Record GPU duration, model revision, seed, settings, and fallback reason in the manifest.
- Never silently fall back to CPU without telling the user why.
