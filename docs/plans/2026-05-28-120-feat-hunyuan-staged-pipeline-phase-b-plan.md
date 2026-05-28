---
title: "feat: Hunyuan staged pipeline (shape→texture contract, inference skeleton)"
type: feat
status: completed
date: 2026-05-28
origin: docs/plans/2026-05-28-119-feat-meshy-class-platform-foundation-plan.md
---

# feat: Hunyuan staged pipeline (shape→texture contract, inference skeleton)

## Summary

Advance Phase B toward G7 by wiring Hunyuan's two-tower shape→texture flow into the Plan 119 `generation.pipeline_stages` contract, adding an inference module skeleton inside the existing GPU shell, and updating G6 manifest parity — without enabling `configured=True` on Space or claiming neural validation.

---

## Problem Frame

Plan 119 reserved `shape`, `texture`, `pbr`, and `export` stages but auto-skips texture for cpu-demo/text-demo. Hunyuan3D uses sequential shape then paint towers; the orchestrator and adapter must reflect that before weights and tier-C deps land. G1–G6 are PASS with `configured=False`; G7–G9 remain OPEN.

---

## Requirements

- R1. **Staged tracker API** — `PipelineStageTracker` supports shape→texture progression without auto-skipping texture for staged adapters.
- R2. **Inference skeleton** — `hunyuan_inference.py` documents shape+texture flow; raises `NotImplementedError` until weights/backend wired.
- R3. **Adapter delegation** — `hunyuan.py` delegates to inference module; returns `pipeline_stages` in metadata when configured.
- R4. **Orchestrator integration** — For `hunyuan-zerogpu`, apply adapter-reported stages; cpu-demo/text-demo unchanged.
- R5. **G6 fixture** — Sample manifest includes `parameters.generation.pipeline_stages`.
- R6. **Trust preserved** — Default `configured=False`; preflight bundle and G7 guards still pass.

---

## Scope Boundaries

- Loading Hunyuan3D weights on Space
- Tier-C dependency install in default Space requirements
- `IMAGEEZ_HUNYUAN_CONFIGURED=true` on hosted Space
- G7 PASS attestation or hosted-validation update
- PBR map sidecar export (Phase C)

---

## Implementation Units

- U1. **Staged pipeline tracker methods** — `generation_pipeline.py` + tests
- U2. **Hunyuan inference skeleton** — `hunyuan_inference.py` + `tests/test_hunyuan_inference.py`
- U3. **Adapter + orchestrator wiring** — `hunyuan.py`, `orchestrator.py` + adapter/orchestrator tests
- U4. **G6 manifest fixture parity** — fixture JSON + manifest parity tests

---

## Key Technical Decisions

- Adapter returns `metadata["pipeline_stages"]` for staged backends; orchestrator merges into manifest.
- `pbr` stays `skipped` until Phase C; texture stage is `running→succeeded` only when inference completes.
- Injectable mock backend in inference module for unit tests only.

---

## Sources & References

- `docs/solutions/best-practices/g7-enablement-readiness-2026-05-28.md`
- `docs/knowledgebase/hunyuan-admission-gates.md`
- `docs/plans/2026-05-28-119-feat-meshy-class-platform-foundation-plan.md` (Phase B)
