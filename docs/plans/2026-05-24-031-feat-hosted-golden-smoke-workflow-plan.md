---
title: "feat: Hosted golden smoke CI workflow"
type: feat
status: completed
date: 2026-05-24
origin: docs/ideation/2026-05-24-post-trust-slice-refresh.md
---

# feat: Hosted golden smoke CI workflow

## Summary

Add a scheduled GitHub Actions workflow that runs Block `/generate` against the live HF Space and asserts export-sidecar-era golden contracts (run id, export budget, CPU fallback visibility). Complements local `golden-sample` CI without replacing hosted manual validation.

## Requirements

- R1. `hosted_golden_smoke.run_hosted_golden_smoke()` — Gradio API Block generate + status validation
- R2. `scripts/hosted_golden_smoke.py` CLI with `--space-url`, `--json`, `--record`
- R3. `.github/workflows/hosted-golden-smoke.yml` — `workflow_dispatch` + daily `schedule`; install `.[app,dev]`
- R4. Unit tests for status validation (no live Space in unittest)
- R5. 98+ tests; style guard + ruff on changed paths
- R6. Document in parity register (P13) and hosted-validation KB after first green run

## Scope Boundaries

- Not a replacement for local golden-sample job
- No Hunyuan/ZeroGPU enablement
- No merge-blocking on PRs (scheduled/dispatch only)

## Files

- Add: `src/imageezgen3d/hosted_golden_smoke.py`
- Add: `scripts/hosted_golden_smoke.py`
- Add: `tests/test_hosted_golden_smoke.py`
- Add: `.github/workflows/hosted-golden-smoke.yml`
- Modify: `docs/knowledgebase/40-operational-risk/source-runtime-parity-register.md`
