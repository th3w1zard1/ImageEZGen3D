---
title: Scheduled G7 live probe while Hunyuan adapter is disabled
date: 2026-05-28
category: best-practices
module: hunyuan-g7-preflight
problem_type: best_practice
component: ci
severity: high
applies_when:
  - "Changing hunyuan_g7_preflight or hosted-golden-smoke workflow"
  - "Debugging false G7 neural claims before enablement"
  - "Reviewing hunyuan-g7-live-probe.json artifacts"
tags: [hunyuan, g7, hosted-golden-smoke, admission-gates, fallback-honesty]
---

# Scheduled G7 live probe while Hunyuan adapter is disabled

## Context

G1–G6 can pass in-repo while G7 remains **OPEN**. Golden smoke enforces cpu-demo honesty via [g7-false-neural-golden-smoke-guard-2026-05-28.md](g7-false-neural-golden-smoke-guard-2026-05-28.md). A separate check is needed: when a client requests `adapter=hunyuan-zerogpu` on the live Space, the response must **not** look like a successful G7 neural run.

## Guidance

| Step | Command / artifact |
| --- | --- |
| Local + network | `PYTHONPATH=src python scripts/hunyuan_g7_preflight.py --live-probe --json` |
| Scheduled smoke | `--live-probe --record hunyuan-g7-live-probe.json` in `hosted-golden-smoke.yml` |
| Verify artifact | `PYTHONPATH=src python scripts/verify_hunyuan_g7_live_probe_record.py` |
| Smoke JSON bundle | `PYTHONPATH=src python scripts/verify_hosted_smoke_artifacts.py` |

**Expected while disabled:** `hosted_probe.ok=true` with a `probe_note` that the Space rejected the hunyuan adapter (e.g. not in Gradio choices) or did not return G7-valid neural status.

**Not G7 closure:** Passing the live probe does **not** set `G7_STATUS: PASS` — that requires a real neural Hunyuan run after enablement.

## Agent checks

- Unit + subprocess: `tests/test_hunyuan_g7_preflight.py` (`test_verify_hunyuan_g7_live_probe_record_cli_subprocess`).
- Invalid records must exit 1 with `hosted_probe` mentioned on stderr.

## Related

- [g7-false-neural-golden-smoke-guard-2026-05-28.md](g7-false-neural-golden-smoke-guard-2026-05-28.md)
- [hosted-golden-smoke-record-verify-2026-05-28.md](hosted-golden-smoke-record-verify-2026-05-28.md)
- [hosted-export-tier-smoke-record-verify-2026-05-28.md](hosted-export-tier-smoke-record-verify-2026-05-28.md)
- Plan 095 — `docs/plans/2026-05-28-095-g7-live-probe-scheduled-smoke.md`
- Plan 097 — `docs/plans/2026-05-28-097-g7-live-probe-learning-and-verify.md`
