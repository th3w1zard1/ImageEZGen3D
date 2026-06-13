# Hunyuan G9 enablement runbook

Gate **G9** closes when an explicit enablement PR merges with rollback steps documented. Until then, the disabled-adapter guard in admission audit may show G9 as passing only because `configured=False`.

## Pre-flight (required)

**One command (preferred — includes admission audit, enablement preflight, and capstone run+verify):**

```bash
PYTHONPATH=src python scripts/hunyuan_enablement_evidence_capstones.py --record-dir .
PYTHONPATH=src python scripts/hunyuan_enablement_evidence_capstones.py --record-dir . --strict
PYTHONPATH=src python scripts/hunyuan_enablement_evidence_capstones.py --record-dir . --strict --require-hosted-neural --hosted-neural --status-file status.md --hosted-sample Block
```

**Admission audit subset only (included in capstones preflight via admission capstone):**

```bash
python scripts/hunyuan_preflight_bundle.py
```

**Run and verify separately (subset debugging):**

```bash
PYTHONPATH=src python scripts/hunyuan_admission_g9_enablement_evidence_bundle.py --record-dir .
PYTHONPATH=src python scripts/hunyuan_admission_g9_enablement_evidence_bundle.py --record-dir . --strict
PYTHONPATH=src python scripts/hunyuan_admission_g9_enablement_evidence_bundle.py --record-dir . --strict --require-hosted-neural --hosted-neural --status-file status.md --hosted-sample Block
PYTHONPATH=src python scripts/verify_enablement_evidence_capstones.py --record-dir .
```

**Per-capstone verify (subset debugging):**

```bash
PYTHONPATH=src python scripts/verify_admission_g9_enablement_evidence_bundle.py --record-dir .
PYTHONPATH=src python scripts/verify_g9_enablement_evidence_bundle.py --record-dir .
PYTHONPATH=src python scripts/verify_neural_enablement_preflight_bundle.py --record-dir .
```

**G9 evidence capstone only (subset of admission + evidence bundle):**

```bash
PYTHONPATH=src python scripts/hunyuan_g9_enablement_evidence_bundle.py --record-dir .
PYTHONPATH=src python scripts/hunyuan_g9_enablement_evidence_bundle.py --record-dir . --strict
PYTHONPATH=src python scripts/hunyuan_g9_enablement_evidence_bundle.py --record-dir . --strict --require-hosted-neural --hosted-neural --status-file status.md --hosted-sample Block
PYTHONPATH=src python scripts/verify_g9_enablement_evidence_bundle.py --record-dir .
```

**Tier-C workstation (neural capstone subset):**

```bash
PYTHONPATH=src python scripts/hunyuan_neural_enablement_preflight_bundle.py --record-dir .
PYTHONPATH=src python scripts/hunyuan_neural_enablement_preflight_bundle.py --record-dir . --live-probe
PYTHONPATH=src python scripts/hunyuan_neural_enablement_preflight_bundle.py --record-dir . --hosted-neural --status-file status.md --hosted-sample Block
PYTHONPATH=src python scripts/hunyuan_neural_enablement_preflight_bundle.py --record-dir . --strict
PYTHONPATH=src python scripts/verify_neural_enablement_preflight_bundle.py --record-dir .
```

### Evidence field glossary

| Field | Meaning on CI / non-GPU hosts | Tier-C operator target |
| --- | --- | --- |
| `workstation_evidence_ready` | Neural workstation probe not satisfied (expected `false`) | `true` after live GPU probe |
| `neural_enablement_ready` | Adapter neural forward path not proven (expected `false`) | `true` after configured forward pass |
| `g9_enablement_evidence_ready` | Combined G9/admission capstone gate (expected `false` here) | `true` before Space enablement PR |

`--strict` on capstone scripts exits **1** when the row's CI-expected value is `false`. Do not treat `workstation_evidence_ready=false` alone as a separate blocker label — the operator-facing enablement gate is **`g9_enablement_evidence_ready=true`** plus **`parity_ok=true`** on tier-C.

The capstone bundle above writes admission, enablement, workstation, G9 bundle, neural enablement, G9 evidence (`g9-enablement-evidence.json`), admission + G9 evidence bundle (`admission-g9-enablement-evidence-bundle.json`), and (with `--live-probe`) `hunyuan-g7-live-probe.json` under `--record-dir`, then verifies record + cross-artifact parity. With `--hosted-neural --status-file`, also writes `hunyuan-g7-hosted-neural.json` for post-enablement G7 evidence parity (Phase AP). When `g9-enablement-evidence.json` is present, parity also checks G9 evidence ↔ neural alignment (Phase AS), G9 evidence ↔ admission audit alignment when `hunyuan-admission-audit.json` is present (Phase AT), and bundle nested evidence ↔ standalone G9 evidence when `admission-g9-enablement-evidence-bundle.json` is present (Phase AW). Expect `workstation_evidence_ready=false` and `neural_enablement_ready=false` on CI; on tier-C GPU workstation re-run with `--strict` until `g9_enablement_evidence_ready=true` and `parity_ok=true` on the G9/admission capstone (Phases AY–AZ) and matching parity on the neural capstone (Phase AZ).

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
   Record evidence locally (standalone or via neural capstone):
   ```bash
   PYTHONPATH=src python scripts/hunyuan_g7_hosted_neural_record.py \
     --status-file status.md --sample Block --record hunyuan-g7-hosted-neural.json
   # Or one-shot with neural capstone + parity:
   PYTHONPATH=src python scripts/hunyuan_neural_enablement_preflight_bundle.py \
     --record-dir . --hosted-neural --status-file status.md --hosted-sample Block --strict
   PYTHONPATH=src python scripts/verify_hunyuan_g7_hosted_neural_record.py \
     hunyuan-g7-hosted-neural.json
   ```
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
