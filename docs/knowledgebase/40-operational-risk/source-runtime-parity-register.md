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
| P1 | App port | `pyproject.toml` → `[tool.imageezgen3d.app].port` = 7865; env chain in `config.py` | 2026-05-24 | `[REPO]` Local default 7865; Space defaults to 7860 when `SPACE_ID` set and no port env vars; `launch()` omits `server_port` on Spaces | Re-verify if HF injects non-7860 `GRADIO_SERVER_PORT` | OK |
| P2 | Config loader default | `src/imageezgen3d/config.py` `port: int = 7865` | 2026-05-23 | Aligns with pyproject; env overrides documented in configuration.md | None | OK |
| P3 | Docker expose | `Dockerfile` EXPOSE / CMD port | 2026-05-24 | `[REPO]` Docker image uses 7865; hosted Space validated at 7860 via config + Gradio launcher | Container deploys still use Dockerfile port; Space is separate surface | OK |
| P4 | Deploy asset templates | `scripts/render_deploy_assets.py` → `deploy/` | 2026-05-23 | `[REPO]` Stray `7865` token removed from argparse; render uses `.tmpl` only; port 7865 in outputs | Re-render on image/port changes | OK |
| P5 | Deploy assets module | `src/imageezgen3d/deploy_assets.py` | 2026-05-23 | `[REPO]` Fixed `podman_dir: Path` annotation; `_render_tree` skips non-`.tmpl` sources | Run deploy_assets tests on deploy changes | OK |
| P6 | Requirements vs pyproject | `requirements.txt` vs `[project.optional-dependencies]` | 2026-05-23 | Space uses requirements-first install | Diff on every dependency change | Review on dep PRs |
| P7 | AGENTS.md vs project-intent | `AGENTS.md` vs `project-intent.md` | 2026-05-23 | `[REPO]` Intent doc previously denied AGENTS.md existence | Refreshed 2026-05-23 KB pass | OK |
| P8 | KB vs runtime claims | KB docs vs `app.py` / exporters | 2026-05-24 | `[REPO]` export-guide matches cpu-demo GLB/OBJ/PLY/STL outputs; hosted validation recorded; Space port fix documented | Re-audit when heavy adapters add texture exports | OK |
| P9 | VS Code tasks vs CI | `.vscode/tasks.json` vs `.github/workflows/ci.yml` | 2026-05-23 | `[REPO]` verification.md asserts sync | Spot-check on workflow edits | OK |
| P10 | Live HF Space behavior | Hosted app vs README frontmatter | 2026-05-24 | `[UI]` Block E2E on live Space; run `20260524-084947-19c70f8f`; cpu-demo fallback; manifest/GLB/OBJ verified | See [hosted-validation-2026-05-23.md](hosted-validation-2026-05-23.md); ZeroGPU adapter still disabled | OK |
| P11 | HF Space CI deploy | `.github/workflows/hf-space.yml` + `scripts/hf_space_sync.py` | 2026-05-23 | `[REPO]` Auto sync on default branch + `v*` tags; staged minimal payload; legacy `sync-hf-space.yml` manual-only | CI upload ≠ E2E; verify after workflow edits | OK |
| P12 | Golden sample CI attestation | `scripts/golden_sample_attestation.py` + `.github/workflows/ci.yml` job `golden-sample` | 2026-05-24 | `[REPO]` Block PNG → cpu-demo generate; manifest/GLB/OBJ/size gates in CI | Does not replace hosted P10 E2E or ZeroGPU verification | OK |
| P13 | Hosted golden smoke CI | `scripts/hosted_golden_smoke.py` + `.github/workflows/hosted-golden-smoke.yml` | 2026-05-24 | `[REPO]` Scheduled/dispatch Gradio `/generate` on live Space; export budget + run id checks | Complements P12; first green run records run id in KB | OK |

## How To Update

1. Change a listed surface → add or update row same PR.
2. After hosted validation → set Last verified date; move Status to OK or document residual `[OPEN]`.
3. When delta is intentional → note rationale in Action column.
4. When delta is accidental → fix source before closing row.

## Repo Implications

- Do not claim deploy parity while P4/P5 remain blocked. *(P4/P5 resolved 2026-05-23 in vertical-slice pass.)*
- Port 7865 migration requires vertical slice: pyproject, config, Docker, deploy scripts, rendered templates, Space settings.
- Hosted verification (P10) is mandatory for runtime/export PRs per `AGENTS.md`.

## Caveats

- `[REPO]` Hosted Block E2E recorded 2026-05-24 in [hosted-validation-2026-05-23.md](hosted-validation-2026-05-23.md) (hosted CPU fallback, not ZeroGPU).
- `[REPO]` Local Gradio browser smoke passed 2026-05-23; does not satisfy hosted E2E row.
- Rendered `deploy/` artifacts use port 7865 after 2026-05-23 vertical-slice re-render (P4 OK).
