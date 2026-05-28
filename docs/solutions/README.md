# Institutional Learnings (`docs/solutions/`)

Searchable compound documentation for solved problems and durable practices. Used by `ce-learnings-researcher`, `/ce-compound`, and LFG passes before implementing features.

## How To Search

1. **By topic:** browse category subdirectories below
2. **By metadata:** grep frontmatter fields:

```bash
rg -l "tags:.*hf-space" docs/solutions/
rg -l "problem_type: build_error" docs/solutions/
rg -l "module: release-automation" docs/solutions/
```

3. **By keyword:** `rg -i "staged payload|GRADIO_SERVER_PORT|F401" docs/solutions/`

## Categories

| Directory | problem_type values |
|-----------|---------------------|
| `build-errors/` | `build_error`, CI/lint failures |
| `architecture-patterns/` | `architecture_pattern` |
| `best-practices/` | `best_practice` |
| `tooling-decisions/` | `tooling_decision` |
| `workflow-issues/` | `workflow_issue` |

Frontmatter contract: Compound Engineering `ce-compound` schema (`module`, `date`, `problem_type`, `component`, `severity`, `tags`).

## Authority Hierarchy

- **KB runbooks** (`docs/knowledgebase/`) — canonical operational detail
- **Plans** (`docs/plans/`) — how we decided to build something
- **Solutions** (here) — what we learned when it broke or when a pattern worked

When a solution and KB doc overlap, prefer KB for procedure and solutions for the distilled lesson + pointer.

## Index (2026-05-23 bootstrap)

| Doc | Track | Summary |
|-----|-------|---------|
| [build-errors/ci-ruff-and-style-guard-2026-05-23.md](build-errors/ci-ruff-and-style-guard-2026-05-23.md) | Bug | PR #1 lint/style CI failures |
| [architecture-patterns/hf-space-staged-payload-ci-deploy-2026-05-23.md](architecture-patterns/hf-space-staged-payload-ci-deploy-2026-05-23.md) | Knowledge | Staged HF upload on branch + tag |
| [best-practices/ci-upload-vs-hosted-e2e-2026-05-23.md](best-practices/ci-upload-vs-hosted-e2e-2026-05-23.md) | Knowledge | CI sync ≠ browser E2E |
| [tooling-decisions/gradio-port-env-precedence-2026-05-23.md](tooling-decisions/gradio-port-env-precedence-2026-05-23.md) | Knowledge | PORT / GRADIO_SERVER_PORT chain |
| [tooling-decisions/hf-space-demo-port-binding-2026-05-24.md](tooling-decisions/hf-space-demo-port-binding-2026-05-24.md) | Knowledge | Module-level demo + Space port 7860 |
| [architecture-patterns/trust-slice-completion-2026-05-24.md](architecture-patterns/trust-slice-completion-2026-05-24.md) | Knowledge | Trust slice landed — golden CI vs hosted E2E |
| [best-practices/hunyuan-ci-artifact-parity-2026-05-27.md](best-practices/hunyuan-ci-artifact-parity-2026-05-27.md) | Knowledge | Hunyuan audit vs preflight JSON parity; use `hunyuan_preflight_bundle.py` in CI |
| [best-practices/g7-false-neural-golden-smoke-guard-2026-05-28.md](best-practices/g7-false-neural-golden-smoke-guard-2026-05-28.md) | Knowledge | Golden smoke fails false G7 neural status while adapter disabled |
| [best-practices/hosted-golden-smoke-record-verify-2026-05-28.md](best-practices/hosted-golden-smoke-record-verify-2026-05-28.md) | Knowledge | CI verifies `hosted-golden-smoke.json` schema including `g7_false_neural_guard_ok` |
| [best-practices/hosted-export-tier-smoke-record-verify-2026-05-28.md](best-practices/hosted-export-tier-smoke-record-verify-2026-05-28.md) | Knowledge | CI verifies `hosted-export-tier-smoke.json` draft+balanced checks |
| [best-practices/hunyuan-g7-live-probe-scheduled-smoke-2026-05-28.md](best-practices/hunyuan-g7-live-probe-scheduled-smoke-2026-05-28.md) | Knowledge | Scheduled G7 live probe rejects false neural success while adapter disabled |
| [best-practices/hosted-smoke-guard-stack-2026-05-28.md](best-practices/hosted-smoke-guard-stack-2026-05-28.md) | Knowledge | Index: golden + export-tier + bundle + G7 live-probe scheduled smoke guards |

## Related

- [docs/knowledgebase/README.md](../knowledgebase/README.md)
- [docs/knowledgebase/50-execution/ideation-to-pr-pipeline.md](../knowledgebase/50-execution/ideation-to-pr-pipeline.md)
- `AGENTS.md` — search solutions before deploy/runtime changes
