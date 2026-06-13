---
status: completed
execution: ops
phase: "26"
program: hunyuan-g7-readiness
---

# Post-deploy browser attestation (Phase 26)

## Problem

Phase 25 redeployed Space (`a149111`) and re-ran the full **Gradio API** guard stack, but AGENTS.md and the mode-validation matrix (P10) still require **browser E2E** on the live `hf.space` app after deploy. Phases 20–25 documented API attestation only; browser evidence for the post-#167 deploy is missing.

## Requirements

| ID | Requirement |
| --- | --- |
| R1 | Browser E2E on live Space: load app, run Block sample end to end |
| R2 | Confirm run id, CPU-fallback honesty, manifest + GLB + OBJ downloadable |
| R3 | Append Phase 26 section to hosted-validation; update attestation index |
| R4 | Do **not** claim G7 PASS, hosted ZeroGPU, or enable Hunyuan |

## Scope

**In:** Live Space browser smoke (Block), screenshot/snapshot evidence, doc updates

**Out:** G7 PASS, tier-C `--strict`, Space redeploy, `IMAGEEZ_HUNYUAN_CONFIGURED=true`

## Verification

```bash
# Browser (agent-browser headless)
agent-browser open https://th3w1zard1-imageezgen3d.hf.space/
# … Block sample → Generate → wait → verify artifacts …

# Repo guards (pre-commit)
PYTHONPATH=src python scripts/hunyuan_admission_audit.py
PYTHONPATH=src python scripts/verify_meshy_parity_bundle.py
```
