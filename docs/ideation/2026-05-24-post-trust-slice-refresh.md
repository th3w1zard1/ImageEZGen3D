---
date: 2026-05-24
topic: post-trust-slice
focus: What to build after trust slice + golden CI + History parity
mode: repo-grounded
---

# Ideation: Post–Trust Slice Focus

## Context

Trust slice (Plans 012–022) is landed on `main`: fallback honesty, Phase 1 UX, Hunyuan admission docs, manifest UI, golden-sample CI (P12), History `/data` parity (PR #12). Hosted CPU fallback is validated; ZeroGPU adapter remains gated.

## Guardrail track (complete)

Export tiers, hosted golden CI, quadric decimation, Gradio tier downloads, and Hunyuan admission audit (CLI + CI + scheduled workflow) are landed on `main` through PR #28 (Plan 045 docs closure). **Preflight bundle in CI** landed via PR #57 (Plans 074–077, 2026-05-27): `ci.yml` and `hosted-golden-smoke` use `hunyuan_preflight_bundle.py` instead of three separate JSON/verify steps. No further guardrail slices are queued unless product adds a new runtime or UX driver.

## Recommended next slices (ranked)

1. **Hunyuan G7 hosted E2E** — real Hunyuan path on Space (wall-clock + artifacts). **Top priority** for neural path.
2. **Hunyuan G6 manifest parity** — **done (Plan 059)** — sample manifest + validator on `main`; G7 hosted E2E still OPEN.
3. **Hunyuan G1** — **done** (Plan 049); `license-audit.md`.
4. **Hunyuan G2** — **done** (Plan 050); `hunyuan-weight-access.md`.
5. **Hunyuan G3** — **done** (Plan 052); `hunyuan-dependencies.md` + `.[hunyuan-audit]`.
6. **Hunyuan G4** — **done** (Plan 051); `@spaces.GPU` scaffold.
7. **Hunyuan G5** — **done** (Plan 053); `hunyuan-resource-fit.md` + automated G1 verify.
8. **Neural decimation hookup (optional)** — wire real adapter decimation at export when a neural path ships; quadric MVP is done.

## Completed since this ideation doc

- **Phase 3 history compare** — MVP compare UI (PR #14), manifest JSON/MD export (PR #15), hosted smoke + KB evidence.
- **Export sidecar + decimation presets** — PR #16 merged; golden attestation + hosted Block E2E (Plan 030).
- **Hosted golden smoke CI** — scheduled workflow + `hosted_golden_smoke.py` (Plan 031).
- **Mesh decimation + RAW export** — PR #18 merged; largest-face decimation MVP + `raw.glb` tier (Plan 033/034).
- **Hosted export tier smoke** — PR #19 merged; manifest validation for draft/balanced (Plan 035/036).
- **Gradio export tier downloads** — PR #20 merged; Export sidecar + RAW GLB on Create/History (Plan 037/038).
- **Trimesh quadric decimation** — PR #22 merged; quadric simplification + hosted sidecar validation (Plan 039/040).
- **Hunyuan admission audit CLI** — PR #24 merged; `scripts/hunyuan_admission_audit.py` (Plan 041/042).
- **Hunyuan CI admission gate** — PR #25 merged; `hunyuan-admission-audit` CI job on `main` (Plan 043).
- **Hosted admission audit workflow** — PR #27 merged; scheduled smoke runs audit + artifact (Plan 044/045).
- **Plan 045 docs closure** — PR #28 merged; KB + ideation sync for PR #27 ship (Plan 046).
- **Plan 046 guardrail closure** — PR #29 merged; guardrail track complete on `main` (Plan 047).
- **Plan 047 ship closure** — PR #30 merged; KB validation for PR #29 merge (Plan 048).
- **Hunyuan G1 legal audit** — Plan 049; `G1_STATUS: PASS` in license-audit (adapter still disabled).
- **Hunyuan G2 weight access** — Plan 050; `G2_STATUS: PASS` in hunyuan-weight-access (adapter still disabled).
- **Hunyuan G3 dependency audit** — Plan 052; pins + CI smoke (adapter still disabled).
- **Hunyuan G5 resource fit** — Plan 053 / PR #35; VRAM/disk budget + `hunyuan_g1_legal_verify.py` (adapter still disabled).
- **Plan 053 ship** — PR #35 merged on `main` (Plan 054).
- **Hunyuan G4 ZeroGPU wiring** — Plan 051; GPU scaffold (adapter still disabled).
- **Hunyuan preflight bundle CI** — PR #57 merged (Plans 074–077); `hunyuan_preflight_bundle.py` in `ci.yml` and scheduled smoke.
- **G7 false-neural golden smoke guard** — PR #59 merged (Plans 078–086); `g7_false_neural_guard_ok` + `validate_g7_not_false_neural_claim`.
- **Smoke JSON artifact verify** — PR #60–#62 merged (Plans 087–092); `verify_hosted_golden_smoke_record.py` and `verify_hosted_export_tier_smoke_record.py` in scheduled workflow.
- **G7 scheduled live probe** — PR #64 merged (Plans 095–096); `--live-probe` + `hunyuan-g7-live-probe.json` artifact on scheduled smoke.

## Explicitly defer

- Marketplace, collaboration, quota systems
- Enabling Hunyuan without gate sign-off
- More KB expansion without a runtime or UX driver

## Evidence

- `[REPO]` Plans 012–022 completed; PRs #4–#12 merged
- `[REPO]` `hosted-validation-2026-05-23.md` — hosted CPU fallback E2E
- `[OPEN]` ZeroGPU on live Space
