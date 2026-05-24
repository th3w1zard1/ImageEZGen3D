# Frontier Image-to-3D Tracking (May 2026)

**Evidence tier:** Tier 3 — frontier / adjacent tracking  
**Product truth:** This document is **not** current product truth. It records emerging directions to watch, not commitments to ship.

**Last updated:** 2026-05-23  
**Related:** [3d-reconstruction-theory.md](../3d-reconstruction-theory.md), [zerogpu-runtime.md](../zerogpu-runtime.md), [creator-product-patterns.md](../creator-product-patterns.md)

---

## Purpose

Track 2025–2026 adjacent research and platform patterns relevant to ImageEZGen3D: a ZeroGPU-first Gradio image-to-3D scaffold on Hugging Face Spaces with explicit CPU fallback, manifest/GLB/OBJ exports, and creator-workspace UX fidelity.

---

## 1. Feed-forward / single-image 3D reconstruction

| Signal | Evidence | Repo implication |
|--------|----------|------------------|
| Large feed-forward models (TripoSR-class, LRM variants, Hunyuan3D, TRELLIS-style sparse-structure + mesh decoders) dominate single-image demos | `[SYNTH]` from `[REPO]` model-matrix + `[OFFICIAL]` HF model cards (2025–2026) | **Track:** adapter admission criteria in model-matrix; **Implement now:** keep mesh as canonical export, not splat-only preview |
| Single-image output remains ambiguity-managed, not metrology-grade | `[REPO]` 3d-reconstruction-theory.md | **Implement now:** retain capture hints, quality modes, and honest "draft" labeling in UI |
| Hybrid mesh + texture pipelines beat pure NeRF for creator editability | `[SYNTH]` aligned with theory doc | **Track:** texture-aware mesh decoders; **Defer:** splat-first user artifacts |
| Sub-second inference on A100-class hardware does not imply sub-second on ZeroGPU cold start | `[OPEN]` hosted latency unverified for this repo | **Implement now:** manifest records adapter path + fallback; **Track:** cold-start benchmarks on HF Spaces |

**Frontier watch (non-current truth):**

- Gaussian-splat or triplane latents as *internal* representations with mandatory mesh extraction for export.
- Multi-view conditioning without full photogrammetry capture (2–4 synthetic views from one photo).
- License-gated commercial models (Hunyuan, proprietary APIs) — admission only after license-audit pass.

---

## 2. Creator-tool UX patterns (image-to-3D)

| Pattern | Evidence | Repo implication |
|---------|----------|------------------|
| Composer-first layout: brief → upload → primary CTA above fold | `[UI]` design review May 2026; `[REPO]` ui-fidelity checklist | **Implement now:** composer-grid before starter-card-row (layout reorder) |
| Starter templates as accelerators, not the hero | `[REPO]` creator-product-patterns, reference-creator-workspace-audit | **Implement now:** templates below composer; **Track:** image-led thumbnails on cards |
| Explicit mode path in result surface (adapter, fallback, run id) | `[REPO]` agent-operating-contract, mode-validation-matrix | **Implement now:** never hide fallback behind success chrome |
| Artifact rail with downloadable manifest/GLB/OBJ | `[REPO]` export-guide, verification.md | **Implement now:** keep three-artifact contract |
| Progress as staged pipeline, not spinner-only | `[SYNTH]` competitive-product-benchmark-2026 | **Track:** step labels tied to orchestrator phases |

**Anti-patterns to avoid (Tier 3 advisory):**

- Generic "AI slop" hero with vague taglines and buried Generate button.
- Claiming ZeroGPU when CPU demo path ran.
- Preview-only 3D viewers with no export trust chain.

---

## 3. ZeroGPU / serverless GPU on Hugging Face

| Pattern | Evidence | Repo implication |
|---------|----------|------------------|
| `@spaces.GPU`-decorated functions for inference bursts | `[OFFICIAL]` HF ZeroGPU docs; `[REPO]` zerogpu-runtime.md | **Implement now:** GPU work inside decorated handlers only |
| Strict runtime detection (Spaces markers + `spaces` import) | `[REPO]` runtime.py policy | **Implement now:** fail honestly when markers absent |
| CPU fallback as explicit product mode, not silent degradation | `[REPO]` mode-validation-matrix | **Implement now:** label fallback in UI + manifest |
| Hunyuan ZeroGPU adapter gated pending license/deps | `[REPO]` config.py, model-matrix | **Track:** enable when license-audit + deps land; **Defer:** presenting as validated ZeroGPU until hosted E2E passes |
| Gradio-only hosted surface | `[REPO]` architecture.md | **Implement now:** no separate API server assumption on Spaces |

**Frontier watch:**

- Queue-aware UX when ZeroGPU slots are contended (wait estimates, cancel).
- Warm-model pinning strategies for repeat users (platform-dependent; not implemented).

---

## 4. Mesh export + trust / validation

| Pattern | Evidence | Repo implication |
|---------|----------|------------------|
| Manifest as provenance record (run id, adapter, timestamps, artifact paths) | `[REPO]` exporters.py, verification.md | **Implement now:** manifest always emitted with generation |
| GLB + OBJ dual export for interoperability | `[REPO]` export-guide | **Implement now:** maintain both; GLB for viewers, OBJ for DCC pipelines |
| Capture-quality scoring as pre-flight hint | `[REPO]` capture-guide, evaluation-metrics (frontier) | **Track:** lightweight heuristics (resolution, contrast, subject isolation); **Defer:** ML-based capture scorer |
| Source-runtime parity register for deploy/UI drift | `[REPO]` source-runtime-parity-register.md | **Implement now:** update register when deploy or UI contracts change |
| Four-mode validation honesty (local CPU/GPU, hosted CPU fallback, hosted ZeroGPU) | `[REPO]` mode-validation-matrix | **Implement now:** P10 hosted E2E remains `[OPEN]` until Block/Vase run on live Space |

**Frontier watch:**

- Cryptographic or content-hash manifest signing for reproducibility (not required for MVP).
- Automated mesh sanity checks (watertightness, triangle count bounds) in export pipeline.

---

## Action summary

### Implement now (Tier 1–2)

1. Composer-above-fold layout with regression test.
2. Explicit fallback labeling in UI and manifest.
3. Three-artifact export contract (manifest, GLB, OBJ).
4. Parity register updates when deploy/UI changes.

### Track (Tier 3 — do not treat as shipped)

1. Hunyuan and other license-gated ZeroGPU adapters.
2. Hybrid splat/mesh internal representations.
3. Capture-quality ML scoring.
4. ZeroGPU queue/contention UX.
5. Image-led starter card thumbnails.

### Explicitly deferred

- Hosted HF Space E2E (P10) until CLI deploy + Block/Vase verification.
- Presenting ZeroGPU generation as validated when adapter is disabled or fallback ran.

---

## Caveats

- `[OPEN]` External model latency and ZeroGPU slot behavior not measured for this repository on 2026-05-23.
- `[OPEN]` Competitive landscape evolves quickly; re-benchmark quarterly.
- This doc supersedes no canonical architecture or verification authority — defer to flat canonical docs in [README.md](../README.md).
