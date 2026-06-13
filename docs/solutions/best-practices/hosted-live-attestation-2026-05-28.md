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

## Phase 20–28 live runs (2026-06-13)

### Deploy `e368ad8` — Phases 20–24 (pre-redeploy)

After Meshy program closure and Phase 20 Gradio index repair (PR #167, #168 on `main`); Space deploy `e368ad8003640e0d81545d92ae0e536195d7d9b6`:

| Phase | Check | Run id(s) | Mode reported |
| --- | --- | --- | --- |
| 20 | Export-tier draft | `20260613-080815-cb81682c` | Hosted CPU fallback |
| 20 | Export-tier balanced | `20260613-080821-b95f913f` | Hosted CPU fallback |
| 21 | Golden smoke (Block) | `20260613-081414-7d4c8891` | Hosted CPU fallback |
| 21 | Golden smoke (Vase) | `20260613-081427-d4e091d3` | Hosted CPU fallback |
| 21 | G7 live probe | (probe record) | Space rejected `hunyuan-zerogpu`; `hosted_probe.ok=true` |
| 23 | Golden smoke (Block) | `20260613-091037-26cc856b` | Hosted CPU fallback |
| 23 | Golden smoke (Vase) | `20260613-091123-f271693b` | Hosted CPU fallback |
| 23 | G7 live probe | (probe record) | Space rejected `hunyuan-zerogpu`; `hosted_probe.ok=true` |
| 24 | Golden smoke (Block) | `20260613-092056-22306a7d` | Hosted CPU fallback |
| 24 | Golden smoke (Vase) | `20260613-092102-ca6e72c5` | Hosted CPU fallback |
| 24 | Export-tier draft | `20260613-092107-3a5c8011` | Hosted CPU fallback |
| 24 | Export-tier balanced | `20260613-092112-8764015f` | Hosted CPU fallback |
| 24 | G7 live probe + preflight bundle | (probe record) | Space rejected `hunyuan-zerogpu`; bundle ok |

### Deploy `a149111` — Phases 25–28 (post-redeploy + pause)

Hub redeploy `a1491116013b420d4c38a964df053b476ce2e19f` (PR #167 server fixes on Space):

| Phase | Check | Run id(s) | Mode reported |
| --- | --- | --- | --- |
| 25 | Hub redeploy | `a1491116013b420d4c38a964df053b476ce2e19f` | PR #167 server fixes on Space |
| 25 | Golden smoke (Block) | `20260613-092927-c307caa4` | Hosted CPU fallback |
| 25 | Golden smoke (Vase) | `20260613-092931-a8c0384d` | Hosted CPU fallback |
| 25 | Export-tier draft/balanced | `20260613-092936-9c10235e` / `20260613-092940-bfbd5e37` | Hosted CPU fallback |
| 26 | Browser E2E (Block) | `20260613-095610-69c9a820` | Hosted CPU fallback — Playwright UI path |
| 27 | Vase golden smoke + local capstone refresh | `20260613-100431-f294b98c` | Ops arc closure; tier-C handoff next |
| 28 | Tier-C `--strict` gate (expected fail, no GPU) | exit 1, blocker recorded | **Program paused** until GPU workstation |

Details: [hosted-validation-2026-05-23.md](../../knowledgebase/40-operational-risk/hosted-validation-2026-05-23.md) § Phase 20–28. **G7/G8/G9 remain OPEN**. Ops track **paused** on non-GPU hosts after Phase 28.

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
