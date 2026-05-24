# Release And Deploy Surfaces

Architecture map for how ImageEZGen3D ships to Hugging Face Spaces and related release targets. Use with [deployment-hf-cli.md](../deployment-hf-cli.md) (operator CLI) and [release-automation.md](../release-automation.md) (workflow inventory).

## Source Basis

- `[REPO]` `.github/workflows/hf-space.yml`
- `[REPO]` `.github/workflows/sync-hf-space.yml`
- `[REPO]` `.github/workflows/release.yml`
- `[REPO]` `scripts/hf_space_sync.py`, `scripts/release_workflow_outputs.py`
- `[REPO]` `src/imageezgen3d/hf_cli.py` (`stage_space_payload`, `deploy_commit_message`)
- `[REPO]` `pyproject.toml` → `[tool.imageezgen3d.release.forge.huggingface]`
- `[OFFICIAL]` Hugging Face Spaces install `requirements.txt` before copying source (build order)

## Deploy Paths

| Path | Trigger | Payload | When to use |
|------|---------|---------|-------------|
| **Staged HF upload (primary)** | `hf-space.yml`: push `main`/`master`, push tag `v*`, `workflow_dispatch` | Minimal staged dir via `stage_space_payload()` | Default automatic CI deploy |
| **Full-repo mirror (legacy)** | `sync-hf-space.yml`: `workflow_dispatch` only | Entire repo via `huggingface/hub-sync` | Emergency manual mirror only |
| **Operator CLI** | Local `hf upload` / `hf_space_sync.py --execute` | Staged or exclude patterns | Pre-push dry-run, hotfix deploy |
| **Python dist release** | `release.yml`: tag `v*` | GitHub Release wheels/sdist | Package publishing only; does not upload Space |

`[SYNTH]` Pull requests run plan/summary jobs only — no external Space mutation.

## Staged Payload Contract

`[REPO]` `stage_space_payload()` copies only:

- `README.md`, `app.py`, `pyproject.toml`, `requirements.txt`, `runtime.txt`
- `assets/`, `src/`

`[REPO]` `hf_space_sync.py --execute` uploads the staged directory with `--delete` patterns that strip `.github/`, `docs/`, `tests/`, `outputs/`, venvs, caches, and build artifacts from the remote Space.

This aligns with `AGENTS.md` Space payload hygiene: do not upload workspace-only artifacts.

## Credentials And Gating

- `[REPO]` `HF_TOKEN` secret required for CI sync; missing token → release plan skips Hugging Face target with reason
- `[REPO]` `[tool.imageezgen3d.release.forge.huggingface] enabled = true` in `pyproject.toml`
- `[REPO]` Sync job runs when `huggingface_action == push` from `release_workflow_outputs.py`

## Tag Deploy Behavior

`[REPO]` Since 2026-05-23 (plan 006):

- Push of `v*` release tags triggers the same staged upload as default-branch push
- Upload commit message uses `Deploy ImageEZGen3D <tag>` when `GITHUB_REF` is `refs/tags/v*`
- Tag deploy refreshes the same Space as branch deploy (not a separate Space per release)

## Port Binding On Hosted Spaces

`[REPO]` `load_config()` resolves launch port:

1. `PORT`
2. `GRADIO_SERVER_PORT` (injected by Hugging Face Gradio Spaces)
3. `IMAGEEZ_PORT`
4. `[tool.imageezgen3d.app].port` in `pyproject.toml` (local default **7865**)

`[SYNTH]` Local dev defaults to 7865; hosted Spaces typically bind via `GRADIO_SERVER_PORT`. Do not hardcode local port in app launch without reading config.

## CI Upload vs Hosted E2E Validation

| Check | Proves | Does not prove |
|-------|--------|----------------|
| `hf-space.yml` sync success | Staged files reached Space; build may start | Live app loads; generation works; adapter path honest |
| AGENTS.md hosted loop | End-to-end Block/Vase on live `hf.space` | — |

`[OPEN]` Successful CI upload must not be reported as hosted E2E validation. See [mode-validation-matrix.md](../40-operational-risk/mode-validation-matrix.md).

## Repo Implications

- Prefer `hf-space.yml` + staged payload for all automatic deploys
- Keep `sync-hf-space.yml` manual-only to avoid competing full-repo uploads
- After deploy workflow changes, run `scripts/hf_space_sync.py` dry-run locally and update parity register row P11

## Caveats

- P10 hosted Block/Vase E2E executed 2026-05-24 — see [hosted-validation-2026-05-23.md](../40-operational-risk/hosted-validation-2026-05-23.md)
- `[OPEN]` ZeroGPU adapter path not verified on live Space (CPU fallback validated with honest labeling)
- History on hosted Space uses `/data/outputs` when persistent `/data` is writable; `demo.load` refreshes History on page load (Plan 021)
- `[OFFICIAL]` Space build order requires self-contained `requirements.txt` — no editable install at build time
