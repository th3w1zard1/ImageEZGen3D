# Frontend UX Blueprint

This note translates the research docs and competitive benchmark into a concrete frontend blueprint for ImageEZGen3D.

The goal is not to imitate any single app. The goal is to build a top-tier, low-friction, trustworthy image-to-3D workflow that fits this repository's architecture and runtime constraints.

## Core UX Objective

The app should minimize three user costs:

- time to first trust signal;
- time to first usable mesh;
- time to iterate from a weak result to a better result.

Useful internal mental models:

- `T_trust = T_upload + T_validation_visible + T_status_visible`
- `T_iterate = T_change + T_regenerate + T_compare`

The product should reduce these values even when absolute generation time cannot be made small.

## Human Factors That Matter

### Visibility Of System Status

Users should always know:

- what the app is doing now;
- what evidence it used;
- which runtime was selected;
- whether the result is draft-grade or quality-grade;
- what to do next.

The live browser probe adds one more requirement:

- where the primary composer actually is.

If upload or prompt entry is pushed below the fold by shell chrome, the app is paying a trust tax before the user even starts.

### Progressive Disclosure

Do not expose every knob before the first successful run.

Practical rule:

- first run: only the decisions that materially change outcome quality or trust;
- later refinement: expose seed, decimation, texture resolution, adapter choice, and deeper runtime controls.

### Recognition Over Recall

Users should not have to remember:

- capture rules;
- example prompts;
- which prior settings worked;
- why a previous run failed.

Show these things near the current task.

### Non-Destructive Iteration

Every run should behave like a revision, not a replacement.

History, compare, rerun-from-settings, and preserved manifests are product features, not internal implementation details.

The deeper prompt-behavior benchmark suggests a stronger rule:

- successful artifacts should expose nearby branch actions instead of forcing blank-state restart.

For this repo that means actions such as:

- image to draft mesh;
- retry with stronger structure;
- keep current shape and refine texture;
- open export-safe preview;
- compare against previous run.

### Workspace Continuity

Modern creative tools increasingly keep the creator inside a persistent workspace shell.

Useful surrounding surfaces include:

- recent runs;
- pinned or favorite runs;
- projects or collections;
- templates or starter flows;
- compare views and rerun actions.
- remembered draft state for unsent text or previously selected evidence.

### Locality Of Reference

Inputs, validation, progress, preview, exports, and next actions should remain visually close together.

The strongest benchmark signal across modern tools is that users lose confidence when the main result appears far away from the main control surface.

The implementation probe reinforces a related rule:

- the primary input lane should remain above the fold on first load for common desktop widths.

## Recommended Information Architecture

### Primary Page Regions

1. Intake panel
2. Validation and capture guidance panel
3. Generation controls panel
4. Preview and export panel
5. Run history and compare drawer

### Intake Panel

Should include:

- primary image upload;
- optional labeled view uploads: front, back, left, right, detail;
- optional text instruction for style or cleanup intent;
- example chips such as "single product photo", "multi-view turntable", and "draft from one image".
- a clearly recommended default path for unsure users, such as `Recommended` or `Auto`, with the chosen path explained after the run.

If prompting support grows later, example chips should include transformation, diagram, cleanup, and stylization ideas rather than only generic art prompts.

### Validation Panel

Should show before generation:

- normalized preview;
- background/crop/blur warnings;
- confidence or risk badge;
- best next step guidance.

If the app later has hosted quotas, this is also a good place to surface likely runtime cost before generation.

### Generation Controls Panel

Simple controls first:

- mode: draft or quality;
- route choice: recommended or manual;
- output target: GLB default;
- optional quality preset.

Advanced controls behind disclosure:

- seed;
- texture size;
- decimation;
- adapter selection;
- runtime preference;
- future style/reference controls.

If `recommended` or `auto` mode is offered, the UI should later record:

- which path it chose;
- which runtime it used;
- why that choice was made.

If multiple runtime or model options are exposed manually, they should:

- be grouped by provenance or trust category when relevant;
- use short option names;
- avoid burying critical differences in repetitive marketing-style labels.

### Preview And Export Panel

Should include:

- inline `Model3D` preview;
- 2D thumbnails for input and normalized evidence;
- clear indicator for shape-only versus textured output;
- export buttons for available formats;
- manifest and validation report access.

Suggested next-step chips should appear nearby when they are credible, for example:

- add a back view;
- retry as draft;
- preserve shape and skip texture;
- compare against previous run.
- branch into a turntable preview;
- refine texture only.

### History And Compare Drawer

Should support:

- rerun from prior settings;
- compare two runs side-by-side;
- favorite or pin a run;
- inspect runtime, settings, and fallback reason.

## Recommended State Machine

The UI should explicitly model:

1. idle
2. validating
3. ready
4. generating shape
5. shape ready
6. generating texture or refinement
7. complete
8. degraded but usable
9. recoverable failure

Each state should define:

- visible status text;
- allowed actions;
- disabled actions;
- primary next step.

## Generation Flow

### Draft Path

Best for:

- single image;
- low-friction concept generation;
- CPU-safe fallback;
- rapid iteration.

UI expectations:

- fast path button;
- explicit warning that hidden sides are inferred;
- immediate preview and exports when complete.
- visible starter examples that help the user succeed without learning the entire system first.

### Quality Path

Best for:

- coherent multi-view evidence;
- higher quality geometry;
- future texture stages;
- more serious export intent.

UI expectations:

- asks for more evidence up front;
- explains why it may take longer;
- separates shape and texture/refinement phases if needed.
- makes the stronger evidence requirement explicit before consuming heavier runtime.

## Authentication Strategy If Added Later

ImageEZGen3D does not currently need authentication for its local or simple hosted form, but if auth is added later for saved projects, collaboration, or remote quotas, the preferred strategy is:

1. allow users to see examples, capture guidance, and product value before sign-in;
2. keep basic local or guest experimentation available where practical;
3. require auth for save, share, project history sync, collaboration, or high-cost remote generation;
4. avoid a hard login wall unless security, privacy, or billing constraints truly require it.

If a gated surface becomes necessary, label it honestly as a sign-in requirement for a specific benefit, not as a vague blocker.

## Prompting And Reference Strategy

ImageEZGen3D is evidence-first, but prompt support is still valuable.

Recommended use of text:

- clarify object identity;
- request stylistic texture direction later;
- ask for cleanup emphasis such as "preserve thin handle" or "avoid heavy smoothing".

Recommended reference support:

- optional style references;
- optional material references;
- labeled multi-view evidence kept distinct from style references.

Do not mix evidence images and style references without telling the user which role each image is playing.

## Preview Strategy

The main result must stay on the same surface.

Recommended preview stack:

- preprocessed 2D evidence preview;
- inline 3D model preview;
- quick metadata summary;
- export actions adjacent to the preview;
- compare toggle for prior runs.

If later representations are added, prefer:

- mesh as the default preview target;
- optional splat or radiance view as a secondary inspection mode.

## Error And Recovery UX

Every failure should map to a next action.

Preferred recovery messages:

- add a back view;
- retake with softer light;
- remove background clutter;
- retry as draft mode;
- rerun texture stage only;
- export shape-only mesh if texturing is weak.

If generation consumes credits or scarce hosted runtime later, also report:

- whether credits or quota were spent;
- whether they were returned after failure;
- whether a cheaper retry path exists.

The recent CapCut-style benchmark pattern is worth copying here:

- show preflight cost before action;
- show refund or return state after failure when applicable;
- keep retry or branch actions attached to the affected artifact.

Avoid messages that tell the user only that something failed.

## Accessibility And Responsiveness

Must-have behaviors:

- keyboard-accessible upload, settings, generate, compare, and export flows;
- readable status and error text;
- mobile or narrow-layout survival without hiding the core workflow;
- same-page preview behavior on desktop and mobile.

Implementation rules from the live probe and W3C guidance:

- use real buttons for mode chips and action triggers rather than div-based lookalikes;
- use menu-button semantics for expandable mode pickers;
- use named grouped option lists when exposing long model or runtime menus;
- do not rely on placeholder text alone to explain the purpose of the main prompt or instruction field.

## Product Metrics Worth Tracking

Future instrumentation should track:

- upload-to-validation-visible time;
- upload-to-first-preview time;
- first-run completion rate;
- retry rate after actionable guidance;
- export success rate;
- compare/history usage;
- frequency of CPU fallback and whether users understand it.

## Repo Implications

This blueprint implies future implementation work in:

- Gradio layout and state management;
- richer manifest schema;
- run history indexing;
- compare and rerun affordances;
- more explicit validation reporting;
- staged orchestration status events.

## Near-Term Recommendations

The most valuable near-term UI improvements for this repo are:

1. visible normalized-input preview before generation;
2. explicit draft-versus-quality mode selector;
3. runtime and fallback status displayed near progress;
4. same-page history and compare affordance;
5. example capture sets and recovery guidance near upload;
6. artifact-local next-action chips after a run completes;
7. a `recommended` path that explains its runtime and evidence choices after generation.

Those changes would move the product materially closer to the best current consumer patterns without violating the repo's CPU-safe and verification-first architecture.
