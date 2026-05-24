# Ideation-to-PR Pipeline

Maps Compound Engineering workflow stages to ImageEZGen3D knowledgebase entry points and exit criteria. Use when running `/lfg`, `/ce-plan`, or multi-skill KB/runtime passes.

## Source Basis

- `[REPO]` `docs/knowledgebase/knowledgebase-builder-agent-spec.md`
- `[REPO]` `docs/knowledgebase/00-intent/agent-operating-contract.md`
- `[SYNTH]` Compound Engineering skill ordering (ce-ideate → ce-plan → ce-work → ce-code-review → ce-test-browser → ce-commit-push-pr)

## Stage Map

| Stage | Skill / agent | Entry artifact | Exit criteria | KB pointers (≤3) |
|-------|---------------|----------------|---------------|------------------|
| **Ideate** | `ce-ideate` | Focus hint or "surprise me" | Ranked survivors in `docs/ideation/` or synthesis for planning | [project-intent.md](../project-intent.md), [roadmap.md](../roadmap.md), [README.md](../README.md) |
| **Brainstorm** | `ce-brainstorm` | Selected ideation survivor | `docs/brainstorms/*-requirements.md` with scope boundaries | [frontend-ux-blueprint.md](../frontend-ux-blueprint.md), [creator-product-patterns.md](../creator-product-patterns.md) |
| **Plan** | `ce-plan` | Requirements doc or feature description | `docs/plans/*-plan.md` with implementation units | [architecture.md](../architecture.md), [configuration.md](../configuration.md), [verification.md](../verification.md) |
| **Work** | `ce-work` | Plan file path | Files changed per units; tests pass for touched code | [vscode-workflow.md](../vscode-workflow.md), [verification.md](../verification.md) |
| **Review** | `ce-code-review` | `mode:autofix plan:<plan-path>` | Autofixes committed; residual findings recorded | [mode-validation-matrix.md](../40-operational-risk/mode-validation-matrix.md), [failure-modes.md](../failure-modes.md), [agent-operating-contract.md](../00-intent/agent-operating-contract.md) |
| **Browser test** | `ce-test-browser` | `mode:pipeline` | UI/runtime surfaces exercised when applicable | [verification.md](../verification.md), [mode-validation-matrix.md](../40-operational-risk/mode-validation-matrix.md) |
| **Ship** | `ce-commit-push-pr` | Remaining changes | Branch pushed; PR open with test plan | [release-automation.md](../release-automation.md), [deployment-hf-cli.md](../deployment-hf-cli.md) |

## LFG Pipeline (`/lfg`)

`[SYNTH]` Autopilot ordering:

1. `ce-plan` — plan file required in `docs/plans/` before work
2. `ce-work` — implement plan units
3. `ce-code-review mode:autofix` — autofix and residual summary
4. Persist review autofixes (commit + push)
5. Residual handoff — PR body or `docs/residual-review-findings/` fallback
6. `ce-test-browser mode:pipeline`
7. `ce-commit-push-pr`

KB-only passes skip browser test when no UI/runtime surface changes; still run doc hygiene (`git diff --check`).

## KB Orchestration Pass (kb-orchestrator)

For knowledgebase builds, prefer this sequence before feature work:

1. `kb-repo-archaeologist` — repo anchor extraction
2. `kb-drift-detector` — drift baseline (optional but recommended)
3. `ce-ideate` — gap ideation (headless in pipeline)
4. `ce-plan` — KB implementation plan
5. `ce-work` — write/update docs
6. Curation gate — evidence labels, index links, parity register update

## Exit Criteria by Change Type

| Change type | Minimum exit evidence |
|-------------|----------------------|
| Docs only | `git diff --check`; index/parity register updated if authority changed |
| Python/runtime | unittest + compileall + style guard; mode matrix label if claiming validation |
| Deploy/Space | HF CLI deploy proof; hosted E2E template filled; parity register row updated |

## Repo Implications

- Plans must use repo-relative paths only.
- Do not skip plan gate in LFG even for KB work.
- Review residuals must land in PR body or tracked fallback file before DONE.

## Prefer / Defer / Avoid

**Prefer:** narrow vertical slices; honest mode labels; index-first navigation.

**Defer:** full flat-file taxonomy migration; adapter enablement docs until admission runbook pass.

**Avoid:** claiming hosted validation without evidence template; plan-less KB sprawl.
