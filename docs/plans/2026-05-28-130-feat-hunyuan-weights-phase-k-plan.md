---
title: "feat: Hunyuan weight cache helper (Phase K, pre-G7)"
type: feat
status: completed
date: 2026-05-28
origin: docs/solutions/best-practices/g7-enablement-readiness-2026-05-28.md
---

# feat: Hunyuan weight cache helper (Phase K, pre-G7)

## Summary

Add `hunyuan_weights.ensure_hunyuan_weights()` and config pins for `tencent/Hunyuan3D-2.1` so future inference wiring can warm the Hub cache without enabling the adapter or claiming G7 PASS.

## Requirements

- R1. Pinned repo/revision defaults match G2 documentation.
- R2. Config/env overrides for repo, revision, and cache dir.
- R3. Sentinel checkpoint validation after `snapshot_download`.
- R4. Unit tests mock Hub download; no weights in git.
- R5. Admission preflight bundle remains exit 0 with `configured=False`.

## Out of scope

- Tencent inference runtime / tier-C deps
- `IMAGEEZ_HUNYUAN_CONFIGURED=true` on Space
- G7 hosted attestation
