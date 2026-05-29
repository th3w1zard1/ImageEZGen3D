---
title: "Hunyuan G9 preflight bundle (Phase AF)"
type: requirements
date: 2026-05-29
status: active
---

# Hunyuan G9 preflight bundle (Phase AF)

## Problem

After Phase AE, operators can run `hunyuan_g9_workstation_bundle.py` and get four JSON artifacts in `--record-dir`, but there is no single command that verifies cross-artifact consistency the way `hunyuan_preflight_bundle.py` does for admission audit + enablement preflight.

## Actors

- **Tier-C workstation operator** — runs G9 evidence chain before enablement PR
- **CI** — validates structural skip path without GPU
- **Enablement reviewer** — needs parity guarantees across nested enablement JSON

## Requirements

- R1. One-shot `hunyuan_g9_preflight_bundle` runs G9 workstation bundle, verifies G9 bundle record, and verifies artifact parity.
- R2. Parity fails when `g9-workstation-bundle.json.enablement` diverges from `workstation-enablement-preflight.json`.
- R3. Parity delegates admission audit ↔ enablement preflight checks via existing `verify_hunyuan_ci_artifact_parity` when those files exist.
- R4. Parity fails when `adapter_configured=true` in admission audit (enablement safety guard).
- R5. Default exit 0 on CI-like skip; `--strict` exit 1 when `workstation_evidence_ready=false`.
- R6. Does not enable adapter or claim G7 hosted PASS.

## Success criteria

- CI `hunyuan-admission-audit` uses G9 preflight bundle instead of separate G9 bundle + fixture-only path (fixtures verify retained).
- Unit tests cover parity pass, enablement mismatch, and CI-like bundle subprocess.

## Out of scope

- `IMAGEEZ_HUNYUAN_CONFIGURED=true` on Space
- G7 hosted Block/Vase attestation
- GPU inference wiring
