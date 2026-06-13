---
status: active
execution: ops
phase: "22"
program: hunyuan-g7-readiness
---

# Hosted attestation index sync + local capstone baseline (Phase 22)

## Problem

Phase 20–21 re-attested export-tier and golden smokes on live Space, but [hosted-live-attestation-2026-05-28.md](../solutions/best-practices/hosted-live-attestation-2026-05-28.md) still indexes only Plans 107–110. Readers miss the latest run ids. Local enablement capstone baseline on this CI host (no GPU) should be recorded to anchor tier-C next steps without claiming G7 PASS.

## Requirements

| ID | Requirement |
| --- | --- |
| R1 | Extend hosted-live-attestation index with Phase 20 export-tier + Phase 21 golden run ids |
| R2 | Run `hunyuan_enablement_evidence_capstones.py --record-dir /tmp/...` (non-strict) and document expected blockers |
| R3 | Add Phase 22 pointer in g7-enablement-readiness + hosted-validation cross-links |
| R4 | Do **not** claim G7 PASS, ZeroGPU neural validation, or enable Hunyuan on Space |

## Scope

**In:**

- Update `docs/solutions/best-practices/hosted-live-attestation-2026-05-28.md`
- Append Phase 22 ops note to `docs/knowledgebase/40-operational-risk/hosted-validation-2026-05-23.md`
- Update `docs/solutions/best-practices/g7-enablement-readiness-2026-05-28.md`
- Refresh admission-gates last-audit line (Phase 22 index sync)

**Out:** G7 PASS, `IMAGEEZ_HUNYUAN_CONFIGURED=true`, tier-C `--strict` capstones (requires GPU workstation), Space redeploy

## Verification

```bash
PYTHONPATH=src python scripts/hunyuan_enablement_evidence_capstones.py --record-dir /tmp/phase22-capstones
PYTHONPATH=src python scripts/verify_enablement_evidence_capstones.py --record-dir /tmp/phase22-capstones
PYTHONPATH=src python scripts/hunyuan_admission_audit.py
PYTHONPATH=src python scripts/verify_meshy_parity_bundle.py
```
