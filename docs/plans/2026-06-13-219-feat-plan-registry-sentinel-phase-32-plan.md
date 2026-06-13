---
status: completed
execution: code
phase: "32"
program: agent-hygiene
---

# Plan registry sentinel — Phase 32

## Problem

Phases 30–31 closed stale Meshy plan frontmatter, but agents can still add new `status: active` plans or leave Hunyuan/Meshy tracks ambiguous. Bare `/lfg` on non-GPU hosts keeps spinning doc loops.

## Scope

**In:**

- `tests/test_program_plan_registry.py` — every `docs/plans/*.md` must have `status: completed`
- Wire test into `scripts/verify_meshy_parity_bundle.py`
- `AGENTS.md` — Meshy plan registry closed; bare `/lfg` Hunyuan ops blocked on non-GPU hosts
- Note in `g7-enablement-readiness-2026-05-28.md`

**Out:** Hunyuan G7 enablement, new features, hosted redeploy

## Verification

```bash
PYTHONPATH=src python scripts/verify_meshy_parity_bundle.py
PYTHONPATH=src python -m pytest tests/test_program_plan_registry.py -q
```
