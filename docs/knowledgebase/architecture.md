# Architecture Decisions

ImageEZGen3D starts from a CPU-safe, inspection-friendly foundation with explicit adapter boundaries. That architecture is aimed at avoiding the most common image-to-3D failure pattern: one script that mixes GPU imports, native-wheel assumptions, UI code, file conversion, runtime selection, and persistence into a fragile monolith.

## Source Basis

This note is based on:

- `app.py`;
- `src/imageezgen3d/config.py`;
- `src/imageezgen3d/orchestrator.py`;
- `src/imageezgen3d/runtime.py`;
- `src/imageezgen3d/storage.py`;
- `src/imageezgen3d/preprocess.py`;
- the adapter, exporter, and mesh-check modules;
- the current knowledgebase research layer.

## Core Architectural Priorities

The current architecture prefers:

- explicit module boundaries over convenience coupling;
- CPU-safe orchestration outside GPU-only sections;
- inspectable manifests and run folders over hidden transient state;
- graceful fallback behavior over optimistic runtime assumptions;
- product workflow proof before heavyweight model ambition.

## Borrowed Patterns

- Hunyuan3D-2.1: staged shape-versus-texture thinking, image preprocessing, mesh cleanup, and Gradio or ZeroGPU awareness;
- TRELLIS.2: richer asset thinking, inline 3D preview, render-mode sensitivity, and export-minded workflows;
- Pixal-style systems: health and runtime-state mindset, progress reporting, and deployment-lifecycle awareness;
- consumer image apps in 2026: prompt-first entry, visible examples, same-surface iteration, history, projects, route separation, and explicit edit-after-generate flows.

The repo borrows these as architectural and product patterns, not as a mandate to absorb their full dependency or UI identity.

## Current Module Shape

- `app.py`: the Gradio Blocks composition layer and UI entry point;
- `config.py`: typed config loader that resolves defaults, TOML values, `.env`, and environment overrides;
- `runtime.py`: runtime detection and ZeroGPU eligibility logic;
- `orchestrator.py`: run lifecycle, adapter selection, manifest updates, and end-to-end request flow;
- `preprocess.py`: input normalization, validation, resizing, and reporting;
- `storage.py`: run IDs, per-run directories, atomic writes, manifest persistence, and retention cleanup;
- `adapters/`: pluggable generation backends, with CPU demo live and heavy adapters still gated;
- `exporters.py`: pure-Python draft OBJ, PLY, STL, and GLB export path;
- `mesh_checks.py`: artifact integrity inspection for exported outputs.

## Control-Flow Shape

The current high-level flow is intentionally staged:

1. load configuration;
2. determine runtime availability and adapter choice;
3. create a run folder and seed a manifest;
4. preprocess and validate inputs;
5. persist source and normalized inputs;
6. generate through the selected adapter;
7. inspect artifacts and update mesh-report fields;
8. persist final manifest state and return a structured payload.

This makes generation a recordable workflow rather than a single opaque callback.

## Why The Orchestrator Exists

The orchestrator is the architecture's main anti-chaos boundary.

Its job is to keep these concerns coordinated without collapsing them together:

- adapter selection;
- runtime truth;
- manifest updates;
- preprocessing output;
- artifact recording;
- success versus failure state handling.

That separation matters because the app is expected to grow from a CPU demo into a mixed CPU and GPU system without losing inspectability.

## Storage And Manifest Architecture

Run storage is a first-class architectural choice, not a logging afterthought.

Key properties:

- each run gets its own folder;
- inputs, processed files, meshes, exports, and reports are separated by category;
- manifest writes are atomic;
- artifacts are recorded explicitly;
- retention cleanup is centralized.

This gives the project a durable recovery and audit surface even before it has a sophisticated model backend.

## Runtime Architecture

Runtime selection is intentionally centralized instead of being scattered across UI and adapter code.

The current contract is:

- explicit adapter selection wins;
- `auto` attempts the preferred hosted path when truly usable;
- CPU fallback is a policy decision, not a silent accident;
- the reason for the runtime decision should be visible to the operator.

That is the correct shape for a repo that wants ZeroGPU support without pretending every environment is a GPU host.

## Frontend Architecture Direction

The future UI should stay modular in the same way as the backend.

Recommended surfaces:

- intake surface: upload, labeled views, optional text instruction, and example starters;
- validation surface: normalized preview, capture warnings, and recovery guidance;
- generation surface: draft-versus-quality mode, runtime status, adapter choice, and progress;
- result surface: inline 3D preview, evidence previews, export actions, and manifest access;
- history surface: prior runs, manifests, compare mode, and rerun-from-settings.

This keeps stateful UX concerns legible instead of burying them in one monolithic callback chain.

## Frontend State Model

The cleanest user-facing state model remains:

1. idle;
2. validating;
3. ready;
4. generating shape;
5. shape ready;
6. generating texture or refinement;
7. complete;
8. degraded but usable;
9. recoverable failure.

The UI should always make the current state, the next action, and the fallback reason visible.

## Architectural Non-Goals For Now

- no hidden background orchestration that bypasses manifests;
- no GPU-only architecture that makes local development second-class;
- no forced dependence on gated model artifacts just to exercise the workflow;
- no premature collapse of mesh-first delivery into representation experimentation.

## Self-Critique

The CPU demo mesh is not a real image-to-3D model. It is a testable scaffold that proves UI, persistence, export, and verification behavior before heavier adapters are added.

That limitation is acceptable because the architecture is currently optimized for trustworthy product scaffolding, not benchmark-chasing model depth.
