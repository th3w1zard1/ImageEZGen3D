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

## Phase 20 baseline (2026-06-13)

Export-tier hosted smoke re-attested after Meshy program closure; Hunyuan capstones re-run with expected blocker `configured_adapter_neural_forward_not_ready`. Hosted smoke helpers fixed for `preview_extras` output offset and Space `/app/` manifest paths. Evidence: [hosted-validation-2026-05-23.md](../../knowledgebase/40-operational-risk/hosted-validation-2026-05-23.md) § Phase 20.

**Phase 21 (2026-06-13):** Golden smoke Block/Vase re-attested after Phase 20 index repair; see hosted-validation § Phase 21.

**Phase 22 (2026-06-13):** Hosted-live-attestation index synced with Phase 20–21 run ids; local capstone baseline recorded (expected `configured_adapter_neural_forward_not_ready` on non-GPU host). See hosted-validation § Phase 22.

**Phase 23 (2026-06-13):** Golden smoke Block/Vase + G7 live probe re-attested after Phase 22 merge; see hosted-validation § Phase 23.

**Phase 24 (2026-06-13):** Full guard stack (golden + export-tier + preflight bundle + G7 live probe) re-attested; see hosted-validation § Phase 24.

**Phase 25 (2026-06-13):** Space redeploy (`a149111`) with PR #167 server fixes; full guard stack re-attested post-deploy; see hosted-validation § Phase 25.

**Phase 26 (2026-06-13):** Post-deploy browser E2E (Block, Playwright) closes P10 gap for deploy `a149111`; run id `20260613-095610-69c9a820`; see hosted-validation § Phase 26.

## Recommended next execution slice

1. Run `PYTHONPATH=src python scripts/hunyuan_enablement_evidence_capstones.py --record-dir .` locally (do not commit output JSON).
2. On tier-C workstation: `PYTHONPATH=src python scripts/hunyuan_enablement_evidence_capstones.py --record-dir . --strict` until `g9_enablement_evidence_ready=true` and `parity_ok=true`.
3. Optional drill-down: `hunyuan_configured_inference_probe.py` and `hunyuan_g7_enablement_preflight_bundle.py` for sub-gate detail.
4. Follow [hunyuan-g9-enablement-runbook.md](../../knowledgebase/hunyuan-g9-enablement-runbook.md) for the enablement PR (`IMAGEEZ_HUNYUAN_CONFIGURED=true` on Space only with G7 evidence).
5. Deploy Space; run Block/Vase; record status with `hunyuan_g7_hosted_neural_record.py` and verify with `verify_hunyuan_g7_hosted_neural_record.py`.
6. Update `hosted-validation-2026-05-23.md` with `## G7 validation` only after real neural path is proven (`G7_STATUS: PASS` + run id).
7. Re-run scheduled smoke; confirm manifests and downloads.

## Mode reporting (honesty)

| Mode | Claim allowed |
| --- | --- |
| Local CPU Preview / hosted `cpu-demo` fallback | Guard stack + live attestation validated |
| Real ZeroGPU Hunyuan neural | **Not** until G7 section records PASS with run id |
