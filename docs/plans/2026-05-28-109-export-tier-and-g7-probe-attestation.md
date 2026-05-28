---
title: Live export-tier smoke and G7 probe attestation (Plan 109)
status: completed
created: 2026-05-28
---

# Plan 109 — Export-tier smoke + G7 live probe on live Space

## Problem

Plan 107 attested golden smoke only. Scheduled smoke also runs export-tier checks and G7 live probe; fresh live evidence after Plans 078–108 is missing for those paths.

## Scope

- Run `hosted_export_tier_smoke.py --record` against live Space; verify with `verify_hosted_export_tier_smoke_record.py`.
- Run `hunyuan_g7_preflight.py --live-probe --json --record`; verify with `verify_hunyuan_g7_live_probe_record.py`.
- Record Plan 109 section in `hosted-validation-2026-05-23.md`.
- Do not commit transient JSON artifacts.

## Out of scope

- Hunyuan enablement or G7 PASS / ZeroGPU neural claims.

## Test scenarios

1. Export-tier smoke exits 0; record has draft+balanced checks with `g7_false_neural_guard_ok`.
2. G7 live probe exits 0; `hosted_probe.ok=true` while adapter disabled.

## Files

- `docs/plans/2026-05-28-109-export-tier-and-g7-probe-attestation.md`
- `docs/knowledgebase/40-operational-risk/hosted-validation-2026-05-23.md`
