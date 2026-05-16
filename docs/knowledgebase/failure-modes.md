# Failure-Mode Playbook

This note is not only about model quality. It covers the full stack of ways the user can lose trust in an image-to-3D workflow: bad input, wrong runtime assumptions, weak outputs, disconnected artifacts, and misleading UI behavior.

## Core Principle

The project should fail in ways that are:

- visible;
- classified;
- recoverable;
- preserved in the run record.

## Failure Matrix

| Symptom | Likely Cause | Suggested Recovery |
| --- | --- | --- |
| Missing or wrong back side | Single image has no rear evidence | Add labeled back or side views, or explicitly treat the result as a draft |
| Blobby silhouette | Low resolution, crop, motion blur, or soft focus | Retake a sharper image with the full object visible |
| Input is rejected or heavily warned | Image is too small, too large, low contrast, or otherwise outside validation thresholds | Use a clearer image closer to the recommended capture envelope |
| Holes or loose parts | Thin structures, segmentation errors, or weak visual evidence | Retake on a cleaner background and plan for mesh repair |
| Stretched or implausible texture | UV or bake limitations, missing viewpoints, or occluded surfaces | Lower texture expectations, add coherent views, or export shape-first |
| Reflective or transparent failure | Material properties violate common reconstruction assumptions | Use a matte proxy, softer diffuse lighting, or manual cleanup |
| Fine structures disappear | Input evidence is insufficient or simplification pressure is too high | Capture more views and treat production detail as a later cleanup stage |
| Bad topology | Generative mesh is not production retopology | Retopologize in DCC tools for game or production use |
| Output looks plausible in preview but weak in export | Preview and artifact integrity are not being checked together | Inspect exported files and mesh report, not only the viewer |
| Unknown adapter error | Requested adapter name is not registered | Use a listed adapter choice or leave the app on `auto` |
| ZeroGPU never engages | Not running in a valid Spaces runtime, `spaces` support missing, or hosted adapter not enabled | Accept CPU fallback or fix the hosted environment instead of assuming GPU should have run |
| Run aborts because CPU fallback is disabled | ZeroGPU could not be used and fallback was intentionally blocked | Re-enable CPU fallback or fix the hosted prerequisites |
| User cannot tell why runtime changed | Auto routing and fallback reason are not surfaced clearly enough | Show runtime status and fallback reason near progress and output |
| User thinks draft output is a bug | Single-image ambiguity was not framed clearly | Mark draft mode explicitly and explain that hidden sides are inferred |
| User loses confidence after generation | Preview, export, validation, and manifest feel disconnected | Keep preview, downloads, validation, and run metadata visible in one place |
| User retries blindly | Failure text is generic or shamefully vague | Suggest the best next evidence step: add view, retake image, or lower expectation |
| UI feels overwhelming | Too many controls are shown before first success | Use progressive disclosure and keep a short primary path |
| Main result opens elsewhere | Preview flow leaves the current page | Keep preview inline and preserve current working context |
| Prior outputs seem to vanish | Retention settings or output location were not understood | Surface output location and retention policy clearly |
| Hosted deployment behaves differently from local docs | Source-versus-runtime drift in config, requirements, or deploy assumptions | Reconcile docs, source, and hosted behavior before calling the deployment healthy |

## Failure Families

### Capture Failures

These are evidence problems, not runtime problems.

Common examples:

- missing views;
- blur;
- crop issues;
- reflective or transparent materials;
- weak background separation.

Best response:

- ask for better evidence or lower the claim from "quality reconstruction" to "draft concept mesh."

### Runtime-Selection Failures

These occur when the user expects one runtime path but another one actually runs.

Common examples:

- ZeroGPU is unavailable locally;
- a placeholder hosted adapter is selected in theory but not actually configured;
- CPU fallback is disabled and the hosted path is not viable.

Best response:

- make the runtime decision and fallback reason explicit before and after generation.

### Artifact-Integrity Failures

These happen when generation technically completes but the exported or persisted outputs are not coherent.

Common examples:

- manifest exists but is incomplete;
- preview works but exports are missing;
- artifacts exist but the user cannot trace them back to a run.

Best response:

- treat manifests, reports, exports, and preview as one connected trust surface.

### Product-Trust Failures

These are often more damaging than raw geometry defects.

Common examples:

- draft mode not labeled;
- generic error text;
- a disconnected preview or export path;
- workflow context lost by opening a different page.

Best response:

- keep the app honest about what it inferred, what it validated, and what the user should do next.

## Recovery Rules

- prefer the next best evidence step over generic retry advice;
- preserve failure state in the manifest instead of hiding it;
- prefer partial useful success over fake full success, for example shape-only export when texturing is not trustworthy;
- classify whether the problem came from capture, runtime, adapter readiness, export, or UX clarity.

## Evidence Rule

Community reports and forum anecdotes are useful for discovering failure classes. They are not enough by themselves to justify product-wide benchmark claims.
