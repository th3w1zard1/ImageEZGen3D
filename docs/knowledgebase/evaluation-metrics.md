# Evaluation And Metrics

There is no single metric that tells the truth about a 3D asset.

For creator-facing image-to-3D tools, evaluation has to be layered. A model can score well on rendered images and still produce a mesh that is unusable for export, editing, or printing.

## Evaluation Stack

### 1. Geometry Fidelity

Useful metric families:

- Chamfer Distance:
  `CD(A, B) = mean_a min_b ||a - b||^2 + mean_b min_a ||b - a||^2`
- F-score at a distance threshold.
- IoU or occupancy overlap where voxelized or signed-volume references exist.
- surface accuracy and completeness when ground-truth scans exist.
- normal consistency for local surface orientation quality.

What they catch well:

- wrong silhouette;
- missing or extra surface regions;
- over-smoothed geometry;
- thin-part collapse.

What they miss:

- editability;
- UV quality;
- material usefulness;
- user trust.

### 2. Rendered Appearance Fidelity

Common image-space metrics:

- PSNR:
  `PSNR = 10 log10(MAX^2 / MSE)`
- SSIM for structural similarity.
- LPIPS for perceptual similarity.

What they are good for:

- view synthesis quality;
- coarse regression tracking during training;
- comparing render fidelity across models.

What they are bad at:

- judging whether geometry is actually usable;
- detecting semantically wrong backsides or materials;
- detecting creator-tool failure states such as bad topology.

### 3. Semantic And Prompt Alignment

Useful metric families:

- CLIP-style similarity for image-text or image-image alignment;
- ULIP or Uni3D-style cross-modal metrics when 3D-language alignment matters;
- task-specific semantic correctness checks.

These help answer whether the output still looks like the requested object, not whether it is a good asset.

### 4. Multi-View Consistency

This is under-measured and extremely important.

Failure modes often missed by standard metrics:

- different shapes implied from different views;
- backside hallucination;
- inconsistent texturing across angles;
- seams or view-dependent artifacts;
- Janus-style multi-face ambiguity.

For this repo, manual multi-view inspection is still mandatory.

### 5. Asset Utility

For creator tools, the export itself needs evaluation.

Questions that matter:

- Does the mesh parse?
- Is the geometry non-empty and structurally sane?
- Are textures and references present when promised?
- Is payload size acceptable for web preview?
- Does the previewed model match the downloaded asset?
- Can the user understand what backend, settings, and fallback path produced it?

### 6. Human Judgment

Human review remains essential because users care about:

- whether the object looks believable from the views they care about;
- whether the result is editable or merely pretty;
- whether the app communicated limitations honestly;
- whether the failure is recoverable with more input.

## Failure Taxonomy

Common recurrent failures:

- wrong or invented backside;
- floaters and detached fragments;
- holes and self-intersections;
- over-smoothed or melted geometry;
- thin-part collapse;
- stretched or inconsistent textures;
- baked lighting and shadow contamination;
- glossy or transparent material breakdown;
- payloads too large for browser delivery;
- fallback behavior hidden from the user.

Each failure should be tagged by recovery path:

- retake input;
- add more views;
- rerun texture stage only;
- simplify or decimate;
- manual cleanup required;
- fundamental unsupported case.

## Product-Side Definition Of Done

For ImageEZGen3D, a run is only truly complete when all of these layers are acceptable:

1. automated tests and compile/style checks pass;
2. input validation warnings are generated when appropriate;
3. the selected runtime and fallback reason are recorded;
4. exported files exist and are structurally sane;
5. inline preview and download paths work;
6. the result is framed honestly as draft or quality, depending on evidence.

## Minimal Evaluation Matrix For This Repo

| Layer | Minimum Evidence |
| --- | --- |
| Runtime | Adapter chosen, runtime status, fallback reason in manifest |
| Input quality | Validation report for blur, crop, alpha/background, and risk flags |
| Export integrity | Mesh exists, non-empty payload, parse or health check passes |
| UX correctness | Preview updates inline, no confusing tab hopping, prior runs preserved |
| User trust | Errors and limitations are explicit and actionable |

## Frontier Topics To Track

Emerging evaluation themes worth watching:

- explicit uncertainty estimation for novel views;
- active view selection based on reconstruction uncertainty;
- perceptual quality datasets for Gaussian splatting;
- metrics for text readability, relightability, and semantic consistency;
- compression-aware quality metrics for browser or mobile delivery.

These should inform future docs and tests, but they should not displace the current layered evaluation approach.
