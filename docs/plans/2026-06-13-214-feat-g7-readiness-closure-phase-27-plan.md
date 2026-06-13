---
status: completed
execution: ops
phase: "27"
program: hunyuan-g7-readiness
---

# G7 readiness ops arc closure + tier-C handoff (Phase 27)

## Problem

Phases 20–26 completed post-Meshy attestation on deploy `e368ad8` (Phases 20–24) and `a149111` (Phases 25–26: redeploy + browser E2E), but the ops program lacked an explicit **closure** section and a refreshed **local capstone baseline** anchored to current `main`.

## Requirements

| ID | Requirement |
| --- | --- |
| R1 | Re-run `hunyuan_enablement_evidence_capstones.py` (non-strict) and document expected blocker |
| R2 | Re-run `hunyuan_preflight_bundle.py` locally and record summary |
| R3 | Re-run hosted golden smoke (Vase, `red_vase.png`) on live Space — complements Phase 26 browser Block |
| R4 | Append Phase 27 + **ops arc closure** section; tier-C handoff checklist in g7-enablement-readiness |
| R5 | Do **not** claim G7 PASS, enable Hunyuan, or redeploy Space |

## Scope

**In:** Local capstone/preflight refresh, one hosted Vase golden smoke, closure/handoff docs

**Out:** G7 PASS, tier-C `--strict`, Space redeploy, `IMAGEEZ_HUNYUAN_CONFIGURED=true`

## Verification

```bash
PYTHONPATH=src python scripts/hunyuan_enablement_evidence_capstones.py --record-dir /tmp/phase27-capstones
PYTHONPATH=src python scripts/verify_enablement_evidence_capstones.py --record-dir /tmp/phase27-capstones
PYTHONPATH=src python scripts/hunyuan_preflight_bundle.py --record-dir /tmp/phase27-preflight
PYTHONPATH=src python scripts/hosted_golden_smoke.py --record /tmp/vase-p27.json --sample assets/examples/red_vase.png
PYTHONPATH=src python scripts/verify_hosted_golden_smoke_record.py /tmp/vase-p27.json
PYTHONPATH=src python scripts/hunyuan_admission_audit.py
PYTHONPATH=src python scripts/verify_meshy_parity_bundle.py
```
