# Model Matrix

This matrix is meant to guide staged adapter adoption, not to rank impressive model demos in the abstract.

## How To Read This Matrix

The key question for this repo is not "which model is coolest?"

It is:

- which backend preserves local development viability;
- which backend can be integrated without hiding runtime truth;
- which backend supports mesh-first user outcomes;
- which backend can survive legal, dependency, and hosted-runtime review.

## Current Matrix

| Backend Or Family | Primary Role | Best Current Value | Main Risk | Fit For This Repo Right Now | Current Status |
| --- | --- | --- | --- | --- | --- |
| CPU demo | Local and CI scaffold | No CUDA, no weights, deterministic export path, easy validation | Not real reconstruction quality | Excellent for workflow proof and regression coverage | Implemented |
| Hunyuan3D-2.1 | Future hosted shape-plus-texture path | Strong modular pipeline ideas, multi-view direction, potential ZeroGPU-facing relevance | License restrictions, gated assets, VRAM pressure, texture-stage complexity | Promising but still blocked on audit and runtime readiness | Placeholder until audit |
| TRELLIS.2 | High-end structured asset research | Strong ideas around richer asset outputs and PBR-oriented thinking | CUDA-only custom wheels, heavy setup, no current CPU-safe fallback | Good research signal, poor current scaffold fit | Research reference |
| Pixal-style cascade stacks | Product and runtime architecture reference | Good inspiration for staged progress, health reporting, camera estimation, and pipeline orchestration | Large dependency surface, CUDA coupling, operational heaviness | Better as product-pattern reference than near-term default adapter | Research reference |
| Gaussian splat and radiance-field families | Representation and preview research | Excellent view-synthesis fidelity, fast preview, strong hybrid-scene research | Weak as the primary editable canonical asset, viewer and portability constraints remain | Valuable complement, not primary export path | Research reference |

## What The Matrix Currently Says

The repo should implement reliable workflow first, then add audited model adapters one at a time.

The strongest current conclusions remain:

- mesh-first outputs are still the safest canonical artifact for this repo;
- Gaussian splats and radiance-style outputs are useful complements, not replacements, for a creator-facing scaffold centered on export utility;
- single-image generation should be framed as draft ideation;
- coherent multi-view input remains the quality path;
- shape-first, texture-second pipelines are still the most pragmatic user-facing architecture.

## Why CPU Demo Still Matters

The CPU demo is not a compromise to be apologized for.

It is what currently proves:

- the app can ingest images;
- preprocessing and validation work;
- manifests and run folders are coherent;
- exports are valid;
- the UI can preview and download assets;
- CI and local development remain alive without special hardware.

Without that path, the repo would risk becoming a model-integration shell that cannot reliably demonstrate its own workflow.

## Why Hunyuan Is Still Only A Placeholder

Hunyuan remains the most plausible future hosted direction in this scaffold, but it is not ready to be treated as an enabled default because:

- the legal review is not finished;
- hosted runtime costs and fit still matter;
- the configured adapter is still a placeholder rather than a completed integration;
- the repo's trust model requires explicit fallback and operational honesty.

## What Counts As Admission For The Next Adapter

A future adapter should only graduate from research reference to enabled implementation when all of these are true:

1. license and redistribution terms are written down;
2. dependency installation is reproducible enough for the intended host and audience;
3. CPU-safe code paths outside GPU work remain intact;
4. runtime selection and fallback reasons remain explicit in manifests and UI;
5. exports remain coherent with the mesh-first product contract;
6. verification and failure-mode docs have been updated for the new path.

## Frontier Guidance

The matrix should continue tracking frontier representations and creator-tool workflows, but frontier tracking should not automatically change the default product contract.

Use the frontier layer to influence:

- future preview ideas;
- hybrid representation support;
- editing and relighting directions;
- viewer strategy.

Do not use it to silently replace the repo's current export and verification priorities.
