# Verification Gate

Do not call work complete until evidence exists for the slice that changed.

The repo's definition of done is broader than "tests passed once." It includes source correctness, workflow behavior, artifact integrity, and hosted-runtime honesty.

## Source Basis

This note is based on:

- the current workspace tasks;
- the existing tests and lightweight checks;
- the runtime-selection path in `orchestrator.py` and `runtime.py`;
- the run-store and manifest behavior;
- the UX expectations established across the knowledgebase.

## Validation Ladder

Use the narrowest meaningful check first, then widen only when the change surface requires it.

### 1. Documentation-Only Hygiene

For markdown-only changes:

- run `git diff --check` on touched docs;
- confirm the changed docs still match source and runtime behavior where relevant.

### 2. Narrow Automated Checks

For Python or workflow changes, use the current repo checks:

```bash
PYTHONPATH=src .venv/bin/python -m unittest discover -s tests
PYTHONPATH=src .venv/bin/python -m compileall -q app.py src tests scripts
PYTHONPATH=src .venv/bin/python scripts/check_python_style.py
```

Equivalent VS Code tasks already exist and should stay in sync with these commands.

### 3. Local Workflow Check

Run the app when the touched slice affects:

- UI flow;
- runtime selection;
- preprocessing;
- run storage;
- manifest contents;
- export availability.

### 4. Artifact-Integrity Check

When generation or export behavior changes, inspect the actual run folder rather than trusting the UI alone.

### 5. Hosted Or Runtime-Parity Check

When a change touches Spaces, ZeroGPU, deploy flow, or runtime assumptions, verify the hosted-facing story too.

## Automated Baseline

The current baseline automated evidence is:

- unit tests pass;
- the code compiles;
- the repo's style check passes.

That is necessary but not sufficient for product claims.

## Manifest And Artifact Checks

For a successful run, inspect at least these surfaces:

- a run folder exists under `outputs/`;
- the run folder contains the expected subdirectories such as `inputs`, `processed`, `meshes`, `exports`, and `reports`;
- `manifest.json` exists and updates as the run advances;
- the manifest includes requested adapter, selected adapter, runtime details, and fallback reason when applicable;
- input validation output exists;
- exported artifacts exist for the advertised formats;
- mesh inspection output is coherent with what the UI claims.

For a failed run:

- the manifest should still exist;
- stage should end in a failed state rather than silent disappearance;
- the error should be preserved clearly enough to diagnose the problem later.

## Manual UI Checks

- start the app from the project venv after installing dependencies;
- upload a valid image;
- confirm the normalized or validated input preview appears before generation;
- confirm the UI explains whether the run is in draft or quality mode;
- confirm the main workflow stays on the same page and does not eject the user into another route for the core preview path;
- generate with the CPU demo path;
- confirm runtime status is visible and fallback reasons are explicit when relevant;
- confirm inline model preview updates in the same page;
- confirm manifest, GLB, and OBJ downloads are available when the run succeeds;
- confirm prior run folders remain intact after a new run, subject to retention policy;
- confirm validation and failure messages tell the user what to do next, not only that something failed.

## Benchmark-Driven UX Checks

- confirm the first screen shows a clear primary path instead of an undifferentiated wall of controls;
- confirm examples, capture guidance, or prompt scaffolds are visible near the main entry surface;
- confirm advanced settings are progressive rather than mandatory for the first success;
- confirm generated assets and exported assets are clearly traceable to the same run;
- confirm the app keeps trust surfaces nearby: runtime choice, fallback reason, validation report, and export path.

## Runtime And ZeroGPU Checks

- confirm the Space SDK is Gradio when the hosted path is involved;
- confirm GPU-only adapters are decorated with `@spaces.GPU` when they become real runtime paths;
- confirm no `torch.compile` path is enabled for ZeroGPU use;
- confirm CPU preprocessing and storage logic still run without CUDA;
- confirm default `auto` backend records whether ZeroGPU was used or why CPU fallback was selected;
- confirm local execution does not pretend it is a genuine ZeroGPU environment.

## Source-Versus-Runtime Parity Checks

When the change touches deployment, runtime, or docs, verify parity across:

- `pyproject.toml`;
- `requirements.txt`;
- README instructions;
- task and debug workflows;
- knowledgebase notes describing the same behavior.

This prevents the common failure where the repo looks coherent in source but the served or documented experience says something different.

## Evidence Expectations By Change Type

### Docs Only

- patch hygiene;
- source parity.

### Code Only

- automated checks;
- artifact or runtime check if behavior changed.

### UI Or Workflow Changes

- automated checks;
- local app run;
- manual path verification;
- artifact inspection.

### Deployment Or Runtime Changes

- automated checks;
- local app run when possible;
- hosted or deploy-path verification;
- source-versus-runtime parity review.

## Practical Rule

Verification is part of the product. If the user cannot tell what path ran, what failed, or where the outputs came from, the implementation is not actually complete.
