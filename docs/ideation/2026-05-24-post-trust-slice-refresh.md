---
date: 2026-05-24
topic: post-trust-slice
focus: What to build after trust slice + golden CI + History parity
mode: repo-grounded
---

# Ideation: Post–Trust Slice Focus

## Context

Trust slice (Plans 012–022) is landed on `main`: fallback honesty, Phase 1 UX, Hunyuan admission docs, manifest UI, golden-sample CI (P12), History `/data` parity (PR #12). Hosted CPU fallback is validated; ZeroGPU adapter remains gated.

## Recommended next slices (ranked)

1. **Mesh cleanup / export tiers** — RAW + sidecar, decimation presets tied to quality tier (Track 4; ideation #12). **Now top priority** after Phase 3 compare shipped (PRs #14–#15).
2. **Hosted golden smoke (optional)** — scheduled workflow against live Space URL; separate from local `golden-sample` CI job.
3. **Hunyuan gate closure** — only when product intentionally enables adapter; walk G1–G9 in `docs/knowledgebase/hunyuan-admission-gates.md`.

## Completed since this ideation doc

- **Phase 3 history compare** — MVP compare UI (PR #14), manifest JSON/MD export (PR #15), hosted smoke + KB evidence.

## Explicitly defer

- Marketplace, collaboration, quota systems
- Enabling Hunyuan without gate sign-off
- More KB expansion without a runtime or UX driver

## Evidence

- `[REPO]` Plans 012–022 completed; PRs #4–#12 merged
- `[REPO]` `hosted-validation-2026-05-23.md` — hosted CPU fallback E2E
- `[OPEN]` ZeroGPU on live Space
