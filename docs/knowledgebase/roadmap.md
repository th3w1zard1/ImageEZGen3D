# Roadmap

This roadmap is intended to describe durable execution direction, not just what happened in one session.

## Current Status Snapshot

The repo now has a meaningful scaffold in place:

- CPU-safe workflow proof exists;
- pyproject-backed configuration is live;
- per-run manifests and artifact storage are in place;
- the knowledgebase is now broad enough to guide product, runtime, and architecture decisions;
- ZeroGPU intent is explicit, but real heavy-adapter enablement is still gated.

The main unresolved frontier is not documentation anymore. It is turning the scaffold into a trustworthy higher-quality generation system without breaking the repo's legal, runtime, or local-development contract.

## Execution Tracks

### Track 1: Product Workflow Maturity

Goal:

- make the one-page workflow easier to trust, easier to recover, and easier to iterate on.

Near-term priorities:

- keep normalized preview, runtime status, exports, and manifests tightly linked;
- make draft-versus-quality framing explicit at intake time;
- improve same-surface history, rerun, and compare behavior;
- keep recovery suggestions specific instead of generic.

### Track 2: Runtime And Deployment Readiness

Goal:

- preserve the repo's CPU-safe local path while making hosted behavior more explicit and verifiable.

Near-term priorities:

- verify ZeroGPU behavior on a real target Space;
- keep CPU-safe work outside GPU-decorated sections;
- make hosted runtime limits and fallback reasons visible;
- prevent source-versus-runtime drift across config, requirements, docs, and deployed behavior.

### Track 3: Adapter Admission

Goal:

- move from placeholder references to audited, real model integrations one adapter at a time.

Near-term priorities:

- complete license and dependency review for the next candidate adapter;
- ensure installation and host compatibility are reproducible enough for the intended path;
- preserve manifests, failure handling, and export validation across both CPU and GPU routes.

### Track 4: Creator-Workflow Depth

Goal:

- evolve from "single run succeeds" toward a creator-friendly iteration workspace.

Near-term priorities:

- labeled multi-view intake;
- better compare and organization surfaces;
- starter examples, style references, or prompt assists where they genuinely help;
- richer export options without losing the mesh-first default.

## Phased Product And UX Direction

### Phase 1: Trust-First Frontend

- show normalized input before generation;
- expose draft versus quality as the primary choice;
- keep preview, downloads, and run status on one page;
- preserve prior runs and manifests without destructive replacement.

Exit signal:

- a first-time user can complete a run and understand what happened without reading code.

### Phase 2: Staged Generation UX

- separate shape generation from texturing or refinement;
- make runtime choice and fallback reason visible;
- provide actionable retry guidance based on validation and failure class.

Exit signal:

- the app can explain degraded but usable outcomes instead of collapsing them into generic success or failure.

### Phase 3: Compare And Organize

- add run history and compare views;
- support rerun from prior settings;
- expose lightweight boards, moodboards, favorites, or reference organization for iterative creation.

Exit signal:

- users can meaningfully iterate without losing context between runs.

### Phase 4: Heavy Adapter Integration

- add audited adapters one at a time;
- keep CPU-safe orchestration outside GPU sections;
- preserve identical trust signals across CPU and GPU paths.

Exit signal:

- a real higher-quality adapter is enabled without breaking local development or the repo's audit posture.

### Phase 5: Advanced Creator Workflow

- multi-view labeled intake;
- optional prompt and style references;
- richer export validation and decimation choices;
- future splat or radiance complements without displacing mesh-first output.

Exit signal:

- the app supports both quick draft ideation and stronger evidence-driven reconstruction paths.

## What Is Intentionally Not Immediate

- production retopology and full DCC cleanup workflows;
- broad multi-model enablement without audit discipline;
- representation novelty that displaces mesh-first export utility;
- auth-heavy product layers before there is a clear need for save, sync, collaboration, or quota control.

## Roadmap Risks

- enabling a heavy adapter too early could collapse the local development story;
- hosted-runtime optimism could create a product that only works on paper;
- richer UX surfaces could become cluttered if staged disclosure is not preserved;
- benchmark envy could push the repo toward identity-copying instead of pattern borrowing.

## Self-Critique

The project now has a strong foundation and a real knowledge layer, but the high-quality model path remains intentionally gated. That is still the right tradeoff until licensing, native wheels, VRAM footprint, and actual ZeroGPU behavior are verified on a live host.
