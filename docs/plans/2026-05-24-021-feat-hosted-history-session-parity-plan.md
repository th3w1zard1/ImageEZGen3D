---
title: "feat: Hosted History session parity"
type: feat
status: completed
date: 2026-05-24
origin: docs/ideation/2026-05-23-next-focus-ideation.md
---

# feat: Hosted History session parity

## Summary

Runs created on the HF Space were invisible in the browser History tab because output storage defaulted to ephemeral `outputs/` and History only loaded at demo build time. Persist runs under Space `/data` when available and refresh History on page load.

## Requirements

- R1. Merge PR #11 (golden-sample CI) to `main` before feature work
- R2. `resolve_output_dir()` uses `/data/outputs` on HF Space when `/data` is writable unless `IMAGEEZ_OUTPUT_DIR` is set
- R3. `demo.load()` refreshes History radio, notice, and overview panels from disk on page load
- R4. Unit tests for output-dir resolution and existing suite passes (85+ tests)
- R5. Document Space persistent output path in `.env.example` and configuration KB
- R6. Deploy Space and browser-verify History lists a run after in-tab Generate Mesh

## Scope Boundaries

- Multi-replica load balancing across workers without shared storage — document `[OPEN]` if still observed
- Hunyuan / ZeroGPU — out of scope

## Files

- Modify: `src/imageezgen3d/config.py`
- Modify: `app.py`
- Modify: `.env.example`
- Modify: `docs/knowledgebase/configuration.md`
- Add: tests in `tests/test_config.py`
