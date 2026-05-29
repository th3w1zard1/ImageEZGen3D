# Hunyuan pre-G7 stack (Phases J–AE)

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

# Admission + enablement bundle (adapter disabled)
PYTHONPATH=src python scripts/hunyuan_preflight_bundle.py
```

## Honesty constraints

- **`tier_c_available=false`** in default CI/Space builds is expected — tier C is blocked until G5–G7.
- **`DevPreviewHunyuanBackend`** and hosted **`cpu-demo`** paths must not be reported as neural Hunyuan success.
- Do **not** set **`IMAGEEZ_HUNYUAN_CONFIGURED=true`** on Space until [g7-enablement-readiness-2026-05-28.md](g7-enablement-readiness-2026-05-28.md) gates close with evidence.

## Next slice (post-AE)

On a tier-C workstation: `hunyuan_g9_workstation_bundle.py --record-dir . --strict` until `g9-workstation-bundle.json` has `ok=true`, then follow [hunyuan-g9-enablement-runbook.md](../../knowledgebase/hunyuan-g9-enablement-runbook.md).
