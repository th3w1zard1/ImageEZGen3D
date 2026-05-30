# G7 enablement readiness (post live attestation)

**Status:** Prerequisites for *honest disabled-adapter* validation are on `main`. **G7 hosted neural E2E is still OPEN.**

## What is complete (do not redo)

| Layer | Evidence |
| --- | --- |
| Guard stack (Plans 078–106) | [hosted-smoke-guard-stack-2026-05-28.md](hosted-smoke-guard-stack-2026-05-28.md) — golden + export-tier verify, bundle verify, G7 live-probe verify while adapter disabled |
| Live attestation (Plans 107–110) | [hosted-live-attestation-2026-05-28.md](hosted-live-attestation-2026-05-28.md) — executed run ids, CPU-fallback mode labels |
| Trilogy closure (Plans 111–112) | PR #72 on `main`; KB Plan 112 merge attestation |
| Admission G1–G6 | [hunyuan-admission-gates.md](../../knowledgebase/hunyuan-admission-gates.md) — PASS with `configured=False` |
| False-neural guard | [g7-false-neural-golden-smoke-guard-2026-05-28.md](g7-false-neural-golden-smoke-guard-2026-05-28.md) |

## What remains before G7 PASS

| Gate | Requirement |
| --- | --- |
| **G7** | Live Space run with **real** Hunyuan path (not `cpu-demo`); Block or Vase sample; `G7_STATUS: PASS` in hosted-validation |
| **G8** | Post-enablement UX honesty section (interim golden-smoke checks active today) |
| **G9** | Explicit enablement PR per [hunyuan-g9-enablement-runbook.md](../../knowledgebase/hunyuan-g9-enablement-runbook.md) |

## Enablement config seam (Plan 115)

- **`IMAGEEZ_HUNYUAN_CONFIGURED`** (default `false`) sets `HunyuanPlaceholderAdapter.configured` via `AppConfig.hunyuan`.
- When `true`, `generate()` calls the GPU shell and raises **`NotImplementedError`** until inference is wired — not a G7 PASS.
- Do **not** set this on the live Space until weights, tier-C deps, and hosted neural E2E are ready.

## Recommended next execution slice

1. Run `python scripts/hunyuan_preflight_bundle.py` locally (do not commit output JSON).
2. On tier-C workstation: `PYTHONPATH=src python scripts/hunyuan_neural_enablement_preflight_bundle.py --record-dir . --strict` until `ok=true` in `neural-enablement-preflight.json`.
3. Optional drill-down: `hunyuan_configured_inference_probe.py` and `hunyuan_g7_enablement_preflight_bundle.py` for sub-gate detail.
4. Follow [hunyuan-g9-enablement-runbook.md](../../knowledgebase/hunyuan-g9-enablement-runbook.md) for the enablement PR (`IMAGEEZ_HUNYUAN_CONFIGURED=true` on Space only with G7 evidence).
5. Deploy Space; run Block/Vase; update `hosted-validation-2026-05-23.md` with `## G7 validation` only after real neural path is proven.
6. Re-run scheduled smoke; confirm manifests and downloads.

## Mode reporting (honesty)

| Mode | Claim allowed |
| --- | --- |
| Local CPU Preview / hosted `cpu-demo` fallback | Guard stack + live attestation validated |
| Real ZeroGPU Hunyuan neural | **Not** until G7 section records PASS with run id |
