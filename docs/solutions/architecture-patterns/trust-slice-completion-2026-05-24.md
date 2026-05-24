---
module: runtime-trust
date: 2026-05-24
problem_type: architecture_pattern
component: gradio-workflow
severity: medium
tags:
  - trust-slice
  - hosted-e2e
  - golden-sample
  - history
  - manifest-ui
---

# Trust slice completion pattern (2026-05-24)

## Problem

The scaffold had broad KB and UI ambition but users could not trust what ran on the hosted Space: fallback was silent, History lost runs, and CI upload was mistaken for E2E validation.

## What we shipped

| Layer | Outcome |
|-------|---------|
| Honesty | Fallback reason + preview disclaimer in UI and manifest |
| UX | Quality intake, comprehension exit (`## What happened`) |
| Manifest UI | `manifest_ui.py` cards reused in Create + History inspect |
| CI | `golden-sample` job — Block PNG → cpu-demo artifact gates |
| Hosted | `/data/outputs` + `demo.load()` so History survives reload |
| Gates | Hunyuan admission doc; adapter stays disabled |

## Lessons

1. **Separate attestation modes:** local golden CI ≠ hosted browser/API E2E. Document both in KB index and parity register (P10 vs P12).
2. **Space persistence:** default `outputs/` is ephemeral; use `/data/outputs` when `/data` is writable.
3. **History refresh:** build-time `list_runs()` is not enough — wire `demo.load()` to refresh History controls.

## Pointers

- [hosted-validation-2026-05-23.md](../../knowledgebase/40-operational-risk/hosted-validation-2026-05-23.md)
- [ci-upload-vs-hosted-e2e-2026-05-23.md](../best-practices/ci-upload-vs-hosted-e2e-2026-05-23.md)
- [hunyuan-admission-gates.md](../../knowledgebase/hunyuan-admission-gates.md)
