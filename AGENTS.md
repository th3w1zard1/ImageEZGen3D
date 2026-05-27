# ImageEZGen3D Agent Notes

## Institutional Learnings

- Before implementing deploy, CI, runtime, or verification changes, search `docs/solutions/` for applicable past learnings (`ce-learnings-researcher` or `rg -l "tags:.*<topic>" docs/solutions/`).
- Start at [docs/solutions/README.md](docs/solutions/README.md) for the index. Prefer solutions for distilled lessons; use `docs/knowledgebase/` for full runbooks.

## Runtime and Deployment Validation

- For any change that affects Gradio, Hugging Face Spaces, ZeroGPU, model selection, exports, or runtime fallback behavior, check current official documentation for the named platform or library before changing code.
- Use the Hugging Face CLI for Space deploys when validating hosted behavior. Do not stop at generating commands or assuming a push succeeded.
- After each hosted deploy, open the live `hf.space` app in a browser and run at least one default sample image end to end before declaring success.
- Use one of the built-in sample inputs such as `Block` or `Vase` for hosted verification unless the task explicitly requires another asset.
- Confirm all of the following for hosted verification:
  - the app loads without a build error
  - generation completes and reports a run id
  - the selected adapter or fallback path is visible in the result
  - manifest, GLB, and OBJ artifacts are present and downloadable
- Continue the fix, deploy, and retest loop until the requested validation path works or until the remaining blocker is a genuinely missing implementation.
- Do not claim a runtime mode is validated unless you actually executed it. Call out unimplemented or untested modes explicitly.
- Before enabling `hunyuan-zerogpu`, run `python scripts/hunyuan_preflight_bundle.py` (admission audit + enablement preflight + artifact parity verify; sets `PYTHONPATH=src` automatically), or the three scripts in [docs/knowledgebase/hunyuan-g9-enablement-runbook.md](docs/knowledgebase/hunyuan-g9-enablement-runbook.md). Close G1–G8 in `docs/knowledgebase/hunyuan-admission-gates.md`. See [docs/solutions/best-practices/hunyuan-ci-artifact-parity-2026-05-27.md](docs/solutions/best-practices/hunyuan-ci-artifact-parity-2026-05-27.md). CI and scheduled hosted smoke use the same JSON + verify contract.

## Mode-Specific Reporting

- Distinguish local CPU, local GPU, hosted CPU fallback, and hosted ZeroGPU validation as separate checks.
- If hosted ZeroGPU is available but the configured ZeroGPU adapter is disabled, report the successful fallback behavior without presenting it as real ZeroGPU generation.

## Space Payload Hygiene

- Prefer staged minimal uploads for Hugging Face Spaces.
- Do not upload local virtual environments, caches, outputs, history folders, or other workspace-only artifacts.
- Keep the Space install contract compatible with Hugging Face's requirements-first build order. Do not rely on editable installs unless the source tree is guaranteed to be present when dependencies are installed.
