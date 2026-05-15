# Configuration Guide

`pyproject.toml` is the canonical configuration file. The app reads the `[tool.imageezgen3d.*]` tables by default.

## Local Overrides

`.env` is generated from `.env.example` and is ignored by git. Use it for machine-specific values such as launch port, output directory, or Hugging Face token location.

Important overrides:

- `IMAGEEZ_CONFIG`: config source, default `pyproject.toml`.
- `IMAGEEZ_ADAPTER`: `auto`, `cpu-demo`, or a named adapter.
- `IMAGEEZ_RUNTIME`: `auto`, `zerogpu`, or `cpu`.
- `IMAGEEZ_PREFER_ZEROGPU`: defaults to `true`.
- `IMAGEEZ_FALLBACK_TO_CPU`: defaults to `true`.
- `IMAGEEZ_FORCE_CPU`: explicit escape hatch for local/offline work.
- `IMAGEEZ_ZEROGPU_ENABLED`: defaults to `true`.
- `IMAGEEZ_OUTPUT_DIR`: where run manifests and artifacts are written.
- `IMAGEEZ_PREPROCESS_TARGET_SIZE`: normalized image size.

## Why pyproject Owns Defaults

This keeps dependency metadata, package discovery, Pyright analysis settings, runtime defaults, export formats, and app behavior in one auditable place. Thin files still exist where tools expect them:

- `requirements.txt` delegates to `-e .[app]` for Hugging Face Spaces.
- `.vscode/settings.json` points VS Code at the venv and `.env`.
- `.vscode/tasks.json` and `.vscode/launch.json` describe editor workflows.

## Self-Critique

Environment variables are powerful but can hide behavior. Every generated manifest records the selected adapter, requested adapter, runtime status, and fallback reason so decisions remain visible.
