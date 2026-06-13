---
status: active
execution: ops
phase: "23"
program: hunyuan-g7-readiness
---

# Hosted smoke guard re-attestation (Phase 23)

## Problem

After Phase 22 attestation index sync, scheduled guard stack should be re-run on live Space to confirm golden + G7 live-probe honesty still holds on current deploy.

## Requirements

| ID | Requirement |
| --- | --- |
| R1 | Run Block + Vase `hosted_golden_smoke.py` + verify on live Space |
| R2 | Run `hunyuan_g7_preflight.py --live-probe` (adapter disabled) |
| R3 | Append Phase 23 section to hosted-validation; sync admission-gates audit line (PR #169) |
| R4 | Do **not** claim G7 PASS or enable Hunyuan |

## Scope

**In:** hosted-validation Phase 23, g7-enablement-readiness pointer, admission-gates last-audit refresh

**Out:** G7 PASS, `IMAGEEZ_HUNYUAN_CONFIGURED=true`, Space redeploy, tier-C `--strict`

## Verification

```bash
PYTHONPATH=src python scripts/hosted_golden_smoke.py --record /tmp/block-p23.json --sample assets/examples/teal_block.png
PYTHONPATH=src python scripts/verify_hosted_golden_smoke_record.py /tmp/block-p23.json
PYTHONPATH=src python scripts/hosted_golden_smoke.py --record /tmp/vase-p23.json --sample assets/examples/red_vase.png
PYTHONPATH=src python scripts/verify_hosted_golden_smoke_record.py /tmp/vase-p23.json
PYTHONPATH=src python scripts/hunyuan_g7_preflight.py --live-probe --record /tmp/g7-probe-p23.json
PYTHONPATH=src python scripts/hunyuan_admission_audit.py
```
