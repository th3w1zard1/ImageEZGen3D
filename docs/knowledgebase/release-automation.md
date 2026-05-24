# Release Automation

This repo now has dedicated release workflows for forge mirroring, Hugging Face Spaces, and runtime artifact publishing.

## Workflow Split

- `ci.yml` stays read-only and validates the release planning logic with no side effects.
- `forge-mirrors.yml` handles GitLab and Codeberg repository creation or reuse plus branch and tag sync.
- `hf-space.yml` handles Hugging Face Space create-or-upload behavior on default-branch pushes, `v*` release tags, and manual dispatch.
- `sync-hf-space.yml` is a manual full-repo mirror escape hatch only; it does not run automatically on push.
- `runtime-artifacts.yml` handles OCI image publication plus Helm, Kubernetes, Nomad, Podman, and GitHub release assets.

That split is intentional: each workflow owns one deliverable family instead of mixing unrelated external targets into one file.

For architecture-level deploy path comparison (staged payload vs legacy mirror, tag triggers, CI vs E2E), see [10-architecture-runtime/release-deploy-surfaces.md](10-architecture-runtime/release-deploy-surfaces.md).

## Default Behavior

The release surfaces follow the same anti-magic rule as the runtime path.

- pull requests are summary-only and do not create or push external state;
- `push` to `main` or `master`, `push` of `v*` release tags, and `workflow_dispatch` may create missing targets and publish when credentials exist;
- default-branch image publication resolves to `latest` plus an immutable `sha-*` tag;
- pull requests resolve to `pr-*` tags for summaries and dry runs;
- if a target is enabled but credentials are absent, the workflow reports a skip reason instead of failing silently.

## Required Credentials

- `HF_TOKEN` for Hugging Face Space create-or-upload.
- `GITLAB_TOKEN` for GitLab mirror creation and GitLab registry publication.
- `CODEBERG_TOKEN` for Codeberg repository creation and sync.
- `DOCKERHUB_USERNAME` and `DOCKERHUB_TOKEN` for Docker Hub image publication.
- GitHub-hosted workflows use the built-in `GITHUB_TOKEN` for GHCR publication and GitHub release asset upload.

Optional GitLab registry auth can also use `GITLAB_USERNAME`; the workflow falls back to `oauth2` when only a personal access token is provided.

## Local Preview Commands

Use the local scripts before pushing workflow changes.

```bash
PYTHONPATH=src .venv/bin/python scripts/gh_repo_check.py
PYTHONPATH=src .venv/bin/python scripts/release_plan_check.py
PYTHONPATH=src .venv/bin/python scripts/forge_sync.py
PYTHONPATH=src .venv/bin/python scripts/hf_space_sync.py
PYTHONPATH=src .venv/bin/python scripts/render_deploy_assets.py --image ghcr.io/th3w1zard1/imageezgen3d:latest --output-dir tmp/release-assets
```

These are also exposed as VS Code tasks.

`scripts/gh_repo_check.py` and `scripts/hf_space_check.py` are the dry-run CLI mirrors for the GitHub release-asset and Hugging Face Space workflows. They exist so local operators can verify auth, resolved destinations, and the exact recommended commands before a branch push triggers workflow execution.

## Target Sources

`pyproject.toml` is still the committed source of truth for release targets.

- use `[tool.imageezgen3d.release.*]` for repo-wide defaults;
- use `.env` or process environment variables for machine-specific overrides;
- use workflow inputs only for temporary dispatch values such as an explicit `image_tag`.

That keeps the fallback behavior auditable instead of scattering important defaults across multiple workflow files.
