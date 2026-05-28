---
title: "feat: Hunyuan export parity finalize (Phase J, pre-G7)"
type: feat
status: completed
date: 2026-05-28
origin: docs/solutions/best-practices/g7-enablement-readiness-2026-05-28.md
---

# feat: Hunyuan export parity finalize (Phase J, pre-G7)

## Summary

Add shared Hunyuan export finalization (decimation, `export_sidecar`, multi-format exports) so mock and future neural backends produce G6-shaped artifacts. Keeps `configured=False` on Space and does not claim G7 PASS.

## Requirements

- R1. `finalize_hunyuan_exports()` mirrors cpu-demo export contract.
- R2. Inference backend protocol returns meshes; `run_hunyuan_shape_texture` finalizes exports.
- R3. Mock backend tests assert `export_sidecar` and staged pipeline stages.
- R4. Default path still raises `NotImplementedError` without backend.
- R5. Admission preflight bundle remains exit 0 with `configured=False`.

## Out of scope

- Tencent Hunyuan3D weight load / tier-C deps
- `IMAGEEZ_HUNYUAN_CONFIGURED=true` on Space
- G7 hosted attestation update
