# Hunyuan G9 enablement runbook

Gate **G9** closes when an explicit enablement PR merges with rollback steps documented. Until then, the disabled-adapter guard in admission audit may show G9 as passing only because `configured=False`.

## Pre-flight (required)

**One command (preferred):**

```bash
python scripts/hunyuan_preflight_bundle.py
```

**Tier-C workstation (after admission preflight passes):**

```bash
PYTHONPATH=src python scripts/hunyuan_neural_enablement_preflight_bundle.py --record-dir .
PYTHONPATH=src python scripts/hunyuan_neural_enablement_preflight_bundle.py --record-dir . --strict
PYTHONPATH=src python scripts/verify_neural_enablement_record.py neural-enablement-preflight.json
PYTHONPATH=src python scripts/verify_neural_enablement_artifact_parity.py --record-dir .
```

Writes admission, enablement, workstation, G9 bundle, and neural enablement JSON under `--record-dir` and verifies record + cross-artifact parity (neural ↔ G9 ↔ enablement). When `hunyuan-g7-live-probe.json` is also present (from `--live-probe`), parity verify includes live-probe ↔ neural `g7_readiness` alignment. Expect `workstation_evidence_ready=false` and `neural_enablement_ready=false` on CI; on tier-C GPU workstation re-run with `--strict` until `ok=true` in `neural-enablement-preflight.json`.

**Legacy G9-only bundle (subset of the neural capstone):**

```bash
PYTHONPATH=src python scripts/hunyuan_g9_preflight_bundle.py --record-dir . --strict
```

**Individual steps (same contract):**

```bash
PYTHONPATH=src python scripts/hunyuan_enablement_preflight.py \
  --record hunyuan-enablement-preflight.json
PYTHONPATH=src python scripts/hunyuan_admission_audit.py \
  --record hunyuan-admission-audit.json
PYTHONPATH=src python scripts/verify_hunyuan_ci_artifact_parity.py \
  hunyuan-admission-audit.json hunyuan-enablement-preflight.json
```

Expect `prerequisites_met=True` and `blocking_enablement` listing **G7** (and **G8** post-enablement section) until hosted validation sections are updated. The verify script must exit 0 before enablement work proceeds.

After hosted smoke on Space, verify scheduled-style artifacts locally when debugging:

```bash
PYTHONPATH=src python scripts/verify_hosted_golden_smoke_record.py hosted-golden-smoke.json
PYTHONPATH=src python scripts/verify_hosted_export_tier_smoke_record.py hosted-export-tier-smoke.json
PYTHONPATH=src python scripts/verify_hunyuan_g7_live_probe_record.py hunyuan-g7-live-probe.json
PYTHONPATH=src python scripts/verify_hosted_smoke_artifacts.py
```

## Enablement PR checklist

1. Set `HunyuanPlaceholderAdapter.capabilities.configured = True` in the same PR that closes G7–G8 with evidence.
2. Wire weights/secrets per [hunyuan-weight-access.md](hunyuan-weight-access.md) and [hunyuan-dependencies.md](hunyuan-dependencies.md).
3. Deploy Space: `PYTHONPATH=src python scripts/hf_space_sync.py --execute`
4. Run Block or Vase `/generate`; status must pass `validate_g7_hosted_generate_status()`.
5. Update [hosted-validation-2026-05-23.md](40-operational-risk/hosted-validation-2026-05-23.md):
   - `## G7 validation` → `G7_STATUS: PASS` + run id + artifacts
   - `## G8 validation` → `G8_STATUS: PASS` after UX re-verify
6. Re-run hosted golden smoke and admission audit; upload artifacts from CI if applicable.

## Rollback

1. Set `configured=False` (revert enablement PR or hotfix).
2. Redeploy Space so Gradio adapter choices return to `auto` + cpu-demo only.
3. Run `hosted_golden_smoke.py` and confirm cpu-demo fallback honesty (G8 interim checks).
4. Record rollback run id in hosted-validation under a new plan section.

## Related docs

- [hunyuan-admission-gates.md](hunyuan-admission-gates.md)
- [hunyuan-enablement-preflight.md](hunyuan-enablement-preflight.md)
- [hunyuan-g7-preflight.md](hunyuan-g7-preflight.md)
