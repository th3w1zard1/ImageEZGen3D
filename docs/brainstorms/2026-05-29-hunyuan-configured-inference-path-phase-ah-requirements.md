# Hunyuan configured adapter inference path (Phase AH)

**Date:** 2026-05-29  
**Status:** Requirements for `/lfg` slice after Phase AG

## Problem

`_run_hunyuan_inference_on_gpu` already delegates to `run_hunyuan_shape_texture`, but operators lack a single probe for the **configured adapter** path (`IMAGEEZ_HUNYUAN_CONFIGURED=true` + weight/runner/GPU env). Metadata still says "inference runner is not wired yet" when Tencent + GPU forward are enabled.

## Requirements

- R1. `describe_configured_adapter_inference_path()` reports adapter configured flag, backend kind, runner wiring, GPU workstation gates, and `expected_outcome` without running inference.
- R2. `scripts/hunyuan_configured_inference_probe.py` — informational exit 0; `--json` supported.
- R3. `adapter_note_for_backend` and export metadata distinguish **neural forward configured** vs **tier-C shell** when `gpu_forward` + Tencent runner are set.
- R4. Adapter integration test: mocked Tencent runner succeeds when weight backend env is set (no real GPU).
- R5. Do **not** set `IMAGEEZ_HUNYUAN_CONFIGURED=true` on Space; adapter default stays disabled.

## Non-goals

- Hosted G7 attestation or Space enablement PR.
- Another preflight bundle layer.
