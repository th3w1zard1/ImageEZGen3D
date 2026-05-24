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

1. **Hunyuan gate closure** — only when product intentionally enables adapter; walk G1–G9 in `docs/knowledgebase/hunyuan-admission-gates.md`. **Top priority** when enabling neural path.
2. **Mesh polish (optional)** — quadric decimation (trimesh), neural adapter hookup for decimation at export.
## Completed since this ideation doc

- **Phase 3 history compare** — MVP compare UI (PR #14), manifest JSON/MD export (PR #15), hosted smoke + KB evidence.
- **Export sidecar + decimation presets** — PR #16 merged; golden attestation + hosted Block E2E (Plan 030).
- **Hosted golden smoke CI** — scheduled workflow + `hosted_golden_smoke.py` (Plan 031).
- **Mesh decimation + RAW export** — PR #18 merged; largest-face decimation MVP + `raw.glb` tier (Plan 033/034).
- **Hosted export tier smoke** — PR #19 merged; manifest validation for draft/balanced (Plan 035/036).
- **Gradio export tier downloads** — PR #20 merged; Export sidecar + RAW GLB on Create/History (Plan 037/038).
- **Trimesh quadric decimation** — PR #22 merged; quadric simplification + hosted sidecar validation (Plan 039/040).
- **Hunyuan admission audit CLI** — Plan 041; `scripts/hunyuan_admission_audit.py` (audit-only, adapter stays disabled).

## Explicitly defer

- Marketplace, collaboration, quota systems
- Enabling Hunyuan without gate sign-off
- More KB expansion without a runtime or UX driver

## Evidence

- `[REPO]` Plans 012–022 completed; PRs #4–#12 merged
- `[REPO]` `hosted-validation-2026-05-23.md` — hosted CPU fallback E2E
- `[OPEN]` ZeroGPU on live Space
