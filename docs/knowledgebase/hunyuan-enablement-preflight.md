# Hunyuan enablement preflight

Single snapshot before setting `HunyuanPlaceholderAdapter.configured = True`.

## Command

```bash
PYTHONPATH=src python scripts/hunyuan_enablement_preflight.py
PYTHONPATH=src python scripts/hunyuan_enablement_preflight.py --json --record hunyuan-enablement-preflight.json
```

## Interpreting output

| Field | Meaning |
| --- | --- |
| `prerequisites_met` | G1–G6 pass (required before enablement) |
| `g8_enablement_documented` | `G8_STATUS: PASS` in `## G8 validation` (post-enablement closure) |
| `g7_readiness` | Nested object (same shape as admission audit `g7_readiness`) |
| `g8_enablement` | Nested object (`section_present`, `documented`, `interim_open`, `gate_status`) |
| `blocking_enablement` | Gates still open (typically G7 hosted E2E, G8 section) |
| `enablement_complete` | Adapter on **and** all gates pass |

Admission audit JSON uses the same nested `g7_readiness` / `g8_enablement` blocks. Paths and section parsing live in `src/imageezgen3d/hosted_validation.py` (`HOSTED_VALIDATION_PATH`, `read_repo_text`, `hosted_validation_section`). Parity is enforced by `tests/test_hunyuan_ci_artifact_parity.py` against `build_admission_audit_payload()`.

## Related tools

- [hunyuan-admission-gates.md](hunyuan-admission-gates.md) — gate definitions
- [hunyuan-g9-enablement-runbook.md](hunyuan-g9-enablement-runbook.md) — enablement PR + rollback checklist
- [hunyuan-g7-preflight.md](hunyuan-g7-preflight.md) — G7 hosted neural run validator
- [hunyuan-g8-preflight.md](hunyuan-g8-preflight.md) — G8 CPU fallback honesty (hosted golden smoke)

## Scheduled CI

The `hosted-golden-smoke` workflow uploads `hunyuan-enablement-preflight.json` alongside admission audit and golden smoke records, then runs `scripts/verify_hunyuan_ci_artifact_parity.py` so G7/G8 blocks cannot drift between files.
