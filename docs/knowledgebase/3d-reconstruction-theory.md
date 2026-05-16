# 3D Reconstruction Theory

This note is a working synthesis of durable 3D reconstruction ideas and 2025-2026 research directions. It is not a full survey of every paper, but it is meant to capture the theory and methodology that actually matters for product decisions.

## Core Principle

There is no universally best 3D representation.

Every practical system is trading among:

- capture fidelity;
- editability;
- rendering speed;
- export interoperability;
- memory and bandwidth;
- training or inference cost.

Recent strong systems are increasingly hybrid. They use one representation for reconstruction, another for rendering, and another for export.

## Representation Landscape

| Representation | Best At | Weak At | Repo Implication |
| --- | --- | --- | --- |
| Mesh | Editing, UVs, rigging, engines, printing | Harder to infer cleanly from sparse evidence | Keep as the canonical artifact |
| Point cloud | Fast capture and geometry hints | Weak topology and material semantics | Useful as an intermediate, not the final user asset |
| Dense voxels | Structured occupancy and geometry priors | Memory blow-up at high resolution | Better as an internal latent or scaffold |
| Sparse voxels | Efficient structured geometry priors | Still need conversion for creator workflows | Useful for feed-forward or hybrid models |
| SDF / occupancy fields | Clean surfaces and explicit geometry reasoning | Need surface extraction and careful optimization | Strong geometry prior for mesh recovery |
| NeRF | Photoreal novel-view synthesis | Poor direct editability and heavy optimization | Good reference class, not the default user artifact |
| Gaussian splats | Real-time view synthesis and explicit rendering | Weak as a final editable creator asset | Great for preview and scene capture, secondary to mesh export |
| Triplanes / latent planes | Efficient feed-forward inference | Mostly hidden internal representation | Useful design clue, not a user-facing output |
| Hybrid mesh plus splat | Balances editability and fidelity | More complex pipeline and storage rules | The most pragmatic future direction |

## Useful Mathematical Intuition

Some recurring mathematical objects appear across the field.

Signed distance fields define a surface as the zero level set:

`f(x) = 0`

The local surface normal can be recovered from the gradient:

`n(x) = ∇f(x) / ||∇f(x)||`

Volumetric and splatting renderers both accumulate color along a ray using transmittance-weighted contributions:

`C(r) ≈ Σ_i T_i α_i c_i`

where `T_i` is the transmittance up to sample or primitive `i`, `α_i` is opacity, and `c_i` is the color or radiance contribution.

This is one reason the same system can look visually convincing while still having poor extractable geometry: image-space agreement does not guarantee surface correctness.

## Input Regimes

### Single Image

Single-image 3D should be treated as ambiguity-managed generation.

- It is best for ideation and draft assets.
- The hidden side of the object is inferred from priors, not recovered from evidence.
- UX and documentation should say this clearly.

### Sparse Multi-View

Sparse multi-view is the practical quality mode for creator tools.

- Coherent front, side, back, and detail views greatly reduce backside hallucination.
- Strong overlap and stable lighting matter more than raw image count.
- Current research increasingly uses feed-forward reconstruction plus multi-view consistency priors here.

### Dense Multi-View Or Turntable Capture

This remains the best object-centric path when the goal is faithful geometry and clean texture.

- It supports better correspondence, better hole reduction, and more stable texture baking.
- It still struggles on reflective, transparent, and textureless objects.

### Video

Video is useful, but it is not automatically better.

- It is convenient for frame mining and future active view selection.
- Motion blur, rolling shutter, compression, and duplicated viewpoints hurt reconstruction.
- For high-quality assets, selected sharp frames generally beat dumping every frame into the model.

## Canonical Pipeline Shape

The most durable creator-facing pipeline is staged.

1. Preprocess and validate the input.
2. Estimate draft geometry.
3. Refine or re-run with more evidence if geometry confidence is low.
4. Generate texture and material maps as a separate stage.
5. Export and validate the asset.

This shape-first, texture-second separation is one of the most stable patterns in current systems.

## Geometry Methodology

The main geometry lessons are stable across papers.

- Good silhouette coverage matters disproportionately.
- Multi-view agreement is stronger than single-view realism.
- Thin structures, cavities, undersides, and self-occlusions are persistent weak points.
- Better systems spend representation budget where geometry is hard instead of uniformly everywhere.
- Monocular depth, normals, or segmentation priors help, but they do not remove the need for consistent views.

Current frontier trends include:

- feed-forward reconstruction instead of per-scene optimization only;
- pose-free or calibration-light pipelines;
- geometry-aware densification and pruning;
- hybrid Gaussian plus mesh or Gaussian plus SDF stacks;
- active or uncertainty-guided view selection.

## Texture, Materials, And PBR

High-quality texturing is not just "paint the mesh from one view".

Better current pipelines:

- generate or collect multiple coherent views;
- condition texture synthesis on geometry cues such as normals, position maps, or canonical coordinates;
- bake across views;
- fill texture holes in a second pass;
- preserve or recover lighting-invariant material information when possible.

Important material lessons:

- baked shadows look good in screenshots and bad in downstream rendering;
- delighting matters if relighting or PBR is a goal;
- clearcoat, transmission, anisotropy, sheen, specular, IOR, and similar advanced material features should not be exposed unless the backend can infer them credibly.

## What Gaussian Splatting Changes

Gaussian splatting is one of the most important current families because it offers a rare combination of explicit scene structure and real-time rendering.

Its strengths:

- fast rendering;
- strong preview fidelity;
- explicit primitives rather than opaque full-scene MLPs;
- natural fit for scene capture, splat viewing, and hybrid pipelines.

Its limits:

- poor direct compatibility with standard DCC and engine authoring workflows;
- weak topology guarantees;
- floaters, aliasing, and overfitting under sparse evidence;
- compression and browser delivery remain active research areas.

The durable product takeaway is mesh-first, splat-optional.

## Current 2025-2026 Frontiers

The fastest-moving areas now include:

- feed-forward 3D reconstruction and view synthesis;
- compact or controllable Gaussian representations;
- hybrid Gaussian plus mesh pipelines;
- text- or image-driven multi-view consistent editing;
- relightable and inverse-rendered materials;
- 4D dynamic reconstruction and compression;
- semantic and language-aware 3D representations;
- streaming, mobile, and WebGPU-native delivery.

These are important to watch, but they do not change the repo's near-term priorities.

## What Matters For This Repo

The research-backed direction for ImageEZGen3D is:

- keep mesh-first GLB export as the canonical artifact;
- use single-image generation as the draft path;
- treat multi-view as the quality path;
- separate shape generation from texture and material generation;
- keep splat or radiance-style output optional and complementary;
- optimize for explicit recoverability, not just one-pass visual impressiveness.
