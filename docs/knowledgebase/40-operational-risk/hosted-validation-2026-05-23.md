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

## G7 validation

**G7_STATUS: OPEN**

Placeholder for the first live Space run on the real Hunyuan ZeroGPU adapter path (not cpu-demo / Local CPU Preview fallback).

When closing this gate, set `G7_STATUS: PASS` in this section only (not in plan prose) and record:

- Run id and sample (Block or Vase / `assets/examples/teal_block.png`)
- Status passes `validate_g7_hosted_generate_status()` from `hunyuan_g7_preflight.py`
- Manifest, GLB, and OBJ artifacts verified

## G8 validation

**G8_STATUS: OPEN** (post-enablement re-verify)

Interim CPU fallback honesty is enforced on every hosted golden smoke run via `validate_g8_cpu_fallback_status()`. After Hunyuan enablement, add `G8_STATUS: PASS` here following [hunyuan-g8-preflight.md](../hunyuan-g8-preflight.md).

## Plan 012 validation (fallback honesty UI)

After PR #4 merge (`e3dec36` on `main`) and deploy commit `51bf9f293724b3ab32d85906082f032e15b1d68b`:

- **Run id:** `20260524-095746-972cc9ea`
- **Mode:** hosted CPU fallback (`Local CPU Preview` / `cpu-demo`)
- **Fallback reason:** ZeroGPU runtime present; configured ZeroGPU model adapter not enabled yet
- **Preview disclaimer:** present in status markdown and manifest `preview_disclaimer`
- **Artifacts verified:** manifest ☑ (2589 bytes) GLB ☑ (12144 bytes) OBJ ☑ (369 bytes)
- **Evidence:** Gradio API `/generate` with Block sample (`assets/examples/teal_block.png`)

## Plan 114 validation (PR #73 merged to main)

After Plan 114 (2026-05-28):

- **Merge:** squash `2c425d1` on `main` — PR #73 (Plan 113 G7 readiness handoff)
- **On main:** G7 entry doc + admission sync; G7 neural E2E still **OPEN**

## Plan 113 validation (G7 enablement readiness handoff)

After Plan 113 (2026-05-28):

- **Solutions:** [g7-enablement-readiness-2026-05-28.md](../../solutions/best-practices/g7-enablement-readiness-2026-05-28.md) — indexes guard stack + live attestation complete; G7/G8/G9 still **OPEN**
- **Hygiene:** `.gitignore` excludes local `hunyuan-*-preflight.json` / audit JSON from accidental commits
- **G7 gate:** still **OPEN** — no `configured=True`, no neural E2E claim

## Plan 112 validation (PR #72 merged to main)

After Plan 112 (2026-05-28):

- **Merge:** squash `f1188a6` on `main` — PR #72 (Plan 111 hosted live attestation closure)
- **On main:** trilogy solutions doc + STRATEGY/roadmap sync; Plans 107–111 attestation indexed; G7 neural E2E still **OPEN**

## Plan 111 validation (hosted live attestation closure)

After Plan 111 (2026-05-28):

- **Solutions:** [hosted-live-attestation-2026-05-28.md](../../solutions/best-practices/hosted-live-attestation-2026-05-28.md) indexes Plans 107–110 run ids and mode labels.
- **STRATEGY/roadmap:** guard stack + live attestation on `main`; G7 neural E2E still **OPEN**.

## Plan 110 validation (PR #71 merged to main)

After Plan 110 (2026-05-28):

- **Merge:** squash `3777259` on `main` — PR #71 (Plan 109 export-tier + G7 live probe attestation)
- **On main:** Plans 107–109 live attestation complete (golden, export-tier, G7 probe); G7 still **OPEN**

## Plan 109 validation (export-tier smoke + G7 live probe attestation)

After Plan 109 (2026-05-28):

- **Mode:** hosted CPU fallback for export-tier draft + balanced runs
- **Export-tier run ids:** `20260528-025824-1345fc91` (draft), `20260528-025828-ef91630a` (balanced)
- **Adapter:** Local CPU Preview; `g7_false_neural_guard_ok=true` on both checks
- **G7 live probe:** `hosted_probe.ok=true` — Space rejected `hunyuan-zerogpu` (not in choices); no false G7 neural success
- **Verify CLIs:** export-tier + G7 live-probe record verify exit 0
- **G7 gate:** still **OPEN** for real neural Hunyuan path

## Plan 108 validation (PR #70 merged to main)

After Plan 108 (2026-05-28):

- **Merge:** squash `a2e725e` on `main` — PR #70 (Plan 107 live golden smoke attestation)
- **Evidence on main:** run `20260528-024123-5bf694b9`, hosted CPU fallback, `g7_false_neural_guard_ok=true`
- **G7 gate:** still **OPEN** for real neural path

## Plan 107 validation (live hosted golden smoke attestation)

After Plan 107 (2026-05-28):

- **Mode:** hosted CPU fallback (`Local CPU Preview` / cpu-demo path)
- **Run id:** `20260528-024123-5bf694b9`
- **Sample:** Block (`assets/examples/teal_block.png`)
- **Space:** https://th3w1zard1-imageezgen3d.hf.space/
- **Smoke:** `hosted_golden_smoke.py` exit 0; `verify_hosted_golden_smoke_record.py` exit 0
- **`g7_false_neural_guard_ok`:** true (no false G7 neural claim while adapter disabled)
- **G7 gate:** still **OPEN** for real Hunyuan neural path — this attestation is fallback honesty only

## Plan 106 validation (PR #69 merged to main)

After Plan 106 (2026-05-28):

- **Merge:** squash `82b8730` on `main` — PR #69 (Plan 105 KB index guard stack refresh)
- **On main:** KB index links guard stack, G7 preflight, enablement runbook; G7 still **OPEN**

## Plan 105 validation (KB index guard stack refresh)

After Plan 105 (2026-05-28):

- **KB index:** `docs/knowledgebase/README.md` links guard stack, G7 preflight, enablement runbook, P14 caveat.

## Plan 104 validation (PR #68 merged to main)

After Plan 104 (2026-05-28):

- **Merge:** squash `e84fdb5` on `main` — PR #68 (Plan 103 admission + parity sync)
- **On main:** admission gates through Plan 102; parity **P14** hosted smoke guard stack
- **G7 gate:** still **OPEN** for real neural path

## Plan 103 validation (admission + parity sync)

After Plan 103 (2026-05-28):

- **Admission gates:** last-audit footer through Plan 102; links guard stack solutions doc.
- **Parity:** P14 row for hosted smoke guard stack; P13 last-verified refreshed.

## Plan 102 validation (PR #67 merged to main)

After Plan 102 (2026-05-28):

- **Merge:** squash `6dc3730` on `main` — PR #67 (Plan 101 hosted smoke guard stack closure)
- **On main:** [hosted-smoke-guard-stack-2026-05-28.md](../../solutions/best-practices/hosted-smoke-guard-stack-2026-05-28.md) indexes Plans 078–100 verify chain
- **G7 gate:** still **OPEN** for real neural path

## Plan 101 validation (hosted smoke guard stack closure)

After Plan 101 (2026-05-28):

- **Solutions index:** [hosted-smoke-guard-stack-2026-05-28.md](../../solutions/best-practices/hosted-smoke-guard-stack-2026-05-28.md) links Plans 078–100 guard chain.
- **Tests:** `test_verify_hosted_smoke_artifacts_cli_fails_on_invalid_golden` subprocess exit 1.

## Plan 100 validation (PR #66 merged to main)

After Plan 100 (2026-05-28):

- **Merge:** squash `b34dec8` on `main` — PR #66 (Plan 099 G7 live-probe verify learning)
- **On main:** subprocess verify test + enablement runbook lists all smoke JSON verify CLIs
- **G7 gate:** still **OPEN** for real neural path

## Plan 099 validation (G7 live probe verify learning)

After Plan 099 (2026-05-28):

- **Subprocess contract:** `tests/test_hunyuan_g7_preflight.py` exercises `verify_hunyuan_g7_live_probe_record.py` exit 0/1.
- **Runbook:** `hunyuan-g9-enablement-runbook.md` lists G7 live-probe verify with golden/export-tier smoke verifiers.

## Plan 098 validation (PR #65 merged to main)

After Plan 098 (2026-05-28):

- **Merge:** squash `6cf3871` on `main` — PR #65 (Plan 097 G7 live probe record verify)
- **CI on main:** scheduled smoke validates `hunyuan-g7-live-probe.json` via `verify_hunyuan_g7_live_probe_record.py`
- **G7 gate:** still **OPEN** for real neural path — verify proves schema/honesty, not Hunyuan E2E

## Plan 097 validation (G7 live probe learning + record verify)

After Plan 097 (2026-05-28):

- **Solutions:** [hunyuan-g7-live-probe-scheduled-smoke-2026-05-28.md](../../solutions/best-practices/hunyuan-g7-live-probe-scheduled-smoke-2026-05-28.md)
- **CI:** `verify_hunyuan_g7_live_probe_record.py` after `--record hunyuan-g7-live-probe.json`

## Plan 096 validation (PR #64 merged to main)

After Plan 096 (2026-05-28):

- **Merge:** squash `f45b8cb` on `main` — PR #64 (Plan 095 G7 live probe)
- **Live probe on main:** Space rejects `hunyuan-zerogpu` adapter choice (not in Gradio list); `hosted_probe.ok=true`
- **G7 gate:** still **OPEN** for real neural path — probe proves honesty while disabled, not neural E2E

## Plan 095 validation (G7 live probe in scheduled smoke)

After Plan 095 (2026-05-28):

- **Scheduled smoke:** `hunyuan_g7_preflight.py --live-probe --record hunyuan-g7-live-probe.json`
- **Bundle verify:** `verify_hosted_smoke_artifacts.py` checks golden + export-tier records
- **G7 gate:** still **OPEN** for real neural Hunyuan path — live probe proves no *false* G7 success while disabled

## Plan 094 validation (PR #63 merged to main)

After Plan 094 (2026-05-28):

- **Merge:** squash `60c510b` on `main` — PR #63 (Plan 093 export-tier verify learning)
- **Smoke guard stack on `main`:** G7 false-neural guard + golden/export-tier JSON verify + solutions index
- **G7 gate:** still **OPEN** for real Hunyuan path

## Plan 093 validation (export-tier verify learning)

After Plan 093 (2026-05-28):

- **Solutions:** [hosted-export-tier-smoke-record-verify-2026-05-28.md](../../solutions/best-practices/hosted-export-tier-smoke-record-verify-2026-05-28.md)
- **AGENTS.md** + G9 runbook reference both smoke verify CLIs

## Plan 092 validation (PR #62 merged to main)

After Plan 092 (2026-05-28):

- **Merge:** squash `bc869c8` on `main` — PR #62 (Plan 091 export-tier record verifier)
- **Verify CLI:** `verify_hosted_export_tier_smoke_record.py` exits 0 on valid draft+balanced `checks[]`
- **G7 gate:** still **OPEN** for real Hunyuan path

## Plan 091 validation (export tier smoke record verify)

After Plan 091 (2026-05-28):

- **`verify_hosted_export_tier_smoke_record.py`:** validates `checks[]` (draft + balanced) including `g7_false_neural_guard_ok` per entry
- **Plans 066–069** frontmatter marked `completed`

## Plan 090 validation (PR #61 merged to main)

After Plan 090 (2026-05-28):

- **Merge:** squash `c97e07f` on `main` — PR #61 (Plan 089 institutional learning)
- **Solutions:** [hosted-golden-smoke-record-verify-2026-05-28.md](../../solutions/best-practices/hosted-golden-smoke-record-verify-2026-05-28.md) on `main`
- **G7 gate:** still **OPEN** for real Hunyuan path; cpu-demo smoke verified with verify CLI

## Plan 089 validation (smoke record verify learning)

After Plan 089 (2026-05-28):

- **Solutions:** [hosted-golden-smoke-record-verify-2026-05-28.md](../../solutions/best-practices/hosted-golden-smoke-record-verify-2026-05-28.md)
- **AGENTS.md** references verify CLI after `--record`
- **Tests:** subprocess verify CLI exit 0/1 on valid vs incomplete JSON

## Plan 088 validation (PR #60 merged to main)

After Plan 088 (2026-05-28):

- **Merge:** squash `54840ea` on `main` — PR #60 (Plan 087 smoke record verifier)
- **Verify CLI:** `verify_hosted_golden_smoke_record.py` exits 0 on live `--record` output
- **G7 gate:** still **OPEN** for real Hunyuan path; cpu-demo smoke keeps `g7_false_neural_guard_ok=true`

## Plan 087 validation (hosted golden smoke record verify)

After Plan 087 (2026-05-28):

- **`verify_hosted_golden_smoke_record.py`:** fails scheduled smoke when `hosted-golden-smoke.json` lacks `g7_false_neural_guard_ok` or has wrong types
- **Plans 070–073** frontmatter marked `completed` (KB validation already on `main`)

## Plan 086 validation (PR #59 merged to main)

After Plan 086 (2026-05-28):

- **Merge:** squash `373e779` on `main` — PR #59 (Plans 078–086)
- **Workflow contract:** `hosted-golden-smoke.yml` runs `hosted_golden_smoke.py --json` and uploads `hosted-golden-smoke.json`
- **G7 gate:** still **OPEN** for real Hunyuan ZeroGPU path; cpu-demo smoke must keep `g7_false_neural_guard_ok=true` without neural status markers

## Plan 085 validation (close PR 58, ship via PR 59)

After Plan 085 (2026-05-28):

- **PR #58** closed as superseded by **PR #59** (stacked branch includes Plans 078–084)
- **CLI test:** `hosted_golden_smoke.py --json` emits `g7_false_neural_guard_ok`

## Plan 084 validation (stack PR 59 on PR 58)

After Plan 084 (2026-05-28):

- **`feat/080-g7-golden-smoke-guard`** rebased onto `feat/078-ship-pr57-kb-closure` — unified hosted-validation (Plans 078–082)
- Merge **PR #59** only after closing or superseding **PR #58** (same commits now stacked)

## Plan 083 validation (PR #58 rebase readiness)

After Plan 083 (2026-05-28):

- **`feat/078-ship-pr57-kb-closure`** rebased cleanly on `origin/main` (Plans 078–079 only)
- **`tests.test_workflows`** pass on rebased branch

## Plan 082 validation (G7 guard field in smoke JSON)

After Plan 082 (2026-05-28):

- **`hosted-golden-smoke.json`:** includes `g7_false_neural_guard_ok` for scheduled artifact review
- **Hosted golden smoke:** run `20260528-002617-1204154d` (cpu-demo; `g7_false_neural_guard_ok=True`)

## Plan 081 validation (G7 guard institutional learning)

After Plan 081 (2026-05-28):

- **Solutions:** [g7-false-neural-golden-smoke-guard-2026-05-28.md](../../solutions/best-practices/g7-false-neural-golden-smoke-guard-2026-05-28.md)
- **AGENTS.md** points agents to the learning before changing smoke/G7 validators
- **Hosted golden smoke:** run `20260528-001645-8268f2b3` (cpu-demo / Local CPU Preview)

## Plan 080 validation (G7 false-neural golden smoke guard)

After Plan 080 (2026-05-28):

- **`validate_g7_not_false_neural_claim`** in `hosted_golden_smoke.py` — fails smoke when status looks like G7 neural success while adapter disabled
- **Hosted golden smoke:** run `20260528-001022-151788f4` (cpu-demo / Local CPU Preview)

## Plan 079 validation (CI vs smoke bundle flags)

After Plan 079 (2026-05-27):

- **`test_workflows`:** `ci.yml` bundle without `--json`; hosted-golden-smoke with `--json`
- **Hosted golden smoke:** run `20260528-000007-f209b6bc` (cpu-demo / Local CPU Preview)

## Plan 078 validation (PR #57 ship closure)

After PR #57 merge to `main` (2026-05-27, commit `5a7483b`):

- **Shipped:** Plans 074–077 — `hunyuan_preflight_bundle.py` in `ci.yml` and `hosted-golden-smoke.yml`, lint fixes, bundle-first docs, CI bundle subprocess test
- **Current workflow contract:** one bundle step (+ separate G7 preflight); verify runs inside the bundle
- **Hosted golden smoke:** run `20260527-235413-d8839ca1` (cpu-demo / Local CPU Preview; post-merge `main`)

## Plan 077 validation (bundle-first admission docs)

After Plan 077 on branch `feat/075-ci-workflows-use-preflight-bundle` (2026-05-27):

- **Admission gates doc:** bundle-first audit commands
- **CI scripts test:** subprocess coverage for `hunyuan_preflight_bundle.py`
- **Hosted golden smoke:** run `20260527-215147-a4d3b052` (cpu-demo / Local CPU Preview)

## Plan 076 validation (lint + bundle docs)

After Plan 076 on branch `feat/075-ci-workflows-use-preflight-bundle` (2026-05-27):

- **Ruff:** removed unused `sys` from Hunyuan preflight scripts (unblocks PR #57 lint)
- **Hosted golden smoke:** run `20260527-214844-3c7de80b` (cpu-demo / Local CPU Preview)

## Plan 075 validation (CI workflows use preflight bundle)

After Plan 075 on `main` (2026-05-27):

- **`ci.yml` / `hosted-golden-smoke`:** Hunyuan JSON + verify via `hunyuan_preflight_bundle.py` (scheduled smoke uses `--json`)
- **G7 preflight** remains a separate step after the bundle
- **Hosted golden smoke:** run `20260527-214055-500a0ffb` (cpu-demo / Local CPU Preview; balanced Block)

## Plan 074 validation (Hunyuan preflight bundle CLI)

After Plan 074 on `main` (2026-05-27):

- **Bundle CLI:** `scripts/hunyuan_preflight_bundle.py` — audit + enablement `--record` + verify in one step
- **Agents:** `AGENTS.md` and G9 runbook prefer the bundle for pre-enablement checks

## Plan 073 validation (Hunyuan CI parity institutional learning)

After Plan 073 on `main` (2026-05-27):

- **Solutions:** [hunyuan-ci-artifact-parity-2026-05-27.md](../../solutions/best-practices/hunyuan-ci-artifact-parity-2026-05-27.md)
- **G9 runbook:** preflight includes parity verify (via bundle since PR #57)
- **Tests:** `test_hunyuan_ci_scripts` covers legacy three-step and bundle subprocess paths

## Plan 072 validation (CI artifact verify script)

After Plan 072 on `main` (2026-05-27):

- **Verify script:** `scripts/verify_hunyuan_ci_artifact_parity.py` (invoked by `hunyuan_preflight_bundle.py` in CI since PR #57)
- **Fails CI** when `hunyuan-admission-audit.json` and `hunyuan-enablement-preflight.json` disagree on G7/G8

## Plan 071 validation (G8 gates helper + CI scripts contract)

After Plan 071 on `main` (2026-05-27):

- **`g8_enablement_for_gates()`** shared by admission audit builder and enablement preflight
- **`tests/test_hunyuan_ci_scripts.py`:** subprocess `--record` parity for scheduled smoke artifacts

## Plan 070 validation (centralized admission audit payload)

After Plan 070 on `main` (2026-05-27):

- **`hunyuan_admission_audit.py`:** `build_admission_audit_payload()` — single source for `hunyuan-admission-audit.json`
- **Parity tests** import the builder instead of duplicating G8 assembly logic

## Plan 069 validation (hosted doc paths + CI artifact parity)

After Plan 069 on `main` (2026-05-27):

- **`hosted_validation.py`:** `HOSTED_VALIDATION_PATH` + `read_repo_text()` (no private admission imports from enablement preflight)
- **Parity test:** `test_hunyuan_ci_artifact_parity.py` locks admission audit vs enablement preflight G7/G8 snapshots

## Plan 068 validation (enablement JSON parity + hosted section helper)

After Plan 068 on `main` (2026-05-27):

- **`hosted_validation.py`:** shared `hosted_validation_section()` for G7/G8 admission checks
- **`hunyuan-enablement-preflight.json`:** nested `g7_readiness` and `g8_enablement` objects (booleans retained)

## Plan 067 validation (G8 artifact visibility)

After Plan 067 on `main` (2026-05-27):

- **Enablement preflight:** text report includes `g8_enablement_documented=`
- **Admission audit JSON:** `g8_enablement` block mirrors structured G8 section state (`interim_open` while `G8_STATUS: OPEN`)

## Plan 066 validation (G8 admission gate section alignment)

After Plan 066 on `main` (2026-05-27):

- **G8 admission:** `g8_status` uses `g8_enablement_validation_passed()` on `## G8 validation` only; `G8_STATUS: OPEN` does not close the gate
- **Interim honesty:** `validate_g8_cpu_fallback_status()` still runs on every hosted golden smoke (unchanged)
- **AGENTS.md:** links [hunyuan-g9-enablement-runbook.md](../hunyuan-g9-enablement-runbook.md)

## Plan 065 validation (G7/G8 validation placeholders + G9 runbook)

After Plan 065 on `main` (2026-05-27):

- **G7/G8 sections:** dedicated `## G7 validation` / `## G8 validation` placeholders (`G7_STATUS: OPEN`)
- **G9 runbook:** [hunyuan-g9-enablement-runbook.md](../hunyuan-g9-enablement-runbook.md)
- **PR #46:** scheduled enablement preflight artifact merged (`651ced8`)

## Plan 064 validation (enablement preflight on scheduled smoke)

After Plan 064 on `main` (2026-05-27):

- **Scheduled smoke:** `hosted-golden-smoke` uploads `hunyuan-enablement-preflight.json`
- **PR #45:** enablement preflight CLI merged (`5ca053f`)
- **Hosted golden smoke:** run `20260527-163833-108886a7`
- **G7:** still **OPEN**

## Plan 063 validation (unified enablement preflight)

After Plan 063 on `main` (2026-05-27):

- **CLI:** `hunyuan_enablement_preflight.py` — G1–G9 snapshot; exit 1 if G1–G6 regress or adapter enabled with open G7–G9
- **PR #44:** G8 golden smoke checks merged (`2c03a2b`)
- **Hosted golden smoke:** run `20260527-163628-0b5ca207` (G8 honesty ok)
- **G7:** **OPEN** (neural hosted E2E); G8/G9 scaffold pass while disabled

## Plan 062 validation (G8 fallback honesty in hosted golden smoke)

After Plan 062 on `main` (2026-05-27):

- **G8:** `validate_g8_cpu_fallback_status()` wired into `hosted_golden_smoke.py`
- **PR #43:** G7 preflight CI merged (`bf8fa29`)
- **Hosted golden smoke:** run `20260527-162855-2ad20d9d` (G8 honesty checks ok)
- **Mode:** hosted CPU fallback; Hunyuan **not** enabled

## Plan 061 validation (G7 preflight in PR CI)

After Plan 061 on `main` (2026-05-27):

- **CI:** `ci.yml` `hunyuan-admission-audit` runs `hunyuan_g7_preflight.py`; audit JSON includes `g7_readiness`
- **G7 gate:** closes only when a `## G7 validation` section records `G7_STATUS: PASS` (still **OPEN**)
- **PR #42:** G7 preflight harness merged (`3db080f`)

## Plan 060 validation (G7 preflight harness + PR #41 merge)

After Plan 060 on `main` (2026-05-27):

- **G7 preflight:** `hunyuan-g7-preflight.md` — G1–G6 readiness CLI; G7 still **OPEN**
- **PR #41:** G6 sample manifest merged (`25a5583`)
- **CI:** `hosted-golden-smoke` workflow runs `hunyuan_g7_preflight.py`
- **Adapter:** Hunyuan **not** enabled

## Plan 059 validation (G6 manifest sample + PR #40 deploy)

After Plan 059 on `main` (2026-05-27):

- **G6:** `hunyuan-manifest-parity.md` + `tests/fixtures/hunyuan-zerogpu-manifest.sample.json`; admission audit G6 **PASS** (sample contract only)
- **PR #40:** History tab idle backend rail merged (`5f336b9`); Space deploy `73836dd`
- **Hosted golden smoke:** run `20260527-161046-de25d276` (cpu-demo; rail HTML ok)
- **Adapter:** Hunyuan **not** enabled; G7 hosted neural E2E still **OPEN**

## Plan 058 validation (History tab idle backend rail parity)

After Plan 058 on `main` (2026-05-27):

- **UX:** History tab Project Rail shows **What backend ran** chips before first run (same `resolution` path as Create tab)
- **PR #39:** Plan 057 golden smoke rail assertion merged (`1bd46e1`)
- **Hosted golden smoke:** run `20260527-160601-b822c87f` (rail HTML check ok)
- **G7:** still OPEN; Hunyuan **not** enabled

## Plan 057 validation (hosted golden smoke backend rail assertion)

After Plan 057 on `main` (2026-05-27):

- **Automation:** `hosted_golden_smoke` validates `/generate` output index 15 (`create_history_summary`) for **What backend ran** chips
- **Mode:** hosted CPU fallback; Hunyuan **not** enabled
- **G7:** still OPEN (real Hunyuan hosted E2E deferred)

## Plan 056 validation (PR #37 merge + Space deploy)

After squash-merge PR #37 (`f41d22c` on `main`, 2026-05-27) and Hub deploy `9ad3eb7436901c5e11de4f57ed2c75aeca92d6d8`:

- **UX:** Live Create tab shows **What backend ran** region (`aria-label="Active backend"`) in Project Rail
- **Hosted golden smoke:** run `20260527-155624-a8e9d1a9` (cpu-demo / Local CPU Preview; balanced Block)
- **Mode:** hosted CPU fallback; Hunyuan **not** enabled

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
