# Agent Operating Contract

Operating rules for coding agents working on ImageEZGen3D. This doc expands `AGENTS.md` with evidence discipline and KB cross-links. **`AGENTS.md` remains the live runbook** for runtime validation; this contract adds taxonomy context and pipeline hooks.

## Source Basis

- `[REPO]` `AGENTS.md`
- `[REPO]` `docs/knowledgebase/knowledgebase-authoring-playbook.md`
- `[REPO]` `docs/knowledgebase/verification.md`
- `[REPO]` `docs/knowledgebase/40-operational-risk/mode-validation-matrix.md`
- `[REPO]` `docs/knowledgebase/40-operational-risk/source-runtime-parity-register.md`

## Evidence Label Contract

Every substantive KB or agent claim must use one label:

| Label | Use when |
|-------|----------|
| `[REPO]` | Observed in source, tests, scripts, CI, or git |
| `[UI]{public}` / `[UI]{auth}` | Observed product surface; state observation boundary |
| `[OFFICIAL]` | Vendor or library documentation |
| `[SYNTH]` | Repo-specific implication; cite upstream label |
| `[OPEN]` | Unverified hosted path, auth wall, or stale doc risk |

Do not merge categories into unlabeled statements.

## Source Priority

1. User instructions and preferences
2. Existing knowledgebase (this index and canonical docs)
3. Repo evidence (`AGENTS.md`, README, `pyproject.toml`, tests, workflows)
4. Current official docs for named platforms (Gradio, HF Spaces, ZeroGPU)
5. Public HF Space observation
6. External research (label Tier 2/3 explicitly)
7. Community anecdotes — exclude unless labeled and caveated

## Runtime and Deployment Validation

`[REPO]` From `AGENTS.md`:

- Check current official documentation before changing Gradio, Hugging Face Spaces, ZeroGPU, model selection, exports, or runtime fallback behavior.
- Use the Hugging Face CLI for Space deploys when validating hosted behavior. Do not stop at generating commands or assuming a push succeeded.
- After each hosted deploy, open the live `hf.space` app and run at least one default sample (Block or Vase) end to end before declaring success.
- Confirm: app loads without build error; generation completes with run id; adapter or fallback path is visible; manifest, GLB, and OBJ artifacts are present and downloadable.
- Continue fix → deploy → retest until the validation path works or the blocker is genuinely missing implementation.
- Do not claim a runtime mode is validated unless you actually executed it.

See [mode-validation-matrix.md](../40-operational-risk/mode-validation-matrix.md) for the four-mode reporting table.

## Mode-Specific Reporting

`[REPO]` Distinguish these as **separate checks**:

| Mode | Honest claim requires |
|------|----------------------|
| Local CPU | Local app run + artifact inspection |
| Local GPU | CUDA path executed locally |
| Hosted CPU fallback | Live Space run showing fallback reason in manifest/UI |
| Hosted ZeroGPU | Live Space run with ZeroGPU adapter actually selected |

If hosted ZeroGPU is available but the configured ZeroGPU adapter is disabled, report successful fallback **without** presenting it as real ZeroGPU generation.

## Space Payload Hygiene

`[REPO]` From `AGENTS.md`:

- Prefer staged minimal uploads for Hugging Face Spaces.
- Do not upload local virtual environments, caches, outputs, history folders, or workspace-only artifacts.
- Keep the Space install contract compatible with Hugging Face requirements-first build order.
- Do not rely on editable installs unless the source tree is guaranteed present when dependencies install.

Record deploy/payload parity in [source-runtime-parity-register.md](../40-operational-risk/source-runtime-parity-register.md).

## Validation Ladder (Summary)

For doc-only work: `git diff --check` + source parity review.

For code/runtime work: follow [verification.md](../verification.md) — unittest, compileall, style guard, local workflow, artifact integrity, then hosted parity when deploy/runtime assumptions change.

## Pipeline Hooks

When using Compound Engineering skills, follow [ideation-to-pr-pipeline.md](../50-execution/ideation-to-pr-pipeline.md) for stage entry/exit criteria and KB pointers.

## Repo Implications

- Prefer updating parity register when touching config, deploy, or export surfaces.
- Refresh this contract when `AGENTS.md` changes; do not duplicate verbatim without labels.
- Mark hosted verification `[OPEN]` until browser + HF CLI evidence exists.

## Prefer / Defer / Avoid

**Prefer:** explicit mode labels in completion claims; manifest-backed evidence; index-first KB navigation.

**Defer:** adapter enablement claims; ZeroGPU success without executed GPU path.

**Avoid:** presenting CPU fallback as ZeroGPU; unlabeled runtime claims; mega-docs mixing theory and execution.
