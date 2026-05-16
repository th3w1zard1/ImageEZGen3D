# Creator Product Patterns

This note translates current 3D reconstruction research and Gradio/Spaces deployment guidance into product patterns for a user-facing image-to-3D tool.

For direct competitive references, also read:

- `docs/knowledgebase/competitive-product-benchmark-2026.md`
- `docs/knowledgebase/frontend-ux-blueprint.md`

## Staged Workflow Beats Magic

Users trust staged workflows more than opaque one-click pipelines.

Recommended product shape:

1. Show the uploaded or normalized input.
2. Explain validation warnings before generation.
3. Generate shape first.
4. Add texture and material as a distinct stage when supported.
5. Validate exports and show downloads.

This structure matches both current research practice and current shared-runtime deployment constraints.

## Draft Versus Quality Modes

The cleanest mental model is two lanes.

### Draft

- fast;
- single-image friendly;
- CPU-safe or shorter GPU path;
- concept-grade output;
- explicitly warns that hidden sides are inferred.

### Quality

- expects coherent multi-view input;
- spends more compute on consistency and texturing;
- may require staged shape then texture execution;
- should expose why it takes longer and what evidence it uses.

## Trust Signals Users Need

Users should never have to guess what happened.

Important trust surfaces:

- preview of preprocessing result;
- runtime and backend selection;
- whether GPU or CPU was used;
- whether the output is shape-only or textured;
- manifest with seed, settings, and fallback reason;
- preserved prior runs for comparison.

These trust signals should appear before and after generation, not only in exported files.

## Input UX Patterns

Current best practice for creator tools:

- support one clear object per run;
- allow labeled front/back/left/right inputs when available;
- ask for more evidence when the system detects likely ambiguity;
- prefer actionable recovery suggestions over generic errors.

High-value recovery actions:

- add a back view;
- add a side view;
- retake under diffuse light;
- remove or simplify the background;
- switch from textured mode to shape-only draft.

## Competitive Reference Patterns

Current mainstream image apps repeatedly converge on a small set of interaction patterns:

- a fast visible entry surface on first load;
- example prompts or inspiration immediately nearby;
- conversational or iterative refinement instead of one-shot replacement;
- clear separation between creation, editing, organization, and sharing;
- preserved history, boards, moodboards, or community galleries.

For ImageEZGen3D, the strongest borrowable patterns are:

- a visible "start here" lane for draft generation;
- richer quality mode only when the user provides more evidence;
- run history and compare views that stay on the same page;
- example capture sets and recovery suggestions near the upload surface.

Additional patterns from authenticated workspaces:

- projects, recents, or spaces around the main work area;
- template galleries that convert advanced capability into approachable entry points;
- follow-up chips or suggested next edits after generation;
- explicit cost, credit, or failure-state feedback when generation does not succeed.

## Authentication And Gating Patterns

The common UX term for a creation surface blocked before meaningful value is visible is a `login wall`.

Useful distinctions:

- `login wall` or `hard auth gate`: no meaningful value before sign-in;
- `public browse plus gated creation`: inspiration is open but creation is blocked;
- `authenticated workspace shell`: creation happens inside a larger signed-in tool;
- `post-value auth` or `soft gate`: users can see or try meaningful value before being asked to sign in.

For ImageEZGen3D, if authentication is ever added for saved projects, collaboration, or remote inference, the preferred default should be post-value auth unless privacy, billing, or abuse prevention makes that impossible.

## Output UX Patterns

The output surface should support both quick inspection and serious export.

- inline 3D preview for immediate trust;
- download buttons for all supported formats;
- clear distinction between preview asset and canonical export asset;
- preserved run history with per-run manifests;
- warnings when the asset is concept-grade rather than production-grade.
- visible next-step suggestions when the output is weak or when a likely refinement path exists.

## Configuration Surface

Good defaults should live in repository config, not only in the UI.

Recommended user-facing control split:

- simple controls: mode, output format, quality preset;
- advanced controls: seed, texture size, decimation, runtime preference, adapter selection.

Recommended repo-side split:

- `pyproject.toml` holds audited defaults;
- `.env` holds local machine overrides;
- manifests record the effective values used for each run.

## Gradio Patterns

Current Gradio guidance relevant to this repo:

- `Model3D` is the natural preview surface for `.obj`, `.glb`, and `.gltf` assets.
- Blocks-style workflows are the right fit for staged multi-input pipelines.
- File inputs should be treated explicitly, with narrow upload scope when exposed through remote tooling.
- Queueing and progress states matter for long-running inference; users need visible progress, not silent waiting.

For this repo, the preview path should stay inline and same-page rather than opening a new surface unexpectedly.

The strongest app benchmark signal here is locality: inputs, status, preview, and next actions should remain visually close together.

## Hugging Face Spaces And ZeroGPU Patterns

Current platform guidance implies these product rules:

- ZeroGPU is Gradio-only.
- GPU-dependent functions should be isolated behind `@spaces.GPU`.
- CPU preprocessing, validation, manifests, and exports should stay outside GPU sections.
- Shorter GPU durations improve queue priority.
- Dynamic durations are useful when user settings materially change runtime.
- `torch.compile` is not the right ZeroGPU optimization path.
- Shared runtimes can sleep or queue, so the app should make latency and fallback understandable.

Secrets and tokens belong in Space settings, not in source.

Useful deployment-visible environment values include runtime and Space identity variables, but the app should use them only to improve behavior and diagnostics, not to hide logic.

## Performance Patterns

Most user-visible performance wins are product decisions, not model tricks.

- separate shape-only and texture-heavy paths;
- use mesh-first GLB as the default preview/export artifact;
- keep texture sizes and mesh density within browser-friendly budgets;
- avoid shipping oversized assets by default;
- do not spend GPU time on CPU-safe work.

When hosted usage later involves quotas or credits, report them explicitly instead of hiding cost or failure reasons.

## Patterns To Avoid

Competitive research also surfaces recurring mistakes:

- hard auth walls before the user sees enough value;
- overloaded menus without a primary path;
- hidden mode switches or fallback behavior;
- sending the user to a different page to inspect the main result;
- losing prompt, settings, or history between iterations.

## What The Repo Should Prefer

For ImageEZGen3D specifically:

- mesh-first outputs;
- optional splat or radiance-style complements later;
- explicit runtime and fallback visibility;
- draft-versus-quality framing;
- staged generation and export validation;
- recovery guidance that asks for better evidence instead of pretending every failure is a transient compute issue.
