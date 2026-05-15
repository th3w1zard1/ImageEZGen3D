# VS Code Workflow

Use built-in tasks from the Command Palette: `Tasks: Run Task`.

Recommended first run:

1. `setup: create venv and install app`
2. `env: create .env from example`
3. `test: unittest`
4. `check: compile`
5. `check: future annotations`
6. `app: run gradio`

Debug configurations:

- `ImageEZGen3D: Gradio app`
- `ImageEZGen3D: unit tests`
- `ImageEZGen3D: HF helper`

The workspace settings point Python analysis at `.venv` and `src`, and load `.env` for debug runs.
