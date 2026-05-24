# Hosted Validation Record — 2026-05-23

Evidence for Plan 005 hosted E2E (parity register P10). Follows the template in [mode-validation-matrix.md](mode-validation-matrix.md).

## Hosted validation record

- **Date:** 2026-05-24 (UTC run timestamp on Space)
- **Space URL:** https://th3w1zard1-imageezgen3d.hf.space/
- **Mode claimed:** hosted CPU fallback
- **Sample used:** Block (`assets/examples/teal_block.png`)
- **Run id:** `20260524-084947-19c70f8f`
- **Adapter shown:** Local CPU Preview (`cpu-demo`)
- **Fallback reason:** ZeroGPU runtime present; configured ZeroGPU model adapter not enabled (`ZeroGPU runnable now: False`)
- **Artifacts verified:** manifest ☑ GLB ☑ OBJ ☑
- **Build/load:** no error ☑ (Space stage `RUNNING` after deploy commit `3ad22d80`)
- **Evidence link:** Gradio API `/generate` call via `gradio_client`; manifest 2339 bytes; GLB 12144 bytes; OBJ 369 bytes

## Plan 012 validation (fallback honesty UI)

After PR #4 merge (`e3dec36` on `main`) and deploy commit `51bf9f293724b3ab32d85906082f032e15b1d68b`:

- **Run id:** `20260524-095746-972cc9ea`
- **Mode:** hosted CPU fallback (`Local CPU Preview` / `cpu-demo`)
- **Fallback reason:** ZeroGPU runtime present; configured ZeroGPU model adapter not enabled yet
- **Preview disclaimer:** present in status markdown and manifest `preview_disclaimer`
- **Artifacts verified:** manifest ☑ (2589 bytes) GLB ☑ (12144 bytes) OBJ ☑ (369 bytes)
- **Evidence:** Gradio API `/generate` with Block sample (`assets/examples/teal_block.png`)

## Plan 021 validation (History session parity)

After PR #12 merge (`03b82fc` on `main`) and deploy (2026-05-24):

- **Run id:** `20260524-175359-95c7ebb7` (post-merge `/generate` on `main` after redeploy; browser `demo.load` shows latest run on Create tab)
- **Also:** `20260524-175040-3313c6fb` (immediate post-merge generate before Space rebuild settled)
- **Prior branch evidence:** `20260524-174702-003962b1` (API `/generate` seed on feature branch)

Pre-merge branch deploy (`feat/hosted-history-session-parity`, 2026-05-24):

- **Run id:** `20260524-174702-003962b1` (API `/generate` seed)
- **History:** browser History tab lists run after page reload; **Open Run** shows manifest inspect + `## What happened` + GLB/OBJ downloads
- **Mode:** hosted CPU fallback
- **Evidence:** live Space browser smoke + Gradio API

## Plan 017 validation (manifest-driven UI)

After PR #9 merge (`507f003` on `main`) and Hub deploy commit `02bc0c29b5780929360d96e2ab6f5c197a20a3fe` (2026-05-24):

- **Run id:** `20260524-173153-8baf7797`
- **Mode:** hosted CPU fallback (`Local CPU Preview` / `cpu-demo`)
- **Comprehension exit:** status includes `## What happened` with output tier, mesh type, fallback, and suggested next steps (manifest_ui report path)
- **Quality intake:** live Create tab shows “Choose your output tier before generating” and fallback notice in Project Rail (browser smoke)
- **Artifacts verified:** manifest ☑ (2536 bytes) GLB ☑ (12144 bytes) OBJ ☑ (369 bytes)
- **Evidence:** Gradio API `/generate` with Block sample (`assets/examples/teal_block.png`), starter flow `single-photo-draft`
- **History inspect:** `[REPO]` `tests/test_app.py::test_history_inspect_html_composes_status_card_and_artifact_strip` covers `run-status-card` + `artifact-strip` composition; `[UI]` History tab loads on live Space but lists runs only after in-session generation (API `/generate` alone did not populate browser History on 2026-05-24)

## Plan 014 validation (trust-first Phase 1 UX)

After PR #6 merge (`8dd87f1` on `main`) and deploy commit `dfd4990adc93bbaba18ff05541a0ae186307caba`:

- **Run id:** `20260524-121906-f2550d30`
- **Mode:** hosted CPU fallback (`Local CPU Preview` / `cpu-demo`)
- **Comprehension exit:** status includes `## What happened`, output tier, mesh type, fallback, and suggested next steps
- **Quality intake:** live Create tab shows “Choose your output tier” panel (browser smoke)
- **Artifacts verified:** manifest ☑ (quality=`draft` in parameters) GLB ☑ OBJ ☑
- **Evidence:** Gradio API `/generate` with Block sample

## Post-merge validation (main)

After PR #2 merge (`95d452d` on `main`):

- **Deploy commit:** `119be82d` on Hub
- **Run id:** `20260524-091303-98869780`
- **Mode:** hosted CPU fallback (`Local CPU Preview`)
- **Artifacts:** GLB + OBJ returned via `/generate`

## Deploy context

| Step | Result |
|------|--------|
| HF CLI auth | `th3w1zard1` |
| Staged payload upload | `PYTHONPATH=src python scripts/hf_space_sync.py --execute` |
| Hub commit | `3ad22d80e91709a5f736185e77e2390802841dfc` |
| Space startup fix (GitHub) | `e2f0708` — module-level `demo`, Space default port 7860 |

## Runtime honesty

- **Not** hosted ZeroGPU validation — execution used `cpu-demo` on Space with explicit fallback messaging in status output.
- CI upload success alone does not satisfy this record; live generation was required per `AGENTS.md`.

## Source basis

- `[UI]` Live Space load and runtime chips (2026-05-24)
- `[REPO]` `gradio_client` `/generate` response on hosted Space
- `[REPO]` Deploy via `scripts/hf_space_sync.py`, port fix in `app.py` / `config.py`
