# Hunyuan manifest parity (G6)

**Status:** Sample manifest attached for enablement prep. Adapter remains **NOT ENABLED**.

## G6_STATUS: PASS (sample contract)

This record closes **G6 prep** only: the repository includes a representative Hunyuan manifest that satisfies the same trust fields as the validated cpu-demo path (adapter, quality, decimation, runtime, export_sidecar, GLB/OBJ).

It does **not** claim a live Hunyuan reconstruction run (see **G7**).

## Sample artifact

| Item | Location |
| --- | --- |
| JSON sample | `tests/fixtures/hunyuan-zerogpu-manifest.sample.json` |
| Validator | `src/imageezgen3d/hunyuan_manifest_parity.py` — `validate_hunyuan_manifest_parity()` |
| CI | `tests/test_hunyuan_manifest_parity.py` |

## Pass criteria (repo)

- Sample validates with zero issues via `validate_hunyuan_manifest_parity()`
- `selected_adapter` and top-level `adapter` are `hunyuan-zerogpu`
- No `fallback_reason` or `preview_disclaimer` on the neural-path sample
- Artifacts include `manifest`, `glb`, `obj`, `export_sidecar` (balanced tier also lists `raw_glb`)

## Not claimed

- Real weights loaded on Space
- Hosted E2E with neural path (G7)
- `HunyuanPlaceholderAdapter.configured=True`

## Evidence

- `[REPO]` Admission audit reads this doc + sample file for G6
- `[SYNTH]` Sample paths are placeholders; replace with real run artifacts in the enablement PR
