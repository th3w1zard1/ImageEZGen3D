---
title: Hosted live attestation trilogy (Plans 107–110)
date: 2026-05-28
category: best-practices
module: hosted-golden-smoke
problem_type: best_practice
component: validation
severity: high
applies_when:
  - "Re-validating live Space after guard-stack changes"
  - "Reporting hosted validation modes to users or KB"
  - "Distinguishing scheduled smoke honesty from G7 closure"
tags: [hosted-validation, hosted-golden-smoke, hunyuan, g7, fallback-honesty]
---

# Hosted live attestation trilogy (Plans 107–110)

## Context

After Plans 078–106 landed the **scheduled smoke guard stack**, Plans 107–110 re-ran live checks against https://th3w1zard1-imageezgen3d.hf.space/ and recorded evidence in [hosted-validation-2026-05-23.md](../../knowledgebase/40-operational-risk/hosted-validation-2026-05-23.md).

Pair with [hosted-smoke-guard-stack-2026-05-28.md](hosted-smoke-guard-stack-2026-05-28.md) for CI verify CLIs.

## Recorded live runs (2026-05-28)

| Plan | Check | Run id(s) | Mode reported |
| --- | --- | --- | --- |
| 107 | Golden smoke (Block) | `20260528-024123-5bf694b9` | Hosted CPU fallback — Local CPU Preview |
| 109 | Export-tier draft | `20260528-025824-1345fc91` | Hosted CPU fallback |
| 109 | Export-tier balanced | `20260528-025828-ef91630a` | Hosted CPU fallback |
| 109 | G7 live probe | (probe record) | Space rejected `hunyuan-zerogpu`; `hosted_probe.ok=true` |

All records had `g7_false_neural_guard_ok=true` where applicable.

## Local replay commands

```bash
PYTHONPATH=src python scripts/hosted_golden_smoke.py --json --record hosted-golden-smoke.json
PYTHONPATH=src python scripts/verify_hosted_golden_smoke_record.py hosted-golden-smoke.json

PYTHONPATH=src python scripts/hosted_export_tier_smoke.py --record hosted-export-tier-smoke.json
PYTHONPATH=src python scripts/verify_hosted_export_tier_smoke_record.py hosted-export-tier-smoke.json

PYTHONPATH=src python scripts/hunyuan_g7_preflight.py --live-probe --json --record hunyuan-g7-live-probe.json
PYTHONPATH=src python scripts/verify_hunyuan_g7_live_probe_record.py hunyuan-g7-live-probe.json

PYTHONPATH=src python scripts/verify_hosted_smoke_artifacts.py
```

## Mode reporting (required)

| Claim | Allowed when |
| --- | --- |
| Hosted CPU fallback validated | Golden/export-tier smokes pass on live Space with Local CPU Preview |
| G7 honesty while disabled | Live probe passes; adapter not in Gradio choices or no false neural status |
| G7 gate closed | Live Hunyuan neural run + `G7_STATUS: PASS` in hosted-validation — **not** met by Plans 107–110 |
| ZeroGPU neural validated | Real `hunyuan-zerogpu` generation on Space — **not** met while adapter disabled |

## Related

- [hosted-smoke-guard-stack-2026-05-28.md](hosted-smoke-guard-stack-2026-05-28.md)
- [g7-false-neural-golden-smoke-guard-2026-05-28.md](g7-false-neural-golden-smoke-guard-2026-05-28.md)
- [hunyuan-g7-live-probe-scheduled-smoke-2026-05-28.md](hunyuan-g7-live-probe-scheduled-smoke-2026-05-28.md)
