# Source-Runtime Parity Register

Living log of surfaces where repository source, built assets, documentation, and hosted runtime can drift apart. Update this register when touching listed surfaces or after validation runs.

## Source Basis

- `[REPO]` `docs/knowledgebase/knowledgebase-authoring-playbook.md` (drift gotcha)
- `[REPO]` `docs/knowledgebase/verification.md` §Source-Versus-Runtime Parity
- `[REPO]` `pyproject.toml`, `Dockerfile`, `.env.example`, `requirements.txt`
- `[REPO]` `src/imageezgen3d/config.py`, `src/imageezgen3d/deploy_assets.py`
- `[REPO]` `scripts/render_deploy_assets.py`
- `[REPO]` `AGENTS.md`, `docs/knowledgebase/project-intent.md`

## Register

| ID | Surface | Source of truth | Last verified | Observed delta | Action | Status |
|----|---------|-----------------|---------------|----------------|--------|--------|
| P1 | App port | `pyproject.toml` → `[tool.imageezgen3d.app].port` = 7865 | 2026-05-23 | `[REPO]` Port migrated from 7860 across config, Docker, `.env.example` | Confirm live HF Space exposes same port | `[OPEN]` |
| P2 | Config loader default | `src/imageezgen3d/config.py` `port: int = 7865` | 2026-05-23 | Aligns with pyproject | None | OK |
| P3 | Docker expose | `Dockerfile` EXPOSE / CMD port | 2026-05-23 | `[REPO]` Uses 7865 | Verify Space container binding | `[OPEN]` |
| P4 | Deploy asset templates | `scripts/render_deploy_assets.py` → `deploy/` | 2026-05-23 | `[REPO]` `--container-port` default 7865; **syntax corruption** in argparse (`required=True)7865`) | Fix script before re-render; verify Helm/K8s/Nomad/Podman outputs | **BLOCKED** |
| P5 | Deploy assets module | `src/imageezgen3d/deploy_assets.py` | 2026-05-23 | `[REPO]` **Invalid annotation** `podman_dir: Path7865787865` | Fix type annotation; run deploy_assets tests | **BLOCKED** |
| P6 | Requirements vs pyproject | `requirements.txt` vs `[project.optional-dependencies]` | 2026-05-23 | Space uses requirements-first install | Diff on every dependency change | Review on dep PRs |
| P7 | AGENTS.md vs project-intent | `AGENTS.md` vs `project-intent.md` | 2026-05-23 | `[REPO]` Intent doc previously denied AGENTS.md existence | Refreshed 2026-05-23 KB pass | OK |
| P8 | KB vs runtime claims | KB docs vs `app.py` / exporters | 2026-05-23 | `[OPEN]` In-flight UI/export diff may ahead of export-guide | Re-check after code lands | `[OPEN]` |
| P9 | VS Code tasks vs CI | `.vscode/tasks.json` vs `.github/workflows/ci.yml` | 2026-05-23 | `[REPO]` verification.md asserts sync | Spot-check on workflow edits | OK |
| P10 | Live HF Space behavior | Hosted app vs README frontmatter | — | Not executed this pass | Run Block/Vase E2E; record in mode matrix evidence template | `[OPEN]` |

## How To Update

1. Change a listed surface → add or update row same PR.
2. After hosted validation → set Last verified date; move Status to OK or document residual `[OPEN]`.
3. When delta is intentional → note rationale in Action column.
4. When delta is accidental → fix source before closing row.

## Repo Implications

- Do not claim deploy parity while P4/P5 remain blocked.
- Port 7865 migration requires vertical slice: pyproject, config, Docker, deploy scripts, rendered templates, Space settings.
- Hosted verification (P10) is mandatory for runtime/export PRs per `AGENTS.md`.

## Caveats

- `[OPEN]` No browser validation executed during 2026-05-23 KB pass.
- Rendered `deploy/` artifacts may still reference 7860 until P4 is fixed and templates re-rendered.
