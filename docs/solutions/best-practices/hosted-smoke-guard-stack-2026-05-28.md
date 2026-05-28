---
title: Hosted smoke guard stack (golden, export-tier, G7)
date: 2026-05-28
category: best-practices
module: hosted-golden-smoke
problem_type: best_practice
component: ci
severity: high
applies_when:
  - "Changing hosted-golden-smoke workflow or smoke JSON artifacts"
  - "Debugging false G7 neural claims before Hunyuan enablement"
  - "Onboarding agents to scheduled hosted validation"
tags: [hosted-golden-smoke, hunyuan, g7, admission-gates, ci, fallback-honesty]
---

# Hosted smoke guard stack (Plans 078–100)

## Context

While Hunyuan remains disabled, scheduled smoke must prove **cpu-demo honesty** and reject **false G7 neural success**. The stack is layered: in-run guard → per-artifact JSON verify → bundle verify → G7 live-probe verify.

## Scheduled workflow order

| Step | Artifact / action | Verify |
| --- | --- | --- |
| Golden smoke | `hosted-golden-smoke.json` | `verify_hosted_golden_smoke_record.py` |
| Export tier | `hosted-export-tier-smoke.json` | `verify_hosted_export_tier_smoke_record.py` |
| Bundle | both files | `verify_hosted_smoke_artifacts.py` |
| G7 live probe | `hunyuan-g7-live-probe.json` | `verify_hunyuan_g7_live_probe_record.py` |
| Preflight | audit + enablement JSON | `hunyuan_preflight_bundle.py` |

## Key fields and guards

- **`g7_false_neural_guard_ok`** on golden/export-tier records — see [g7-false-neural-golden-smoke-guard-2026-05-28.md](g7-false-neural-golden-smoke-guard-2026-05-28.md).
- **G7 live probe** — Space must not return G7-valid neural status when `adapter=hunyuan-zerogpu` is requested while disabled — see [hunyuan-g7-live-probe-scheduled-smoke-2026-05-28.md](hunyuan-g7-live-probe-scheduled-smoke-2026-05-28.md).

## Local debug (copy-paste)

```bash
PYTHONPATH=src python scripts/hosted_golden_smoke.py --json --record hosted-golden-smoke.json
PYTHONPATH=src python scripts/verify_hosted_golden_smoke_record.py hosted-golden-smoke.json
PYTHONPATH=src python scripts/verify_hosted_export_tier_smoke_record.py hosted-export-tier-smoke.json
PYTHONPATH=src python scripts/verify_hosted_smoke_artifacts.py
PYTHONPATH=src python scripts/hunyuan_g7_preflight.py --live-probe --json --record hunyuan-g7-live-probe.json
PYTHONPATH=src python scripts/verify_hunyuan_g7_live_probe_record.py hunyuan-g7-live-probe.json
```

## Not G7 closure

Passing this stack does **not** set `G7_STATUS: PASS` in hosted-validation — that requires a real neural Hunyuan run after enablement per [hunyuan-g9-enablement-runbook.md](../../knowledgebase/hunyuan-g9-enablement-runbook.md).

## Related learnings

- [hosted-golden-smoke-record-verify-2026-05-28.md](hosted-golden-smoke-record-verify-2026-05-28.md)
- [hosted-export-tier-smoke-record-verify-2026-05-28.md](hosted-export-tier-smoke-record-verify-2026-05-28.md)
- [g7-false-neural-golden-smoke-guard-2026-05-28.md](g7-false-neural-golden-smoke-guard-2026-05-28.md)
- [hunyuan-g7-live-probe-scheduled-smoke-2026-05-28.md](hunyuan-g7-live-probe-scheduled-smoke-2026-05-28.md)
