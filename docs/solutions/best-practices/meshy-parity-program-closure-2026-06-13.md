---
title: Meshy parity program closure (Phases U–18)
date: 2026-06-13
category: best-practices
module: meshy-parity
problem_type: best_practice
component: documentation
severity: low
applies_when:
  - "Closing a Meshy parity program wave or refreshing PARITY-MATRIX"
  - "Adding viewer mesh-op or Meshy-shaped API routes"
  - "Before declaring Meshy parity complete for a slice"
tags: [meshy, parity-matrix, workspace-ui, mesh-ops, hosted-smoke, verification]
---

# Meshy parity program closure (Phases U–18)

## Context

The Meshy Parity + Blender Toolset program landed in two doc-verified waves. Phase 8 refreshed `PARITY-MATRIX.md` after Phases U–7. Phases 12–18 added API/viewer wiring and hosted re-attestation without a matching matrix + solutions closure pass.

## Phase map (second wave)

| Phase | Deliverable |
| --- | --- |
| 12 | Viewer Retry / Download / Send-to handoffs |
| 13 | Boolean mesh-op job modalities (`boolean-union` / `difference` / `intersection`) |
| 14 | Multi-image-to-3d Meshy API + orchestrator intake |
| 15 | Multi-color print 3MF job route + `write_multi_color_3mf` |
| 16 | Viewer Multi-Color 3MF button |
| 17 | Viewer boolean ops + second-mesh file picker |
| 18 | Hosted re-attestation (Space deploy + golden smoke + G7 live probe) |

Authoritative capability rows: [PARITY-MATRIX.md](../../reference/meshy/PARITY-MATRIX.md).

## Trust boundaries (unchanged)

- **demo** adapters are honest stand-ins; **gated** paths (`hunyuan`, `text_neural`) stay disabled until G1–G8 close.
- **real** mesh-ops may require optional engines at runtime (e.g. manifold3d/Blender for booleans, xatlas for UV).
- Hosted attestation in Phase 18 used **CPU fallback** (`cpu-demo`); do not report ZeroGPU/Hunyuan neural validation from that pass.

## Local verify (copy-paste)

```bash
PYTHONPATH=src python scripts/verify_meshy_parity_bundle.py
PYTHONPATH=src python -m pytest tests/test_meshy_parity_matrix.py tests/test_workspace_ui.py -q
```

## Hosted verify (when touching Space/runtime)

Per `AGENTS.md`:

1. `PYTHONPATH=src python scripts/hf_space_sync.py --execute`
2. `PYTHONPATH=src python scripts/hosted_golden_smoke.py --record /tmp/hosted-golden.json --json`
3. `PYTHONPATH=src python scripts/verify_hosted_golden_smoke_record.py /tmp/hosted-golden.json`

Record outcomes in [hosted-validation-2026-05-23.md](../../knowledgebase/40-operational-risk/hosted-validation-2026-05-23.md).

## Viewer wiring invariant

`workspace_ui.VIEWER_ACTION_STUBS` must stay empty when all preview affordances queue jobs. Regression: `tests/test_workspace_ui.py` + `tests/test_meshy_parity_matrix.py`.

## Phase 30 — plan status closure (2026-06-13)

Implementation for Phases 10–17 (`program: meshy-parity` plans 196–204) was already landed and reflected in `PARITY-MATRIX.md`, but plan frontmatter still showed `status: active`. Phase 30 marks those plans **completed** and adds `test_meshy_parity_plans_are_marked_completed` so agents do not re-open finished slices.

## Next frontier (out of Meshy parity)

Hunyuan G7 enablement — run `python scripts/hunyuan_preflight_bundle.py` and close G1–G8 per [hunyuan-g9-enablement-runbook.md](../../knowledgebase/hunyuan-g9-enablement-runbook.md).

## Related

- [meshy-class-automation-stack-2026-05-28.md](meshy-class-automation-stack-2026-05-28.md) — jobs/automation layer
- Plan: [206-feat-meshy-parity-program-closure-phase-19-plan.md](../../plans/2026-06-13-206-feat-meshy-parity-program-closure-phase-19-plan.md)
- Plan: [217-feat-meshy-plan-status-closure-phase-30-plan.md](../../plans/2026-06-13-217-feat-meshy-plan-status-closure-phase-30-plan.md)
