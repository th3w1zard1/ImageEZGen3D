# Hunyuan Admission Gates

This document is the **enablement checklist** for the `hunyuan-zerogpu` adapter. It does not authorize turning the adapter on by itself.

Legal and redistribution rules live in [license-audit.md](license-audit.md). Runtime policy lives in [zerogpu-runtime.md](zerogpu-runtime.md). Hosted honesty requirements live in [40-operational-risk/hosted-validation-2026-05-23.md](40-operational-risk/hosted-validation-2026-05-23.md).

## Current decision

**Status: NOT ENABLED**

`HunyuanPlaceholderAdapter` remains `configured=False` in code until every gate below is explicitly closed with written evidence.

## Automated audit (repo-grounded)

Run from the repository root (does **not** enable the adapter):

```bash
python scripts/hunyuan_preflight_bundle.py
python scripts/hunyuan_preflight_bundle.py --json --record-dir .
```

The bundle runs admission audit, enablement preflight, and artifact parity verify. It exits **0** while `configured=False`. Individual CLIs exit **1** if the adapter were enabled while gates remain open (safety guard for enablement PRs).

**Advanced (audit only):**

```bash
PYTHONPATH=src python scripts/hunyuan_admission_audit.py
PYTHONPATH=src python scripts/hunyuan_admission_audit.py --json
```

**Last audit:** 2026-06-13 — Phase 20–27 on `main` (PR #167–#173 + Space redeploy `a149111`); ops attestation arc **closed**; adapter `configured=False`; **G1–G6 PASS**; G7/G8/G9 **OPEN**; tier-C `--strict` capstones remain the next gate. Prior audit 2026-05-28 (Plans 078–112). Scheduled smoke runs the full guard stack while disabled — see [hosted-smoke-guard-stack-2026-05-28.md](../solutions/best-practices/hosted-smoke-guard-stack-2026-05-28.md) and live attestation index [hosted-live-attestation-2026-05-28.md](../solutions/best-practices/hosted-live-attestation-2026-05-28.md). G7 entry point: [g7-enablement-readiness-2026-05-28.md](../solutions/best-practices/g7-enablement-readiness-2026-05-28.md).

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
| Resource fit | G5 | VRAM/time budget acceptable on Space hardware class | [hunyuan-resource-fit.md](hunyuan-resource-fit.md) — 29 GB VRAM / 14.9 GB weights; `G5_STATUS: PASS` | **PASS** |
| Manifest parity | G6 | Manifest records adapter, quality, fallback, and trust fields same as cpu-demo | [hunyuan-manifest-parity.md](hunyuan-manifest-parity.md) + `tests/fixtures/hunyuan-zerogpu-manifest.sample.json`; `G6_STATUS: PASS` (sample; not live Hunyuan run) | **PASS** |
| Hosted E2E | G7 | Live Space run with **real** Hunyuan path (not cpu-demo fallback); Block or Vase sample | `## G7 validation` in hosted-validation with `G7_STATUS: PASS` | **OPEN** |
| UX honesty | G8 | UI never implies ZeroGPU/neural reconstruction when fallback ran | Interim: `validate_g8_cpu_fallback_status` in hosted golden smoke; final: `## G8 validation` + `G8_STATUS: PASS` | **OPEN** (interim checks active) |
| Enablement PR | G9 | Explicit PR enables adapter; rollback steps documented | [hunyuan-g9-enablement-runbook.md](hunyuan-g9-enablement-runbook.md); merged enablement PR link | **OPEN** |

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
