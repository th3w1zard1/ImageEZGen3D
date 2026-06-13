---
status: completed
execution: ops
phase: "18"
program: meshy-parity
---

# Hosted re-attestation after Phases 12–17 (Phase 18)

## Scope

- Deploy `main` (`c176f8b`) to Hugging Face Space via `scripts/hf_space_sync.py --execute`.
- Re-run hosted golden smoke (Block + Vase) and G7 live probe on live Space.
- Append attestation section to `hosted-validation-2026-05-23.md` and refresh PARITY-MATRIX hosted note.

## Out of scope

- Committing transient smoke JSON to repo (records under `/tmp` only).
- Hunyuan G7 neural enablement or ZeroGPU validation.

## Recorded evidence (2026-06-13)

| Check | Run id / result |
| --- | --- |
| Hub deploy | `26a6b9ffa9661aa0e838905d5c206e9bad732726` |
| Block golden smoke | `20260613-073614-13874d80` |
| Vase golden smoke | `20260613-073635-ab08bdd9` |
| G7 live probe | `hosted_probe.ok=true` |

## Verification commands

```bash
PYTHONPATH=src python scripts/verify_meshy_parity_bundle.py
PYTHONPATH=src python scripts/hf_space_sync.py --execute
PYTHONPATH=src python scripts/hosted_golden_smoke.py --record /tmp/block.json --json
PYTHONPATH=src python scripts/verify_hosted_golden_smoke_record.py /tmp/block.json
PYTHONPATH=src python scripts/hosted_golden_smoke.py --sample assets/examples/red_vase.png --record /tmp/vase.json --json
PYTHONPATH=src python scripts/hunyuan_g7_preflight.py --live-probe --json --record /tmp/g7-probe.json
PYTHONPATH=src python scripts/verify_hunyuan_g7_live_probe_record.py /tmp/g7-probe.json
```
