---
status: active
execution: ops
phase: "24"
program: hunyuan-g7-readiness
---

# Full hosted guard stack re-attestation (Phase 24)

## Problem

Phase 23 re-ran golden smoke only. The scheduled guard stack also requires export-tier smokes and preflight bundle parity on live Space before tier-C enablement work.

## Requirements

| ID | Requirement |
| --- | --- |
| R1 | Block + Vase golden smoke + verify on live Space |
| R2 | Export-tier draft + balanced smoke + verify on live Space |
| R3 | G7 live probe + `hunyuan_preflight_bundle.py` on live Space context |
| R4 | Record Phase 24 in hosted-validation; sync attestation index and admission audit (PR #170) |
| R5 | Do **not** claim G7 PASS or enable Hunyuan |

## Scope

**In:** hosted-validation Phase 24, hosted-live-attestation rows, g7-enablement-readiness pointer, admission-gates refresh

**Out:** G7 PASS, tier-C `--strict`, Space redeploy, `IMAGEEZ_HUNYUAN_CONFIGURED=true`

## Verification

```bash
PYTHONPATH=src python scripts/hosted_golden_smoke.py --record /tmp/block-p24.json --sample assets/examples/teal_block.png
PYTHONPATH=src python scripts/verify_hosted_golden_smoke_record.py /tmp/block-p24.json
PYTHONPATH=src python scripts/hosted_golden_smoke.py --record /tmp/vase-p24.json --sample assets/examples/red_vase.png
PYTHONPATH=src python scripts/verify_hosted_golden_smoke_record.py /tmp/vase-p24.json
PYTHONPATH=src python scripts/hosted_export_tier_smoke.py --record /tmp/export-p24.json
PYTHONPATH=src python scripts/verify_hosted_export_tier_smoke_record.py /tmp/export-p24.json
PYTHONPATH=src python scripts/hunyuan_g7_preflight.py --live-probe --record /tmp/g7-p24.json
PYTHONPATH=src python scripts/hunyuan_preflight_bundle.py --record-dir /tmp/p24-preflight
PYTHONPATH=src python scripts/hunyuan_admission_audit.py
```
