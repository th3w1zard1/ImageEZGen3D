---
title: "feat: Hunyuan G5 resource fit + G1 legal verify automation"
type: feat
status: completed
date: 2026-05-25
origin: docs/ideation/2026-05-24-next-runtime-slice.md
---

# feat: Hunyuan G5 resource fit + G1 legal verify automation

## Summary

Close admission **G5** with documented VRAM/disk budget (upstream 29 GB / Hub 14.9 GB) and add **automated G1** LICENSE verification script. Adapter stays `configured=False`.

## Requirements

- R1. `hunyuan-resource-fit.md` with `G5_STATUS: PASS`
- R2. `scripts/hunyuan_resource_estimate.py` + `scripts/hunyuan_g1_legal_verify.py`
- R3. Admission evaluator G5 **PASS**; gates doc updated
- R4. G1 agent gate close note in `license-audit.md`
- R5. Tests + CI smoke for verify scripts

## Completion

- G7 wall-clock remains open until real Hunyuan hosted run.
