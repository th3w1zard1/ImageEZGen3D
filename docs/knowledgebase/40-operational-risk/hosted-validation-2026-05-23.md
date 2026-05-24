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
