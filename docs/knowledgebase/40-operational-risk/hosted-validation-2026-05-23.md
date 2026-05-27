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

## Plan 055 validation (backend rail chips + PR #36 on main)

After PR #36 merge (`36c0215`) and Plan 055 UX slice (2026-05-27):

- **UX:** Create Project Rail shows **What backend ran** chips (adapter label + fallback when active)
- **PR #36:** Plan 054 ship docs on `main`
- **Hosted golden smoke:** run `20260527-155208-a799d73f` (cpu-demo; balanced Block)
- **Admission:** G1–G5 PASS; G7 OPEN; Hunyuan **not** enabled

## Plan 054 validation (PR #35 merge to main)

After squash-merge PR #35 (`0037bb3` on `main`, 2026-05-27):

- **Merge:** Plan 053 G5 resource fit + G1 `hunyuan_g1_legal_verify.py` in CI; lint fix included
- **Admission audit:** G1–G5 PASS; G7 OPEN; `adapter_configured=False`
- **Hosted golden smoke:** run `20260527-154451-fb0a5893` (cpu-demo / Local CPU Preview; balanced Block)
- **Mode:** hosted CPU fallback; Hunyuan **not** enabled

## Plan 053 validation (Hunyuan G5 resource fit)

After Plan 053 on `main` (2026-05-25):

- **G5:** `hunyuan-resource-fit.md` — upstream 29 GB full pipeline, 14.9 GB Hub weights; `G5_STATUS: PASS`
- **G1 automation:** `scripts/hunyuan_g1_legal_verify.py` passes in CI (pinned LICENSE clauses)
- **Admission:** G1–G5 PASS; G6–G7 OPEN; adapter **not** enabled
- **Hosted golden smoke:** run `20260527-153748-6a1fc854` (cpu-demo / Local CPU Preview; balanced Block)

## Plan 048 validation (PR #30 merge to main)

After squash-merge PR #30 (`f7d77cd` on `main`, 2026-05-24):

- **Merge:** Plan 047 ship docs (Plan 047 plan file + Plan 047 KB section + ideation PR #29 note)
- **Hosted golden smoke:** run `20260524-221015-2f024fec` via `hosted_golden_smoke.py` (Block / balanced; Local CPU Preview)
- **Sanity:** `unittest discover` on `main` after merge
- **Mode:** hosted CPU fallback; Hunyuan **not** enabled

## Plan 047 validation (PR #29 merge to main)

After squash-merge PR #29 (`3222161` on `main`, 2026-05-24):

- **Merge:** Plan 046 guardrail-track closure (ideation + Plan 046 plan file + Plan 046 KB section)
- **Hosted golden smoke:** run `20260524-214350-1ac73103` via `hosted_golden_smoke.py` (Block / balanced; Local CPU Preview)
- **Sanity:** `unittest discover` on `main` after merge
- **Mode:** hosted CPU fallback; Hunyuan **not** enabled

## Plan 046 validation (PR #28 merge to main)

After squash-merge PR #28 (`3d638ac` on `main`, 2026-05-24):

- **Merge:** Plan 045 ship docs (ideation + `hosted-validation` Plan 045 section + completed plan file)
- **Post-trust guardrail track:** marked complete in ideation; no Space redeploy required
- **Sanity:** `PYTHONPATH=src .venv/bin/python -m unittest discover -s tests` on `main` after merge
- **Mode:** hosted CPU fallback unchanged; Hunyuan **not** enabled

## Plan 045 validation (PR #27 merge to main)

After squash-merge PR #27 (`b2eebd2` on `main`, 2026-05-24):

- **Merge:** Hunyuan admission audit step in scheduled `hosted-golden-smoke.yml`; `--record` on audit script; `AGENTS.md` gate note
- **GitHub Actions:** `workflow_dispatch` run `26372769605` — golden smoke, export tier smoke, and **Run Hunyuan admission gate audit** all succeeded
- **Artifacts:** `hunyuan-admission-audit.json` uploaded with hosted smoke bundle
- **Post-merge local:** `hosted_export_tier_smoke.py` exit 0; `hunyuan_admission_audit.py` exit 0 (`adapter_configured=False`)
- **Mode:** hosted CPU fallback; Hunyuan **not** enabled

## Plan 043 validation (PR #25 merge to main)

After squash-merge PR #25 (`a8fdd1e` on `main`, 2026-05-24):

- **Merge:** `hunyuan-admission-audit` CI job + Plan 042 KB closure
- **CI:** PR #25 checks green including new admission audit job
- **Post-merge:** `hunyuan_admission_audit.py` exit 0; export tier smoke draft `20260524-204912-f576f641`, balanced `20260524-204915-3d2ce109`
- **Mode:** hosted CPU fallback; Hunyuan **not** enabled

## Plan 042 validation (PR #24 merge to main)

After squash-merge PR #24 (`c53f126` on `main`, 2026-05-24):

- **Merge:** Hunyuan admission audit CLI (`scripts/hunyuan_admission_audit.py`); adapter remains `configured=False`
- **CI:** `hunyuan-admission-audit` job in `.github/workflows/ci.yml`
- **Post-merge audit:** `hunyuan_admission_audit.py` exit 0 — G9 pass (disabled), G1–G5/G7 open
- **Post-merge smoke:** `hosted_golden_smoke.py` run `20260524-204536-dedc5b0e`; `hosted_export_tier_smoke.py` exit 0 (no Space redeploy; runtime unchanged)
- **Mode:** hosted CPU fallback (`cpu-demo`); Hunyuan **not** enabled

## Plan 040 validation (PR #22 merge to main)

After squash-merge PR #22 (`5df22cb` on `main`, 2026-05-24):

- **Merge:** Trimesh quadric decimation with MVP fallback; `decimation_method` in export sidecar
- **Hub deploy:** `hf_space_sync --execute` commit `b4844dbf` (includes `trimesh` + `fast-simplification` in Space requirements)
- **Post-merge smoke:** `hosted_golden_smoke.py` exit 0 — run `20260524-202920-a3f83314`
- **Export tier smoke:** `hosted_export_tier_smoke.py` exit 0 — draft `20260524-202924-512575a4`, balanced `20260524-202927-f5f15efa` with sidecar `decimation_method: quadric` check
- **Mode:** hosted CPU fallback (`cpu-demo`)

## Plan 038 validation (PR #20 merge to main)

After squash-merge PR #20 (`a33146a` on `main`, 2026-05-24):

- **Merge:** Gradio **Export sidecar** and **RAW GLB** download widgets on Create + History tabs
- **Hub deploy:** `hf_space_sync --execute` commit `ad9117f3`
- **Post-merge smoke:** `hosted_golden_smoke.py` exit 0 — run `20260524-195421-f1926aec`
- **Export tier smoke:** `hosted_export_tier_smoke.py` exit 0 — draft `20260524-195431-bf8499b4`, balanced `20260524-195434-1143b336`
- **Browser:** live Space Create tab shows **EXPORT SIDECAR** and **RAW GLB** labels (`{public}`)
- **Mode:** hosted CPU fallback (`cpu-demo`)

## Plan 036 validation (PR #19 merge to main)

After squash-merge PR #19 (`39e9e47` on `main`, 2026-05-24):

- **Merge:** Hosted export tier smoke via manifest validation (draft + balanced)
- **Post-merge smoke:** `hosted_export_tier_smoke.py` exit 0
- **Run ids:** draft `20260524-193238-5b2e4dc9`, balanced `20260524-193241-e53c7089` (manifest confirms `export_sidecar`, balanced `raw_glb` + decimation flags)
- **GitHub Actions:** workflow_dispatch `26370717326` (hosted golden + export tier steps)
- **Mode:** hosted CPU fallback

## Plan 034 validation (PR #18 merge to main)

After squash-merge PR #18 (`bac08f5` on `main`, 2026-05-24):

- **Merge:** Mesh decimation post-process + `{stem}.raw.glb` for balanced/high CPU demo
- **Hub deploy:** `hf_space_sync --execute` commit `5570f748`
- **Hosted draft smoke:** `hosted_golden_smoke.py` exit 0 — run `20260524-191908-d5c06190`
- **Hosted balanced generate:** run `20260524-191912-86cf0afe` — status shows **Export budget** 150,000 faces
- **Local attestation:** `golden_sample_attestation.py` exit 0; CI balanced integration test verifies `raw_glb` + `decimation_applied` in sidecar
- **Mode:** hosted CPU fallback (`cpu-demo`)

## Plan 032 validation (PR #17 merge to main)

After squash-merge PR #17 (`b04f55f` on `main`, 2026-05-24):

- **Merge:** Hosted golden smoke workflow + `hosted_golden_smoke` module
- **Post-merge smoke:** `scripts/hosted_golden_smoke.py` exit 0
- **Hosted run id:** `20260524-185656-88b04dad` (Block, draft, seed 42)
- **GitHub Actions:** first `workflow_dispatch` run `26369938085`
- **Mode:** hosted CPU fallback (`Local CPU Preview` / `cpu-demo`)

## Plan 031 validation (hosted golden smoke CI)

Branch preflight before merge (2026-05-24):

- **Workflow:** `.github/workflows/hosted-golden-smoke.yml` — daily schedule + `workflow_dispatch`
- **Script:** `scripts/hosted_golden_smoke.py` — Block `/generate` with export budget + adapter checks
- **Local preflight run id:** `20260524-184625-ef5add6e` (draft, seed 42, cpu-demo fallback)
- **Mode:** hosted CPU fallback; complements local `golden-sample` CI job (P12)

## Plan 030 validation (PR #16 merge to main)

After squash-merge PR #16 (`04ba9bf` on `main`, 2026-05-24):

- **Merge:** Quality-tier decimation presets + per-run `export_sidecar` JSON; golden attestation requires sidecar
- **Post-merge local:** `golden_sample_attestation.py` exit 0 with `export_sidecar_bytes` present
- **Hub deploy:** post-merge `hf_space_sync --execute` commit `25ee4bfe`
- **Hosted run id:** `20260524-184255-f0ce0436` (Block, draft, seed 42)
- **Mode:** hosted CPU fallback (`cpu-demo`)
- **Status markdown:** includes **Export budget** up to 25,000 faces
- **Artifacts verified:** manifest ☑ GLB ☑ OBJ ☑ (export sidecar on new runs via API path)

## Plan 028 validation (PR #15 merge to main)

After squash-merge PR #15 (`3228f59` on `main`, 2026-05-24):

- **Merge:** History compare manifest export (JSON + MD downloads, `compare_runs_payload`)
- **Post-merge smoke:** `hosted_history_compare_smoke.py` exit 0 with JSON export field checks
- **Run ids:** `20260524-183056-5bd10391` vs `20260524-183054-82b997e5`
- **Hub deploy:** post-merge `hf_space_sync --execute` (2026-05-24)
- **Browser:** History tab shows **Compare diff (JSON)** and **Compare report (MD)**

## Plan 026 validation (PR #14 merge to main)

After squash-merge PR #14 (`76fa267` on `main`, 2026-05-24):

- **Merge:** History compare MVP + hosted smoke script + Gradio API names on `main`
- **CI:** style guard + ruff + tests 3.10–3.14 + golden-sample green on final PR head
- **Post-merge smoke:** `PYTHONPATH=src python scripts/hosted_history_compare_smoke.py` exit 0
- **Run ids:** `20260524-182227-6a8384e7` vs `20260524-182225-c7e62022` (Block sample, seeds 42/43)
- **Hub deploy:** post-merge `hf_space_sync --execute` (2026-05-24)

## Plan 024 validation (History compare MVP)

After PR #14 branch deploy (2026-05-24) and `scripts/hosted_history_compare_smoke.py`:

- **Run ids:** `20260524-181625-e4af8ed8` and `20260524-181623-469e4213` (Block sample `assets/examples/teal_block.png`, seeds 42 and 43 via smoke script)
- **Compare:** Gradio API `/compare_history_runs` returns `## Run comparison` markdown with backend/quality/artifact diff
- **History list:** `/history_updates` (or `_1` alias) returns ≥2 recent run labels after generates
- **Mode:** hosted CPU fallback (`cpu-demo`)
- **Browser:** History tab shows **Compare Runs** control on live Space
- **Evidence:** `PYTHONPATH=src python scripts/hosted_history_compare_smoke.py` exit 0

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
