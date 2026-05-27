---
title: "feat: Ship PR #40 + Hunyuan G6 manifest parity sample"
type: feat
status: completed
date: 2026-05-27
origin: docs/ideation/2026-05-24-post-trust-slice-refresh.md
---

# feat: Ship PR #40 + Hunyuan G6 manifest parity sample

## Summary

Squash-merge PR #40 (History tab idle backend rail), deploy Space for UX parity, then close **G6 prep** with a repo-grounded Hunyuan sample manifest, validator, CI test, and admission audit wiring (adapter stays disabled).

## Requirements

- R1. Squash-merge PR #40
- R2. Deploy Space via `PYTHONPATH=src python scripts/hf_space_sync.py --execute`
- R3. `tests/fixtures/hunyuan-zerogpu-manifest.sample.json` + `validate_hunyuan_manifest_parity()`
- R4. `docs/knowledgebase/hunyuan-manifest-parity.md` with `G6_STATUS: PASS` (sample only; not enablement)
- R5. Admission audit G6 checks sample file validates
- R6. Hosted golden smoke + browser after deploy
- R7. KB Plan 059 section

## Scope boundaries

- Do **not** set `HunyuanPlaceholderAdapter.configured=True`
- G7 real Hunyuan hosted E2E — deferred

## Files

- Add: `src/imageezgen3d/hunyuan_manifest_parity.py`
- Add: `tests/fixtures/hunyuan-zerogpu-manifest.sample.json`
- Add: `tests/test_hunyuan_manifest_parity.py`
- Add: `docs/knowledgebase/hunyuan-manifest-parity.md`
- Modify: `src/imageezgen3d/hunyuan_admission.py`
- Modify: `docs/knowledgebase/hunyuan-admission-gates.md`

## Test scenarios

- Sample manifest passes parity validator
- Invalid manifest (missing export_sidecar) fails
- Admission audit G6 reports pass when sample + doc present
