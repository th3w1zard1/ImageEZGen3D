---
status: completed
execution: code
phase: "7"
program: meshy-parity
---

# Meshy parity verification + hosted deploy (Phase 7)

## Problem

Phases U–6 landed Meshy docs, mesh_ops, adapters, HTTP API, credits, and workspace UI. Phase 7 closes the program with local smoke, lint, staged Space deploy, and live hosted E2E per `AGENTS.md`.

## Scope

**In:**
- `scripts/verify_meshy_parity_bundle.py` — one-shot local verify (job stack HTTP smoke + meshy test subset).
- Live Space deploy via `scripts/hf_space_sync.py --execute`.
- Hosted golden smoke (Block sample) + record verify; attestation note in hosted-validation doc.
- Plan completion marker.

**Out:** Hunyuan G7 enablement, viewer action job wiring, committing transient smoke JSON to repo.

## Implementation units

1. **`scripts/verify_meshy_parity_bundle.py`** — orchestrates `verify_job_stack_smoke --http` and documents meshy pytest module list.
2. **`docs/knowledgebase/40-operational-risk/hosted-validation-2026-05-23.md`** — append Phase 7 / Meshy program attestation section with run id, adapter mode, artifact presence.
3. **Execution** — deploy Space, run `hosted_golden_smoke.py`, verify record locally.

## Test scenarios

1. Bundle script exits 0 when job stack HTTP smoke passes.
2. `pytest tests/test_credits.py tests/test_meshy_http_api.py tests/test_workspace_ui.py tests/test_app.py` passes.
3. Hosted golden smoke returns `ok: true`, run id present, CPU fallback honestly labeled (not false G7 neural).

## Verification commands

```bash
PYTHONPATH=src python scripts/verify_meshy_parity_bundle.py
PYTHONPATH=src python scripts/verify_job_stack_smoke.py --http
ruff check app.py src scripts tests
PYTHONPATH=src python scripts/hf_space_sync.py --execute
PYTHONPATH=src python scripts/hosted_golden_smoke.py --record /tmp/meshy-phase7-golden.json --json
PYTHONPATH=src python scripts/verify_hosted_golden_smoke_record.py /tmp/meshy-phase7-golden.json
```
