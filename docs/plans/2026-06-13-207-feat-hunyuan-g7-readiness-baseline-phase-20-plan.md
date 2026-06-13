---
status: completed
execution: ops
phase: "20"
program: hunyuan-g7-readiness
---

# Hunyuan G7 readiness baseline + hosted export-tier attestation (Phase 20)

## Problem

Meshy parity closed at Phase 19. Hunyuan G7–G9 remain **OPEN**; admission docs last audited 2026-05-28. Export-tier hosted smoke was not re-run after Phases 12–19. Agents lack a current baseline section tying capstone output to blockers.

## Scope

**In:**

- Execute on live Space: `hosted_export_tier_smoke.py` (draft + balanced) + record verify
- Execute locally: `hunyuan_preflight_bundle.py`, `hunyuan_enablement_evidence_capstones.py` (record under `/tmp`, not committed)
- Append **Phase 20** section to `hosted-validation-2026-05-23.md` with run ids, mode labels, capstone blocker (`configured_adapter_neural_forward_not_ready`)
- Refresh **Last audit** in `hunyuan-admission-gates.md` (still G7/G8/G9 OPEN — no false PASS)

**Out:** `IMAGEEZ_HUNYUAN_CONFIGURED=true`, G7_STATUS PASS, inference wiring, `.cursor/plans/` mega program file

## Code fixes (hosted smoke drift)

- `GENERATE_LEADING_OUTPUT_COUNT=3` for `preview_extras` before artifact slots
- Scan `/generate` outputs for backend rail HTML (tail-slot drift vs stale Space)
- Skip `/app/` manifest artifact path disk checks in hosted validation (Gradio client)

## Files

| File | Change |
| --- | --- |
| `src/imageezgen3d/gradio_artifact_layout.py` | Leading output count + `assets_gallery` index |
| `src/imageezgen3d/hosted_golden_smoke.py` | Backend rail scan + sidecar decode + `/app/` skip |
| `src/imageezgen3d/delivery_exports.py` | `/app/` path skip in delivery manifest validation |
| `tests/test_gradio_artifact_layout.py` | Index expectations |
| `tests/test_hosted_golden_smoke.py` | Backend rail scan test |
| `docs/knowledgebase/40-operational-risk/hosted-validation-2026-05-23.md` | Phase 20 attestation section |
| `docs/knowledgebase/hunyuan-admission-gates.md` | Last audit pointer |
| `docs/solutions/best-practices/g7-enablement-readiness-2026-05-28.md` | Phase 20 baseline note |

## Verification

```bash
PYTHONPATH=src python scripts/hosted_export_tier_smoke.py --record /tmp/hosted-export-tier-phase20.json
PYTHONPATH=src python scripts/verify_hosted_export_tier_smoke_record.py /tmp/hosted-export-tier-phase20.json
PYTHONPATH=src python scripts/hunyuan_preflight_bundle.py
PYTHONPATH=src python scripts/hunyuan_enablement_evidence_capstones.py --record-dir /tmp/hunyuan-capstones-phase20
```

## Risks

- Must not claim G7 PASS or ZeroGPU neural validation.
- Export-tier smoke may fail if Space build broken — fix/deploy loop per AGENTS.md if needed.
