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

Hunyuan G7 readiness **phase numbers (20–28)** are independent of Meshy parity phase numbers (e.g. Phase 19 closure).

Export-tier hosted smoke re-attested after Meshy program closure; Hunyuan capstones re-run with expected blocker `configured_adapter_neural_forward_not_ready`. Hosted smoke helpers fixed for `preview_extras` output offset and Space `/app/` manifest paths. Evidence: [hosted-validation-2026-05-23.md](../../knowledgebase/40-operational-risk/hosted-validation-2026-05-23.md) § Phase 20.

**Phase 21 (2026-06-13):** Golden smoke Block/Vase re-attested after Phase 20 index repair; see hosted-validation § Phase 21.

**Phase 22 (2026-06-13):** Hosted-live-attestation index synced with Phase 20–21 run ids; local capstone baseline recorded (expected `configured_adapter_neural_forward_not_ready` on non-GPU host). See hosted-validation § Phase 22.

**Phase 23 (2026-06-13):** Golden smoke Block/Vase + G7 live probe re-attested after Phase 22 merge; see hosted-validation § Phase 23.

**Phase 24 (2026-06-13):** Full guard stack (golden + export-tier + preflight bundle + G7 live probe) re-attested; see hosted-validation § Phase 24.

**Phase 25 (2026-06-13):** Space redeploy (`a149111`) with PR #167 server fixes; full guard stack re-attested post-deploy; see hosted-validation § Phase 25.

**Phase 26 (2026-06-13):** Post-deploy browser E2E (Block, Playwright) closes P10 gap for deploy `a149111`; run id `20260613-095610-69c9a820`; see hosted-validation § Phase 26.

**Phase 27 (2026-06-13):** Ops arc closure — capstone/preflight baseline refresh + Vase golden smoke; see hosted-validation § Phase 27.

**Phase 28 (2026-06-13):** Tier-C `--strict` gate attestation (exit 1 on non-GPU host); plan hygiene; **program paused**; see hosted-validation § Phase 28.

**Meshy plan registry (Phases 30–31, 2026-06-13):** All Meshy implementation plans marked completed; Phase 32 adds repo-wide plan registry guard. Meshy `/lfg` track is closed — do not re-open from stale frontmatter.

## Ops attestation arc closure (Phases 20–27)

Phases 20–27 on `main` complete the **disabled-adapter honesty** attestation program on two deploy bands:

| Deploy commit | Phases | Scope |
| --- | --- | --- |
| `e368ad8003640e0d81545d92ae0e536195d7d9b6` | 20–24 | Guard stack re-attestation (pre-redeploy Space) |
| `a1491116013b420d4c38a964df053b476ce2e19f` | 25–27 | Redeploy (PR #167 server fixes), browser E2E, ops closure |

**Do not repeat** full guard-stack loops on non-GPU hosts unless Space runtime code changes. Phase 28 **paused** the program pending tier-C GPU — the arc is **complete**, not ongoing.

| Done on this host | Blocked until tier-C GPU |
| --- | --- |
| Golden/export-tier smokes + G7 live probe | `hunyuan_enablement_evidence_capstones.py --strict` |
| Space redeploy + browser Block E2E | Real Hunyuan neural forward + hosted G7 record |
| Local capstone baseline (`configured_adapter_neural_forward_not_ready`) | `g9_enablement_evidence_ready=true` |
| Admission G1–G6 PASS, adapter `configured=False` | Enablement PR per [hunyuan-g9-enablement-runbook.md](../../knowledgebase/hunyuan-g9-enablement-runbook.md) |

### Tier-C handoff (single operator path)

```bash
# On CUDA workstation with tier-C deps installed:
PYTHONPATH=src python scripts/hunyuan_enablement_evidence_capstones.py --record-dir . --strict
# Must exit 0 with g9_enablement_evidence_ready=true before Space enablement
```

Then follow **Recommended next execution slice** steps 4–7 below (enablement PR → hosted neural record → G7 validation section → scheduled smoke).

## Program pause (Phase 28, 2026-06-13)

**Ops attestation track paused** on non-GPU CI hosts after Phase 27. Phase 28 recorded `--strict` capstone exit **1** with `configured_adapter_neural_forward_not_ready`. Do **not** run further Phases 20–27-style guard-stack `/lfg` loops unless Space runtime code changes.

**Resume `/lfg` on the tier-C enablement track only:** tier-C GPU workstation; `hunyuan_enablement_evidence_capstones.py --strict` exits 0 with `g9_enablement_evidence_ready=true`; then enablement runbook + hosted neural G7 record.

## Recommended next execution slice

1. *(Optional — skip if Phase 27/28 baseline unchanged)* Run `PYTHONPATH=src python scripts/hunyuan_enablement_evidence_capstones.py --record-dir .` locally (do not commit output JSON).
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
