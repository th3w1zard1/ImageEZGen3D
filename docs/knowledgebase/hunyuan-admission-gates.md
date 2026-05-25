# Hunyuan Admission Gates

This document is the **enablement checklist** for the `hunyuan-zerogpu` adapter. It does not authorize turning the adapter on by itself.

Legal and redistribution rules live in [license-audit.md](license-audit.md). Runtime policy lives in [zerogpu-runtime.md](zerogpu-runtime.md). Hosted honesty requirements live in [40-operational-risk/hosted-validation-2026-05-23.md](40-operational-risk/hosted-validation-2026-05-23.md).

## Current decision

**Status: NOT ENABLED**

`HunyuanPlaceholderAdapter` remains `configured=False` in code until every gate below is explicitly closed with written evidence.

## Automated audit (repo-grounded)

Run from the repository root (does **not** enable the adapter):

```bash
PYTHONPATH=src python scripts/hunyuan_admission_audit.py
```

Machine-readable output: `PYTHONPATH=src python scripts/hunyuan_admission_audit.py --json`

The audit exits **0** while `configured=False`. It exits **1** if the adapter were enabled while gates remain open (safety guard for enablement PRs).

**Last audit:** 2026-05-24 — Plan 052; adapter `configured=False`; **G1–G4 PASS**; G5–G7 **OPEN**; G6/G8/G9 **PASS** (scaffold + disabled).

## Completed prerequisites

| Prerequisite | Evidence |
| --- | --- |
| Hosted CPU fallback path validated | Plan 015 — run `20260524-121906-f2550d30`; fallback + comprehension exit on live Space |
| Fallback honesty labeling | Plan 012/013 — preview disclaimer in UI and manifest |
| Space deploy contract | `scripts/hf_space_sync.py`, port binding fix on `main` |

## Admission gates

Record evidence in this table (or linked PR) before setting `configured=True` on the Hunyuan adapter.

| Gate | ID | Pass criteria | Evidence required | Status |
| --- | --- | --- | --- | --- |
| Legal review | G1 | License, commercial use, attribution, and redistribution rights documented for code, weights, and wheels | [license-audit.md](license-audit.md) § Hunyuan3D-2.1 audit record — pins `82920d64` (GitHub) / `0b946776` (HF); `G1_STATUS: PASS` | **PASS** |
| Weight access | G2 | Gated downloads, tokens, and acceptance flows documented; no secrets in repo | [hunyuan-weight-access.md](hunyuan-weight-access.md) — dry-run 14.9 GB / 30 files; `G2_STATUS: PASS` | **PASS** |
| Dependency audit | G3 | Python/CUDA deps pinned; wheels redistribution rights known; install reproducible on Space | [hunyuan-dependencies.md](hunyuan-dependencies.md) + `requirements/hunyuan-pins.txt`; `.[hunyuan-audit]` CI smoke; `G3_STATUS: PASS` | **PASS** |
| ZeroGPU wiring | G4 | GPU work only inside `@spaces.GPU`; CPU path unchanged | `src/imageezgen3d/adapters/hunyuan.py` — `_run_hunyuan_inference_on_gpu` uses `spaces.GPU` when importable | **PASS** |
| Resource fit | G5 | VRAM/time budget acceptable on Space hardware class | Benchmark note with hardware SKU and wall time | **OPEN** |
| Manifest parity | G6 | Manifest records adapter, quality, fallback, and trust fields same as cpu-demo | Sample manifest JSON attached to enablement PR | **OPEN** |
| Hosted E2E | G7 | Live Space run with **real** Hunyuan path (not cpu-demo fallback); Block or Vase sample | Entry in hosted-validation doc with run id + artifacts | **OPEN** |
| UX honesty | G8 | UI never implies ZeroGPU/neural reconstruction when fallback ran | Browser + API evidence; mode-validation-matrix satisfied | **OPEN** |
| Enablement PR | G9 | Explicit PR enables adapter; rollback steps documented | Merged PR link; `AGENTS.md` validation loop repeated | **OPEN** |

## Enablement procedure (when gates close)

1. Update [license-audit.md](license-audit.md) snapshot table to **Allowed** with revision pins.
2. Implement GPU-isolated generation behind `@spaces.GPU` without breaking local CPU dev.
3. Set `HunyuanPlaceholderAdapter.capabilities.configured = True` only in the same PR that satisfies G1–G8.
4. Deploy Space, run hosted E2E (G7), update [source-runtime-parity-register.md](40-operational-risk/source-runtime-parity-register.md).
5. Do **not** claim ZeroGPU validation if execution still falls back to `cpu-demo`.

## Red flags (stop)

- Enabling because "ZeroGPU runtime is available" while the adapter is still a stub.
- Skipping hosted E2E after flip of `configured`.
- Vendoring weights or sample meshes without provenance.
- Presenting preview box meshes as Hunyuan reconstruction.

## Source basis

- `[REPO]` `src/imageezgen3d/adapters/hunyuan.py` — placeholder, `configured=False`
- `[REPO]` Hosted validation records Plans 005, 012–015
- `[SYNTH]` Ideation #3 — audit prep only, no enablement in this pass
