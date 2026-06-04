# Hunyuan pre-G7 stack (Phases J–BG)

**Status:** Landed on `main` as incremental slices before G7 neural enablement. Adapter stays **`configured=False`** on Space until G9 runbook completes.

## Slice map

| Phase | PR | Module / scripts | Purpose |
| --- | --- | --- | --- |
| **J** | #85 | `hunyuan_inference.finalize_hunyuan_exports()` | G6 export parity for mock/neural backends |
| **K** | #86 | `hunyuan_weights.ensure_hunyuan_weights()` | G2 Hub cache warm + sentinel checkpoint |
| **L** | #87 | `hunyuan_backend` dev preview + weight-verified shell | Honest local stand-in; stops before tier-C runtime |
| **M** | #88 | `hunyuan_runtime`, `hunyuan_warm_weights.py`, `hunyuan_tier_c_probe.py` | Operator probe for tier B/C imports + weight warm CLI |
| **N** | #89 | `hunyuan_tier_c_runtime`, `hunyuan_tier_c_readiness.py`, `IMAGEEZ_HUNYUAN_WEIGHT_BACKEND` | Tier B/C readiness gate + weight-backend shell |
| **O** | #90 | `hunyuan_inference_runner`, `hunyuan_inference_runner_probe.py` | Pluggable tier-C runner protocol (unwired by default) |
| **P** | #91 | `tencent_hunyuan_runner`, `IMAGEEZ_HUNYUAN_INFERENCE_RUNNER=tencent` | Tencent runner shell — checkpoint verify, honest stop |
| **Q** | #92 | `tencent_hunyuan_pipeline`, `hunyuan_tencent_pipeline_probe.py` | Staged shape+texture upstream module probes |
| **R** | #93 | `TencentStageContext`, pipeline class bindings | Resolve `Hunyuan3DDiTPipeline` / `Hunyuan3DPaintPipeline`; stop before forward |
| **S** | #94 | `TencentShapeForwardPlan`, forward contract probe | Build `from_pretrained` / `__call__` plans; stop before neural execution |
| **T** | #95 | `tencent_mesh_convert`, forward executors | Mesh conversion + injectable executors; default stops before GPU |
| **U** | #96 | `gpu_*_forward_executor`, `IMAGEEZ_HUNYUAN_GPU_FORWARD` | Opt-in GPU upstream forward; default off for CI/Space |
| **V** | #97 | `hunyuan_gpu_forward_smoke`, `hunyuan_gpu_forward_probe.py` | Workstation readiness probe (tier-C + pipeline + CUDA) |
| **W** | #98 | `attempt_gpu_forward_workstation_e2e`, `hunyuan_gpu_forward_e2e.py` | Weight-verified GPU forward attempt when gates pass |
| **X** | #99 | `hunyuan_gpu_forward_e2e_attestation`, `verify_gpu_forward_e2e_record.py` | E2E attestation record + verify for workstation evidence |
| **Y** | #100 | `attempt_gpu_forward_workstation_exports_e2e`, `hunyuan_gpu_forward_exports_e2e.py` | GPU forward E2E with G6 export finalization + artifact gates |
| **Z** | #101 | `hunyuan_gpu_forward_workstation_bundle`, `verify_gpu_forward_e2e_fixtures.py` | One-shot probe + exports attestation + record verify |
| **AA** | #102 | `hunyuan_workstation_evidence_preflight.py` | Optional local `gpu-forward-e2e.json` evidence preflight |
| **AB** | #103 | `hunyuan_workstation_enablement_preflight.py` | Bundle + evidence preflight in one operator command |
| **AC** | #104 | `hunyuan_workstation_enablement_record`, `verify_workstation_enablement_record.py` | Enablement attestation record + verify for G9 evidence |
| **AD** | #105 | `hunyuan_g9_workstation_bundle.py` | Admission preflight bundle + workstation enablement record |
| **AE** | #106 | `hunyuan_g9_workstation_bundle_record`, `verify_g9_workstation_bundle_record.py` | G9 bundle attestation record + verify for tier-C evidence |
| **AF** | #107 | `hunyuan_g9_preflight_bundle.py`, `verify_g9_workstation_artifact_parity.py` | G9 preflight bundle + cross-artifact parity |
| **AG** | #108 | `hunyuan_g7_enablement_preflight_bundle.py` | G9 preflight + G7 readiness (G1–G6) for enablement operators |
| **AH** | #109 | `hunyuan_configured_inference_probe.py` | Configured-adapter inference path report (`generate` → GPU shell → `run_hunyuan_shape_texture`) |
| **AI** | #110 | `hunyuan_neural_enablement_preflight_bundle.py` | G7 enablement preflight + configured neural path for tier-C operators |
| **AJ** | #111 | `hunyuan_neural_enablement_record`, `verify_neural_enablement_record.py` | Neural enablement attestation record + verify for tier-C evidence |
| **AK** | #112 | `verify_neural_enablement_artifact_parity.py` | Cross-artifact parity between neural and G9 workstation JSON |
| **AL** | #113 | `verify_enablement_neural_artifact_parity` (in artifact parity module) | Cross-artifact `g7_readiness` parity between enablement and neural JSON |
| **AM** | #114 | `verify_g7_live_probe_neural_artifact_parity` (in artifact parity module) | Optional cross-artifact `g7_readiness` parity when `hunyuan-g7-live-probe.json` present |
| **AN** | #115 | `--live-probe` on `hunyuan_neural_enablement_preflight_bundle.py` | One-shot neural capstone + hosted G7 live-probe record for parity |
| **AO** | #116 | `hunyuan_g7_hosted_neural_record`, `verify_hunyuan_g7_hosted_neural_record.py` | Post-enablement G7 Block/Vase status attestation JSON + verify |
| **AP** | #117 | `verify_g7_hosted_neural_enablement_artifact_parity` (in artifact parity module) | Optional hosted G7 PASS ↔ neural enablement-ready parity when both JSON present |
| **AQ** | #118 | `--hosted-neural` on `hunyuan_neural_enablement_preflight_bundle.py` | One-shot neural capstone + post-enablement G7 hosted-neural record for parity |
| **AR** | #119 | `hunyuan_g9_enablement_evidence_bundle.py` | G9 enablement PR evidence capstone + `g9-enablement-evidence.json` attestation |
| **AS** | #120 | `verify_g9_enablement_evidence_neural_artifact_parity` (in artifact parity module) | Optional G9 evidence ↔ neural enablement-ready parity when both JSON present |
| **AT** | #121 | `verify_g9_enablement_evidence_admission_artifact_parity` (in artifact parity module) | Optional G9 evidence ↔ admission audit parity when both JSON present |
| **AU** | #122 | `hunyuan_admission_g9_enablement_evidence_bundle.py` | Admission preflight + G9 enablement evidence capstone in one operator command |
| **AV** | #123 | `hunyuan_admission_g9_enablement_evidence_bundle_record`, `verify_admission_g9_enablement_evidence_bundle_record.py` | Bundle attestation record + verify for enablement PR evidence chain |
| **AW** | #124 | `verify_admission_g9_enablement_evidence_bundle_evidence_artifact_parity` (in artifact parity module) | Optional bundle record ↔ standalone G9 evidence parity when both JSON present |
| **AX** | #125 | `verify_admission_g9_enablement_evidence_bundle_evidence_artifact_parity.py`, `verify_admission_g9_enablement_evidence_bundle_evidence_artifact_parity_fixtures.py` | Dedicated bundle↔evidence parity CLI + aligned skipped fixtures + CI smoke |
| **AY** | #126 | `--strict` on G9/admission capstone CLIs | Exit 1 when `parity_ok` is false under `--strict` |
| **AZ** | #127 | `--strict` on `hunyuan_neural_enablement_preflight_bundle.py` | Exit 1 when `parity_ok` is false under `--strict` |
| **BA** | #128 | `verify_admission_g9_enablement_evidence_bundle.py` | One verify command for admission capstone JSON + bundle↔evidence parity |
| **BB** | #129 | `verify_g9_enablement_evidence_bundle.py` | One verify command for G9 evidence capstone JSON + record-dir artifact parity |
| **BC** | #130 | `verify_neural_enablement_preflight_bundle.py` | One verify command for neural capstone JSON + record-dir artifact parity |
| **BD** | #131 | `verify_enablement_evidence_capstones.py` | One verify command for all enablement capstones under `--record-dir` |
| **BE** | #132 | `hunyuan_enablement_evidence_capstones.py` | One run+verify command for admission capstone + umbrella capstone verify |
| **BF** | #133 | (CI dedup) | Drop redundant neural artifact parity CI step subsumed by Phase BE capstones preflight |
| **BG** | — | (arc closure) | Mark AS–BF plans completed; consolidate runbook preferred enablement path |

## Operator commands

```bash
# Tier B/C import surface (informational; exit 0)
PYTHONPATH=src python scripts/hunyuan_tier_c_probe.py
PYTHONPATH=src python scripts/hunyuan_tier_c_probe.py --json

# Weight pin metadata only (no Hub download)
PYTHONPATH=src python scripts/hunyuan_warm_weights.py --describe-only

# Warm pinned snapshot (requires HF token for private/gated assets)
PYTHONPATH=src python scripts/hunyuan_warm_weights.py

# Tier B/C readiness (imports + optional weight warm; informational exit 0)
PYTHONPATH=src python scripts/hunyuan_tier_c_readiness.py --skip-weight-warm
PYTHONPATH=src python scripts/hunyuan_tier_c_readiness.py --json

# Inference runner registration (informational; exit 0)
PYTHONPATH=src python scripts/hunyuan_inference_runner_probe.py

# Tencent upstream shape+texture module probe (informational; exit 0)
PYTHONPATH=src python scripts/hunyuan_tencent_pipeline_probe.py

# GPU forward workstation readiness (informational; exit 0)
PYTHONPATH=src python scripts/hunyuan_gpu_forward_probe.py
PYTHONPATH=src python scripts/hunyuan_gpu_forward_probe.py --json --skip-weight-warm

# GPU forward E2E attempt (skips on CI; tier-C workstation + env below)
export IMAGEEZ_HUNYUAN_GPU_FORWARD=true
export IMAGEEZ_HUNYUAN_INFERENCE_RUNNER=tencent
export IMAGEEZ_HUNYUAN_WEIGHT_BACKEND=true
PYTHONPATH=src python scripts/hunyuan_gpu_forward_e2e.py
PYTHONPATH=src python scripts/hunyuan_gpu_forward_e2e.py --json --skip-weight-warm
PYTHONPATH=src python scripts/hunyuan_gpu_forward_e2e.py --record gpu-forward-e2e.json

# Verify workstation E2E attestation record (ok=true requires real GPU forward evidence)
PYTHONPATH=src python scripts/verify_gpu_forward_e2e_record.py gpu-forward-e2e.json

# GPU forward exports E2E (G6 manifest/GLB/OBJ/sidecar when workstation ready)
PYTHONPATH=src python scripts/hunyuan_gpu_forward_exports_e2e.py
PYTHONPATH=src python scripts/hunyuan_gpu_forward_exports_e2e.py --record gpu-forward-e2e.json

# Workstation evidence bundle (probe + exports attestation + record verify)
PYTHONPATH=src python scripts/hunyuan_gpu_forward_workstation_bundle.py --record-dir .
PYTHONPATH=src python scripts/verify_gpu_forward_e2e_fixtures.py

# Workstation evidence preflight (optional record; does not claim G7 hosted PASS)
PYTHONPATH=src python scripts/hunyuan_workstation_evidence_preflight.py gpu-forward-e2e.json
PYTHONPATH=src python scripts/hunyuan_workstation_evidence_preflight.py gpu-forward-e2e.json --strict

# Workstation enablement preflight (bundle + evidence; tier-C operator path)
PYTHONPATH=src python scripts/hunyuan_workstation_enablement_preflight.py --record-dir .
PYTHONPATH=src python scripts/hunyuan_workstation_enablement_preflight.py --record-dir . --strict
PYTHONPATH=src python scripts/hunyuan_workstation_enablement_preflight.py --record workstation-enablement-preflight.json
PYTHONPATH=src python scripts/verify_workstation_enablement_record.py workstation-enablement-preflight.json

# G9 operator bundle (admission preflight + workstation enablement record)
PYTHONPATH=src python scripts/hunyuan_g9_workstation_bundle.py --record-dir .
PYTHONPATH=src python scripts/hunyuan_g9_workstation_bundle.py --record-dir . --strict
PYTHONPATH=src python scripts/verify_g9_workstation_bundle_record.py g9-workstation-bundle.json
PYTHONPATH=src python scripts/verify_g9_workstation_bundle_fixtures.py
PYTHONPATH=src python scripts/hunyuan_g9_preflight_bundle.py --record-dir .
PYTHONPATH=src python scripts/hunyuan_g9_preflight_bundle.py --record-dir . --strict
PYTHONPATH=src python scripts/verify_g9_workstation_artifact_parity.py --record-dir .

PYTHONPATH=src python scripts/hunyuan_g7_enablement_preflight_bundle.py --record-dir .
PYTHONPATH=src python scripts/hunyuan_g7_enablement_preflight_bundle.py --record-dir . --strict

# Configured adapter inference path (informational; adapter stays disabled on Space)
PYTHONPATH=src python scripts/hunyuan_configured_inference_probe.py --skip-weight-warm
PYTHONPATH=src python scripts/hunyuan_configured_inference_probe.py --json

PYTHONPATH=src python scripts/hunyuan_neural_enablement_preflight_bundle.py --record-dir .
PYTHONPATH=src python scripts/hunyuan_neural_enablement_preflight_bundle.py --record-dir . --live-probe
PYTHONPATH=src python scripts/hunyuan_neural_enablement_preflight_bundle.py --record-dir . --hosted-neural --status-file status.md --hosted-sample Block
PYTHONPATH=src python scripts/hunyuan_neural_enablement_preflight_bundle.py --record-dir . --strict
PYTHONPATH=src python scripts/verify_neural_enablement_preflight_bundle.py --record-dir .
PYTHONPATH=src python scripts/hunyuan_enablement_evidence_capstones.py --record-dir .
PYTHONPATH=src python scripts/hunyuan_enablement_evidence_capstones.py --record-dir . --strict
PYTHONPATH=src python scripts/hunyuan_admission_g9_enablement_evidence_bundle.py --record-dir .
PYTHONPATH=src python scripts/hunyuan_admission_g9_enablement_evidence_bundle.py --record-dir . --strict
PYTHONPATH=src python scripts/verify_enablement_evidence_capstones.py --record-dir .
PYTHONPATH=src python scripts/verify_admission_g9_enablement_evidence_bundle.py --record-dir .
PYTHONPATH=src python scripts/verify_admission_g9_enablement_evidence_bundle_record.py admission-g9-enablement-evidence-bundle.json
PYTHONPATH=src python scripts/verify_admission_g9_enablement_evidence_bundle_evidence_artifact_parity.py --record-dir .
PYTHONPATH=src python scripts/hunyuan_g9_enablement_evidence_bundle.py --record-dir .
PYTHONPATH=src python scripts/hunyuan_g9_enablement_evidence_bundle.py --record-dir . --strict --require-hosted-neural --hosted-neural --status-file status.md --hosted-sample Block
PYTHONPATH=src python scripts/verify_g9_enablement_evidence_record.py g9-enablement-evidence.json
PYTHONPATH=src python scripts/verify_neural_enablement_record.py neural-enablement-preflight.json
PYTHONPATH=src python scripts/verify_neural_enablement_record_fixtures.py
PYTHONPATH=src python scripts/verify_neural_enablement_artifact_parity.py --record-dir .

# Post-enablement G7 hosted neural evidence (after real Block/Vase run)
PYTHONPATH=src python scripts/hunyuan_g7_hosted_neural_record.py --status-file status.md --record hunyuan-g7-hosted-neural.json
PYTHONPATH=src python scripts/verify_hunyuan_g7_hosted_neural_record.py hunyuan-g7-hosted-neural.json

# Admission + enablement bundle (adapter disabled)
PYTHONPATH=src python scripts/hunyuan_preflight_bundle.py
```

## Honesty constraints

- **`tier_c_available=false`** in default CI/Space builds is expected — tier C is blocked until G5–G7.
- **`DevPreviewHunyuanBackend`** and hosted **`cpu-demo`** paths must not be reported as neural Hunyuan success.
- Do **not** set **`IMAGEEZ_HUNYUAN_CONFIGURED=true`** on Space until [g7-enablement-readiness-2026-05-28.md](g7-enablement-readiness-2026-05-28.md) gates close with evidence.

## Next slice (post-BG)

Pre-G7 **enablement evidence automation** closed at Phase BG (Phases J–BG on `main`). No further automation phases are planned unless new requirements land. Next execution slices are **operational**:

1. **Tier-C workstation:** `PYTHONPATH=src python scripts/hunyuan_enablement_evidence_capstones.py --record-dir . --strict` until `g9_enablement_evidence_ready=true` and `parity_ok=true`.
2. **Hosted G7:** live Space Block/Vase neural run; re-run with `--require-hosted-neural --hosted-neural --status-file status.md`; update hosted-validation with `G7_STATUS: PASS` — still **OPEN**.
3. **G9 enablement PR** only after G7 evidence per [hunyuan-g9-enablement-runbook.md](../../knowledgebase/hunyuan-g9-enablement-runbook.md).

Do **not** set `IMAGEEZ_HUNYUAN_CONFIGURED=true` on Space without G7 hosted neural evidence.
