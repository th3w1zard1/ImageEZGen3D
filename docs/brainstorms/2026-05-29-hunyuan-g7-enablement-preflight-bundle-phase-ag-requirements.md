---
title: "Hunyuan G7 enablement preflight bundle (Phase AG)"
type: requirements
date: 2026-05-29
status: active
---

# Hunyuan G7 enablement preflight bundle (Phase AG)

## Problem

After Phase AF, tier-C workstation automation is complete but enablement reviewers still run G9 preflight and G7 readiness checks separately. G7 enablement needs one operator command that chains both without enabling the adapter.

## Requirements

- R1. `run_g7_enablement_preflight_bundle()` runs G9 preflight bundle then `evaluate_g7_readiness()`.
- R2. `g7_enablement_preflight_ok` when G9 preflight passes and G1–G6 readiness passes.
- R3. `g7_enablement_ready` when bundle ok and `workstation_evidence_ready=true` (tier-C evidence).
- R4. CLI with `--record-dir`, `--skip-weight-warm`, `--strict`, `--json`.
- R5. Does not set `IMAGEEZ_HUNYUAN_CONFIGURED=true` or claim G7 hosted PASS.

## Out of scope

- Live Space neural generation
- Adapter enablement on Space
