---
title: "feat: Post-trust KB refresh + golden CI artifact"
type: feat
status: completed
date: 2026-05-24
origin: docs/ideation/2026-05-23-next-focus-ideation.md
---

# feat: Post-trust KB refresh + golden CI artifact

## Summary

Close the trust-slice era with honest KB index updates (P10 verified, golden CI distinct from hosted E2E), persist golden-sample attestation JSON as a CI artifact, and publish a short ideation refresh for what to build next.

## Requirements

- R1. Update `docs/knowledgebase/README.md` caveats — P10 verified via hosted-validation record; golden CI ≠ hosted E2E
- R2. CI `golden-sample` job writes `golden-attestation.json` and uploads via `actions/upload-artifact`
- R3. Optional `--record` on `scripts/golden_sample_attestation.py` writes JSON to a path (for local/debug)
- R4. Add `docs/ideation/2026-05-24-post-trust-slice-refresh.md` with ranked next slices (Hunyuan gated, Phase 3 history compare, mesh cleanup tiers)
- R5. Add `docs/solutions/patterns/trust-slice-completion-2026-05-24.md` compound summary
- R6. Unit test for attestation JSON write; full suite passes

## Scope Boundaries

- Hunyuan enablement — out of scope
- Hosted golden sample in CI — out of scope (requires secrets/Space URL)

## Files

- Modify: `docs/knowledgebase/README.md`
- Modify: `.github/workflows/ci.yml`
- Modify: `scripts/golden_sample_attestation.py`
- Modify: `src/imageezgen3d/golden_sample.py` (optional record helper)
- Add: `docs/ideation/2026-05-24-post-trust-slice-refresh.md`
- Add: `docs/solutions/patterns/trust-slice-completion-2026-05-24.md`
- Add: `tests/test_golden_sample.py` (record test)
