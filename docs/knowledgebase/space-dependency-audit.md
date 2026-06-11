# Space Dependency Audit

Audit record for optional delivery dependencies shipped in Hugging Face Space `requirements.txt`.

## USDZ / usd-core (2026-06-03)

Plan 180 deferred adding `usd-core` to Space until payload impact was measured. Gradio USDZ slots (Plan 181) and hosted delivery-format smoke (Plan 182) are merged; hosted Space still skipped USDZ because the dependency was absent at build time.

### Measurement

| Package | Linux install footprint | Notes |
|---------|-------------------------|-------|
| `usd-core` 26.5 | ~149 MB (`pxr` module tree) | Wheel-only; no native compile on Space |
| Existing mesh stack (`trimesh`, `fast-simplification`) | Already in `requirements.txt` | Baseline mesh export deps |

Measured on Fedora 44 / Python 3.14 dev environment via `du` on installed `pxr` package path after `pip install usd-core`.

### Decision

**Opt in.** ~150 MB is acceptable relative to the existing Space mesh stack and enables USDZ delivery exports on hosted runs without a separate `[mesh-delivery]` editable install (unsupported on HF requirements-first builds).

### Contract

- `requirements.txt` adds `usd-core>=24.0`, matching `pyproject.toml` `[project.optional-dependencies].mesh-delivery`.
- Local/CI dev installs continue using `.[mesh-delivery]`; Space uses flat requirements only.
- Golden sample CI attestation requires **FBX** always and **USDZ** when `usd-core` is installed (Phase N); hosted smoke required keys unchanged until live Space attestation.
