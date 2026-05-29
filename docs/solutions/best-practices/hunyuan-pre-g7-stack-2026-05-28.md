# Hunyuan pre-G7 stack (Phases J–P)

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

# Admission + enablement bundle (adapter disabled)
PYTHONPATH=src python scripts/hunyuan_preflight_bundle.py
```

## Honesty constraints

- **`tier_c_available=false`** in default CI/Space builds is expected — tier C is blocked until G5–G7.
- **`DevPreviewHunyuanBackend`** and hosted **`cpu-demo`** paths must not be reported as neural Hunyuan success.
- Do **not** set **`IMAGEEZ_HUNYUAN_CONFIGURED=true`** on Space until [g7-enablement-readiness-2026-05-28.md](g7-enablement-readiness-2026-05-28.md) gates close with evidence.

## Next slice (post-P)

Integrate Tencent upstream shape+texture entrypoints inside `TencentHunyuanInferenceRunner`, then follow [hunyuan-g9-enablement-runbook.md](../../knowledgebase/hunyuan-g9-enablement-runbook.md) for the enablement PR and G7 Block/Vase hosted attestation.
