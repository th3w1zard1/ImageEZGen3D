---
status: active
execution: ops
phase: "21"
program: hunyuan-g7-readiness
---

# Hosted golden smoke re-attestation (Phase 21)

## Problem

Phase 20 fixed Gradio output index drift (`preview_extras`) and redeployed Space, but golden smoke was not re-recorded in `hosted-validation-2026-05-23.md`. Export-tier attestation alone does not cover default Block/Vase golden path.

## Scope

**In:**

- Execute `hosted_golden_smoke.py` + verify for Block and Vase on live Space
- Execute `hunyuan_g7_preflight.py --live-probe` (adapter still disabled)
- Append Phase 21 section to hosted-validation doc
- Fix Phase 20 admission-gates PR reference (`#167`)

**Out:** G7 PASS, `IMAGEEZ_HUNYUAN_CONFIGURED=true`, new feature code

## Verification

```bash
PYTHONPATH=src python scripts/hosted_golden_smoke.py --record /tmp/block.json --sample assets/examples/teal_block.png
PYTHONPATH=src python scripts/verify_hosted_golden_smoke_record.py /tmp/block.json
PYTHONPATH=src python scripts/hunyuan_g7_preflight.py --live-probe --record /tmp/g7-probe.json
```
