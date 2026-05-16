# VS Code Workflow

This repo is intentionally friendly to editor-driven development. The goal is not only to have commands that work, but to make the default development loop repeatable for future contributors.

## Source Basis

This note is based on:

- `.vscode/tasks.json`;
- `.vscode/launch.json`;
- the current `.env`-based workflow;
- the Python package layout under `src/`.

## Recommended First Run

Use built-in tasks from the Command Palette with `Tasks: Run Task`.

Recommended first run:

1. `setup: create venv and install app`
2. `env: create .env from example`
3. `test: unittest`
4. `check: compile`
5. `check: future annotations`
6. `app: run gradio`

This sequence establishes the environment, creates the local override file, verifies the code slice, and only then launches the UI.

## What Each Task Is For

### `setup: create venv and install app`

- creates `.venv`;
- upgrades `pip`;
- installs the editable package with the `app` and `dev` extras.

### `env: create .env from example`

- creates a local `.env` only when one does not already exist;
- avoids overwriting machine-specific settings during repeat runs.

### `test: unittest`

- runs the current unit-test suite under `tests/`;
- is the narrowest default executable check for basic regressions.

### `check: compile`

- compiles `app.py`, `src`, `tests`, and `scripts`;
- catches syntax and import-surface issues quickly.

### `check: future annotations`

- runs the repo's lightweight Python-style consistency check;
- reinforces the current code style expectations.

### `app: run gradio`

- starts the Gradio app through the project venv;
- depends on the `.env` creation task first.

### `hf: show deployment commands`

- runs the helper script that prints recommended `hf` deployment commands;
- does not deploy anything by itself.

## Debug Configurations

Current launch profiles:

- `ImageEZGen3D: Gradio app`
- `ImageEZGen3D: unit tests`
- `ImageEZGen3D: HF helper`

These all:

- run from the workspace root;
- load `${workspaceFolder}/.env`;
- add `${workspaceFolder}/src` to `PYTHONPATH`;
- use the integrated terminal;
- keep `justMyCode` enabled for a tighter local debugging loop.

## Recommended Daily Loop

### For Code Changes

1. run the narrowest relevant task first;
2. use the unit-test or compile task before widening scope;
3. launch the app when UI, runtime, or artifact behavior changed;
4. inspect the run outputs and manifest after meaningful workflow changes.

### For Documentation Changes

1. update the relevant knowledgebase docs;
2. run `git diff --check` on the touched markdown files;
3. if the docs describe runtime or workflow behavior, confirm the source still matches the docs.

### For Deployment Prep

1. use the local validation tasks;
2. run the HF helper task for current CLI guidance;
3. only then move to the external deployment workflow.

## Environment Model

The workspace assumes:

- the venv lives at `.venv`;
- imports resolve from `src`;
- `.env` is the local override file;
- `.env` is not committed.

This matters because the debug profiles and tasks are intentionally consistent with the same local assumptions.

## Why This Workflow Matters

The repo's broader design goals show up here too:

- explicit setup over hidden editor magic;
- runnable local CPU paths over GPU-only workflows;
- narrow validation before broad confidence claims;
- inspectable helper scripts instead of undocumented deploy rituals.

## Common Gotchas

- running system Python instead of `.venv/bin/python` produces confusing mismatches;
- editing `.env` without remembering that debug profiles load it can make behavior look mysteriously different;
- the HF helper prints commands but does not create or upload a Space automatically;
- if docs, tasks, and debug profiles drift apart, the editor can appear healthy while the actual workflow is not.
