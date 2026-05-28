# Hunyuan G7 preflight

**G7 remains OPEN** until a live Space run completes on the real `hunyuan-zerogpu` path (not cpu-demo fallback).

## G7_PREFLIGHT_STATUS: READY (in-repo)

G1–G6 are closed in-repo. The adapter is still **`configured=False`**. This document records readiness tooling only.

## Tooling

| Item | Purpose |
| --- | --- |
| `src/imageezgen3d/hunyuan_g7_preflight.py` | `evaluate_g7_readiness()`, `validate_g7_hosted_generate_status()`, `probe_hosted_hunyuan_not_enabled()` |
| `scripts/hunyuan_g7_preflight.py` | CLI — local readiness; `--live-probe` for hosted honesty check |
| `tests/test_hunyuan_g7_preflight.py` | Unit tests |

## Commands

```bash
# Local readiness (G1–G6 must pass)
PYTHONPATH=src python scripts/hunyuan_g7_preflight.py

# Optional live probe (network): must NOT report false G7 success while disabled
PYTHONPATH=src python scripts/hunyuan_g7_preflight.py --live-probe
```

## Closing G7 (enablement PR)

1. Set `HunyuanPlaceholderAdapter.configured = True` in the enablement PR.
2. Deploy Space with weights/secrets per G2/G3/G5.
3. Run Block or Vase `/generate` on live Space; status must pass `validate_g7_hosted_generate_status()`.
4. Add a `## G7 validation` section to `hosted-validation-2026-05-23.md` with **`G7_STATUS: PASS`**, run id, and `hunyuan-zerogpu` — admission audit G7 then passes.

**CI:** `hunyuan-admission-audit` and `hosted-golden-smoke` both run `hunyuan_g7_preflight.py` (G1–G6 readiness). Admission audit JSON is built by `imageezgen3d.hunyuan_admission_audit.build_admission_audit_payload()` and includes `g7_readiness` / `g8_enablement`; exits 1 if G1–G6 regress. Hosted doc path: `hosted_validation.HOSTED_VALIDATION_PATH`.

## Golden smoke guard (Plan 080)

`run_hosted_golden_smoke` calls `validate_g7_not_false_neural_claim()` so scheduled/local smoke **fails** if generation status would pass `validate_g7_hosted_generate_status` while the adapter remains disabled (complements G8 CPU fallback honesty).

## Not claimed

- Neural reconstruction on production Space today
- ZeroGPU wall-clock within budget (measure at G7 close)
