# ImageEZGen3D Knowledgebase Index

Navigation map for all knowledgebase documents. Use this index to find authority docs before reading flat files at the repository root of `docs/knowledgebase/`.

**Last updated:** 2026-05-23

## How To Use This Index

| Authority rank | Meaning |
|----------------|---------|
| **Canonical** | Primary reference for a topic; prefer over older notes |
| **Dated slice** | Time-bound research or audit; check supersession links |
| **Companion** | Deep dive; defers to canonical doc for decisions |
| **Frontier** | Tier-3 tracking; not current product truth |

## Layer Map

### 00 — Intent

| Doc | Rank | Purpose |
|-----|------|---------|
| [project-intent.md](project-intent.md) | Canonical | Stable goals, cleanup patterns, non-goals |
| [00-intent/agent-operating-contract.md](00-intent/agent-operating-contract.md) | Canonical | Agent rules, evidence labels, validation modes |
| [00-intent/ui-fidelity-direction-2026-05-18.md](00-intent/ui-fidelity-direction-2026-05-18.md) | Dated slice | UI fidelity direction (May 2026) |
| [roadmap.md](roadmap.md) | Canonical | Execution tracks and near-term frontier |

### 10 — Architecture & Runtime

| Doc | Rank | Purpose |
|-----|------|---------|
| [architecture.md](architecture.md) | Canonical | Module boundaries and orchestration shape |
| [configuration.md](configuration.md) | Canonical | `pyproject.toml` contract and manifest visibility |
| [10-architecture-runtime/release-deploy-surfaces.md](10-architecture-runtime/release-deploy-surfaces.md) | Canonical | HF CI deploy paths, staged payload, port binding |
| [zerogpu-runtime.md](zerogpu-runtime.md) | Canonical | ZeroGPU policy and adapter gating |
| [deployment-hf-cli.md](deployment-hf-cli.md) | Canonical | Hugging Face Space deploy via CLI |
| [release-automation.md](release-automation.md) | Companion | CI/CD, forge mirrors, artifact workflows |
| [model-matrix.md](model-matrix.md) | Companion | Adapter landscape and admission criteria |
| [export-guide.md](export-guide.md) | Companion | Export formats and operator guidance |

### 20 — Domain & Theory

| Doc | Rank | Purpose |
|-----|------|---------|
| [20-theory/frontier-image-to-3d-2026-05-23.md](20-theory/frontier-image-to-3d-2026-05-23.md) | Frontier | Tier-3 image-to-3D trends (May 2026); not product truth |
| [3d-reconstruction-theory.md](3d-reconstruction-theory.md) | Frontier | Reconstruction approaches and tradeoffs |
| [evaluation-metrics.md](evaluation-metrics.md) | Frontier | Quality framing and metrics |
| [capture-guide.md](capture-guide.md) | Companion | Input capture guidance |
| [license-audit.md](license-audit.md) | Canonical | Legal gates for adapters and assets |

### 30 — Product & UX

| Doc | Rank | Purpose |
|-----|------|---------|
| [frontend-ux-blueprint.md](frontend-ux-blueprint.md) | Canonical | Product UX spec |
| [creator-product-patterns.md](creator-product-patterns.md) | Companion | Creator-workflow patterns |
| [competitive-product-benchmark-2026.md](competitive-product-benchmark-2026.md) | Dated slice | 2026 competitive benchmark |
| [prompt-behavior-investigations-2026.md](prompt-behavior-investigations-2026.md) | Dated slice | Prompt and composer behavior research |
| [frontend-implementation-patterns-2026.md](frontend-implementation-patterns-2026.md) | Dated slice | Gradio implementation patterns |
| [auth-gated-ux-patterns.md](auth-gated-ux-patterns.md) | Companion | Auth-gated UX constraints |
| [30-product-ux/reference-creator-workspace-audit-2026-05-18.md](30-product-ux/reference-creator-workspace-audit-2026-05-18.md) | Dated slice | Creator workspace audit |

### 40 — Operational Risk

| Doc | Rank | Purpose |
|-----|------|---------|
| [verification.md](verification.md) | Canonical | Validation ladder and artifact checks |
| [40-operational-risk/mode-validation-matrix.md](40-operational-risk/mode-validation-matrix.md) | Canonical | Four-mode honesty matrix |
| [40-operational-risk/source-runtime-parity-register.md](40-operational-risk/source-runtime-parity-register.md) | Canonical | Living drift log |
| [failure-modes.md](failure-modes.md) | Canonical | Failure classes and recovery |

### 50 — Execution

| Doc | Rank | Purpose |
|-----|------|---------|
| [50-execution/ideation-to-pr-pipeline.md](50-execution/ideation-to-pr-pipeline.md) | Canonical | CE workflow stage map |
| [50-execution/ui-fidelity-implementation-checklist-2026-05-18.md](50-execution/ui-fidelity-implementation-checklist-2026-05-18.md) | Dated slice | UI fidelity implementation checklist |
| [vscode-workflow.md](vscode-workflow.md) | Companion | Local dev tasks and launch configs |

### 90 — Meta

| Doc | Rank | Purpose |
|-----|------|---------|
| [knowledgebase-authoring-playbook.md](knowledgebase-authoring-playbook.md) | Canonical | Evidence rules and taxonomy |
| [knowledgebase-builder-agent-spec.md](knowledgebase-builder-agent-spec.md) | Canonical | KB builder agent contract |

## Quick Entry Points

| If you need… | Start here |
|--------------|------------|
| Project goals and non-goals | [project-intent.md](project-intent.md) + [STRATEGY.md](../../STRATEGY.md) |
| HF deploy / CI upload contract | [10-architecture-runtime/release-deploy-surfaces.md](10-architecture-runtime/release-deploy-surfaces.md) |
| Agent validation rules | [00-intent/agent-operating-contract.md](00-intent/agent-operating-contract.md) |
| What to run before claiming done | [verification.md](verification.md) + [mode-validation-matrix.md](40-operational-risk/mode-validation-matrix.md) |
| Drift between source and hosted | [source-runtime-parity-register.md](40-operational-risk/source-runtime-parity-register.md) |
| CE pipeline stages | [ideation-to-pr-pipeline.md](50-execution/ideation-to-pr-pipeline.md) |
| Writing new KB docs | [knowledgebase-authoring-playbook.md](knowledgebase-authoring-playbook.md) |

## Taxonomy Migration Status

`[SYNTH]` Numbered folders exist for `00-intent/`, `30-product-ux/`, `40-operational-risk/`, and `50-execution/`. Most docs remain flat at `docs/knowledgebase/` root. This index links flat files by layer until a consolidation pass moves them physically.

## Caveats

- `[OPEN]` Hosted Space Block/Vase E2E (P10) not verified — CI upload success is not E2E validation.
- `[REPO]` Port env chain (`PORT` / `GRADIO_SERVER_PORT` / `IMAGEEZ_PORT`) documented 2026-05-23; live Space binding still `[OPEN]`.
- Dated slices may lag in-flight UI changes; check git diff against `app.py` when implementing UX work.
