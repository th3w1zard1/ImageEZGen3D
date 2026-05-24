---
title: "feat: Ship History parity to main"
type: feat
status: completed
date: 2026-05-24
origin: docs/plans/2026-05-24-021-feat-hosted-history-session-parity-plan.md
---

# feat: Ship History parity to main

## Summary

Merge PR #12 (Plan 021 History session parity), redeploy HF Space from `main`, and confirm hosted History + golden-sample contract on the merged default branch.

## Requirements

- R1. Merge PR #12 when CI green
- R2. `unittest discover` passes on `main`
- R3. Deploy Space via `scripts/hf_space_sync.py --execute`
- R4. Hosted `/generate` Block sample completes; browser History shows run after reload
- R5. `golden_sample_attestation.py` passes on `main`
- R6. Mark Plan 022 completed; ideation reflects PR #12 merged

## Scope Boundaries

- Hunyuan enablement — out of scope

## Files

- Modify: `docs/plans/2026-05-24-022-feat-ship-history-parity-main-plan.md` (status)
- Modify: `docs/ideation/2026-05-23-next-focus-ideation.md` (completed PR list)
