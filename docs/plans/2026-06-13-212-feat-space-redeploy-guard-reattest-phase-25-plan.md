---
status: completed
execution: ops
phase: "25"
program: hunyuan-g7-readiness
---

# Space redeploy + post-deploy guard stack (Phase 25)

## Problem

Phases 20–24 attested against Hub deploy `e368ad8` (Phase 19) without redeploying after PR #167 landed server-side Gradio layout and manifest validation fixes. Smoke scripts were updated client-side; Space should carry the server fixes.

## Requirements

| ID | Requirement |
| --- | --- |
| R1 | Deploy Space via `hf_space_sync.py --execute`; record new Hub commit |
| R2 | Re-run full guard stack on live Space after deploy settles |
| R3 | Append Phase 25 section to hosted-validation; update attestation index |
| R4 | Do **not** claim G7 PASS or enable Hunyuan |

## Scope

**In:** Space deploy, full hosted smoke re-attestation, doc updates

**Out:** G7 PASS, tier-C `--strict`, `IMAGEEZ_HUNYUAN_CONFIGURED=true`

## Verification

```bash
PYTHONPATH=src python scripts/hf_space_sync.py --execute
# after Space RUNNING:
PYTHONPATH=src python scripts/hosted_golden_smoke.py --record /tmp/block-p25.json --sample assets/examples/teal_block.png
PYTHONPATH=src python scripts/verify_hosted_golden_smoke_record.py /tmp/block-p25.json
PYTHONPATH=src python scripts/hosted_export_tier_smoke.py --record /tmp/export-p25.json
PYTHONPATH=src python scripts/verify_hosted_export_tier_smoke_record.py /tmp/export-p25.json
PYTHONPATH=src python scripts/hunyuan_g7_preflight.py --live-probe --record /tmp/g7-p25.json
PYTHONPATH=src python scripts/hunyuan_preflight_bundle.py --record-dir /tmp/p25-preflight
```
