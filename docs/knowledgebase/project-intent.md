# Project Intent And Cleanup Patterns

This note summarizes the project's goals and working preferences from the current repository state.

## Source Basis

This synthesis is based on:

- the current repository history;
- `README.md`;
- the existing files in `docs/knowledgebase/`;
- `pyproject.toml`;
- `.vscode/tasks.json` and `.vscode/launch.json`;
- current Gradio documentation for `Model3D`, Blocks workflows, and Spaces integrations;
- current Hugging Face Spaces and ZeroGPU documentation;
- current 2025-2026 research trends around feed-forward reconstruction, Gaussian splatting, mesh extraction, texturing, evaluation, and creator-facing UX patterns.

No repo-local `AGENTS.md`, `copilot-instructions.md`, `*.instructions.md`, `*.agent.md`, or similar customization files were found inside the repository. The current git history also appears to contain a single foundational commit, so the patterns below describe the scaffold's explicit design choices more than a long series of later cleanups.

## What The Project Is Trying To Be

ImageEZGen3D is aiming to be a reliable image-to-3D workspace scaffold before it becomes a heavy model integration project.

The repeated intent across the repo is:

- prefer a ZeroGPU-first Gradio workflow when the environment supports it;
- keep local development viable without CUDA, model weights, or native build friction;
- make CPU fallback explicit instead of magical;
- keep every generation run inspectable through manifests, reports, and retained outputs;
- validate inputs and exported artifacts before claiming success;
- gate heavy adapters behind license, dependency, and runtime checks instead of enabling them early.

In short, the project values dependable workflow and deployment hygiene over chasing model capability too early.

## Patterns The Repository Keeps Cleaning Up Or Preventing

Even with limited git history, the codebase and docs show a consistent cleanup direction.

### 1. Split risky responsibilities instead of mixing them

The architecture separates UI, orchestration, preprocessing, runtime checks, storage, exporters, mesh validation, and adapters. This prevents the common failure mode where one script tries to own GPU imports, file handling, validation, conversion, and interface logic all at once.

This suggests a standing preference for:

- explicit module boundaries;
- adapter isolation;
- CPU-safe code paths outside GPU-only sections.

### 2. Replace hidden behavior with recorded decisions

The docs and config repeatedly insist that runtime selection, adapter choice, and fallback reasons should be visible. Behavior is meant to be explained through manifests and status reporting rather than inferred after the fact.

This shows a cleanup bias toward:

- auditable defaults in `pyproject.toml`;
- manifests that capture what happened and why;
- explicit fallback reasons instead of silent degradation.

### 3. Prefer scaffolding that is testable over realism that is fragile

The CPU demo is intentionally not marketed as real reconstruction. It exists to prove end-to-end workflow, export integrity, persistence, and UI behavior while the high-risk model path stays gated.

That points to a recurring project desire:

- prove the product workflow first;
- defer realism until the system can support it safely;
- keep CI and local development functional without specialized hardware.

### 4. Centralize configuration and keep overrides thin

`pyproject.toml` is treated as the source of truth for package metadata, runtime defaults, exports, preprocessing thresholds, and tool settings. Environment variables exist as local escape hatches, not as the primary design surface.

This reflects a cleanup preference for:

- one auditable config source;
- lightweight wrapper files where tools require them;
- local overrides that are allowed but made visible.

### 5. Document failure classes instead of pretending they do not exist

The knowledgebase already includes failure-mode guidance, capture advice, runtime strategy, deployment notes, and verification steps. The project is not trying to hide known failure classes in image-to-3D generation. It is trying to classify them and give the operator a recovery path.

This implies a standing expectation that future work should:

- preserve actionable error messages;
- keep recovery steps concrete;
- avoid ambiguous success states.

### 6. Make verification part of the definition of done

The verification guide is strict: tests, compile checks, style checks, manual UI checks, and ZeroGPU-specific constraints all sit behind completion claims.

This indicates a cleanup pattern of:

- tightening completion criteria;
- requiring evidence for runtime behavior;
- treating verification as product behavior, not just engineering ceremony.

### 7. Protect the repo from legal and operational debt

The license audit and model matrix are unusually prominent for a small scaffold. Heavy adapters are intentionally blocked until source provenance, weight terms, dependency distribution, and token handling are understood.

That suggests the project wants to clean up or avoid:

- unclear redistribution rights;
- implicit commercial-use assumptions;
- hard coupling to gated or CUDA-only dependencies;
- secrets stored in source.

## Project Goals That Seem Stable

The following goals appear repeatedly enough to treat as durable project intent:

1. Deliver a one-page Gradio workflow for image intake, generation, preview, and export.
2. Keep the default path usable on ordinary local machines.
3. Prefer ZeroGPU automatically when it is truly available and configured.
4. Preserve a deterministic CPU fallback path for tests, demos, and offline development.
5. Retain per-run artifacts, reports, and manifests so behavior can be inspected later.
6. Support standard mesh exports and verify their integrity.
7. Add heavy adapters incrementally and only after legal and runtime gates are satisfied.
8. Keep editor workflows first-class through tasks, debug configs, and `.env`-based local setup.

## Non-Goals Or Explicitly Deferred Work

The repository also makes several boundaries clear.

- The CPU demo is not intended to be mistaken for production-quality reconstruction.
- Hunyuan, TRELLIS, and Pixal-style integrations are reference directions, not enabled features.
- ZeroGPU support is not a license to move CPU-safe work into GPU-only sections.
- Deployment convenience must not come at the cost of storing tokens or vendoring questionable assets.
- The project is not trying to solve retopology, production asset cleanup, or model research depth in the current phase.

## Practical Guidance For Future Changes

If a change fits the existing project intent, it will usually do most of the following:

- keep adapter boundaries explicit;
- improve manifests, reports, or operator visibility;
- preserve local CPU viability;
- make fallback behavior more understandable rather than more automatic;
- add verification coverage alongside new capability;
- avoid introducing license, secret, or CUDA coupling prematurely.

If a proposed change works against the current direction, it will usually do one of these things:

- mix UI, runtime, and model code into one place;
- hide fallback or runtime decisions from the user;
- make local development depend on GPU-only components;
- bypass documented verification gates;
- enable heavyweight adapters before audit and runtime readiness are complete.

## Research Extension

The knowledgebase now also carries a broader external-research layer so product decisions are not driven only by the scaffold itself.

Recommended companion docs:

- `docs/knowledgebase/3d-reconstruction-theory.md`
- `docs/knowledgebase/evaluation-metrics.md`
- `docs/knowledgebase/creator-product-patterns.md`
- `docs/knowledgebase/competitive-product-benchmark-2026.md`
- `docs/knowledgebase/prompt-behavior-investigations-2026.md`
- `docs/knowledgebase/frontend-implementation-patterns-2026.md`
- `docs/knowledgebase/frontend-ux-blueprint.md`
- `docs/knowledgebase/knowledgebase-authoring-playbook.md`
- `docs/knowledgebase/auth-gated-ux-patterns.md`
- `docs/knowledgebase/knowledgebase-builder-agent-spec.md`

Operational companion docs:

- `docs/knowledgebase/configuration.md`
- `docs/knowledgebase/zerogpu-runtime.md`
- `docs/knowledgebase/deployment-hf-cli.md`
- `docs/knowledgebase/failure-modes.md`
- `docs/knowledgebase/verification.md`
- `docs/knowledgebase/license-audit.md`
- `docs/knowledgebase/vscode-workflow.md`

The stable conclusions from that research are:

- no single 3D representation wins across capture, editing, preview, and export;
- hybrid pipelines are now the norm, but mesh-first remains the safest user-facing canonical artifact for this repo;
- single-image generation is best framed as draft ideation, while coherent multi-view evidence is the quality path;
- user trust depends on showing preprocessing, fallback decisions, confidence limits, and recoverable next steps;
- shared-runtime deployments such as ZeroGPU reward staged pipelines, short GPU sections, and explicit CPU-side orchestration;
- the strongest 2026 consumer app patterns combine fast entry, progressive disclosure, same-surface iteration, example-driven prompting, visible history, and explicit post-generation editing paths;
- deeper per-page prompt-behavior investigations reinforce that the best creator tools also provide artifact-local follow-up actions, remembered draft state, `Auto` or recommended defaults, and explicit cost or refund messaging when generation is scarce;
- live frontend implementation probes reinforce that shell continuity only works when the primary composer stays visible, semantic controls are real buttons or listboxes rather than div lookalikes, and large option pickers are grouped by provenance with concise names;
- configuration, deployment, failure handling, verification, and editor workflow are first-class product-quality surfaces in this scaffold, not merely maintainer notes;
- if authentication is ever added, the product should prefer post-value or soft gating over a hard login wall unless security or privacy requirements truly demand otherwise.

## History Caveat

This repository currently exposes very little historical drift in git. If more branches or older commits are imported later, this document should be updated with concrete cleanup trends from those changes. For now, the strongest evidence comes from the scaffold's architecture, docs, operational guardrails, and the current external research layer summarized in the companion knowledgebase notes.
