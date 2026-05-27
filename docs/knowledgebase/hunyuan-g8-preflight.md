# Hunyuan G8 preflight (UX honesty)

**G8 enablement closure** requires a `## G8 validation` section with `G8_STATUS: PASS` after re-verifying UX on the live Space.

While Hunyuan remains disabled, **hosted golden smoke** enforces CPU fallback honesty on every run via `validate_g8_cpu_fallback_status()`.

## Interim checks (cpu-demo path)

Status markdown from `/generate` must include:

- `Local CPU Preview` or `cpu-demo`
- A **Fallback** line or `fallback` mention
- **Preview disclaimer** or `disclaimer` mention
- No false claim of successful `hunyuan-zerogpu` / neural reconstruction

## Tooling

| Item | Purpose |
| --- | --- |
| `src/imageezgen3d/hunyuan_g8_preflight.py` | G8 validators; `evaluate_g8_enablement_status()` for CI JSON |
| `src/imageezgen3d/hosted_validation.py` | Shared `## … validation` section parser |
| `scripts/hunyuan_g8_preflight.py` | `--live` (golden smoke) or `--status-file` |
| `hosted_golden_smoke.py` | Calls G8 validator on each smoke run |

## Commands

```bash
PYTHONPATH=src python scripts/hunyuan_g8_preflight.py --live
PYTHONPATH=src python scripts/hunyuan_g8_preflight.py --status-file /path/to/status.md
```
