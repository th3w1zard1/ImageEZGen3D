---
title: "feat: Golden sample CI attestation"
type: feat
status: completed
date: 2026-05-24
origin: docs/ideation/2026-05-23-next-focus-ideation.md
---

# feat: Golden sample CI attestation

## Summary

Add a reproducible local golden-sample attestation (Block PNG → cpu-demo generate → manifest/GLB/OBJ checks) and wire it into CI so every PR/main run proves the core generation contract without claiming hosted ZeroGPU.

## Requirements

- R1. `imageezgen3d.golden_sample` module runs Block sample through orchestrator on cpu-demo
- R2. Attestation validates `stage=done`, run id, manifest + GLB + OBJ exist with minimum byte sizes
- R3. CLI `scripts/golden_sample_attestation.py` exits 0 on success, non-zero on failure; supports `--json`
- R4. CI job `golden-sample` runs attestation on Python 3.12 for push/PR to `main`
- R5. Unit tests cover success path and missing-artifact failure
- R6. Parity register row P12 documents golden CI vs hosted E2E distinction
- R7. Full `unittest discover` passes

## Scope Boundaries

- Hosted Space browser/API attestation — remains manual per AGENTS.md; CI is local CPU only
- Hunyuan / ZeroGPU paths — out of scope

## Files

- Add: `src/imageezgen3d/golden_sample.py`
- Add: `scripts/golden_sample_attestation.py`
- Add: `tests/test_golden_sample.py`
- Modify: `.github/workflows/ci.yml`
- Modify: `docs/knowledgebase/40-operational-risk/source-runtime-parity-register.md`
