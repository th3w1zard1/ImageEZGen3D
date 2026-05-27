---
title: Hunyuan admission and enablement JSON must stay aligned
date: 2026-05-27
category: best-practices
module: hunyuan-admission
problem_type: best_practice
component: ci
severity: high
applies_when:
  - "Changing hunyuan_admission_audit or enablement preflight output"
  - "Editing hosted-golden-smoke Hunyuan artifact steps"
  - "Adding fields to hunyuan-admission-audit.json"
tags: [hunyuan, ci, admission-gates, enablement-preflight, artifact-parity]
---

# Hunyuan admission and enablement JSON must stay aligned

## Context

Scheduled `hosted-golden-smoke` and the `hunyuan-admission-audit` CI job upload two JSON files:

- `hunyuan-admission-audit.json` — from `build_admission_audit_payload()`
- `hunyuan-enablement-preflight.json` — from `evaluate_enablement_preflight()`

Operators may compare them to decide whether enablement is safe. If `g7_readiness` or `g8_enablement` diverge, one file can imply readiness while the other does not.

## Guidance

| Layer | What enforces parity |
| --- | --- |
| Shared code | `g8_enablement_for_gates()`, `build_admission_audit_payload()` |
| Unit tests | `tests/test_hunyuan_ci_artifact_parity.py`, `tests/test_hunyuan_ci_scripts.py` |
| CLI verify | `scripts/verify_hunyuan_ci_artifact_parity.py` |
| Workflows | `ci.yml` and `hosted-golden-smoke.yml` run `hunyuan_preflight_bundle.py` (includes verify) |

**Local check (one command):**

```bash
python scripts/hunyuan_preflight_bundle.py --record-dir /tmp/hunyuan-preflight
```

**Individual steps:**

```bash
PYTHONPATH=src python scripts/hunyuan_admission_audit.py --record /tmp/audit.json
PYTHONPATH=src python scripts/hunyuan_enablement_preflight.py --record /tmp/preflight.json
PYTHONPATH=src python scripts/verify_hunyuan_ci_artifact_parity.py /tmp/audit.json /tmp/preflight.json
```

## Related

- [hunyuan-enablement-preflight.md](../../knowledgebase/hunyuan-enablement-preflight.md)
- [hunyuan-admission-gates.md](../../knowledgebase/hunyuan-admission-gates.md)
- [hunyuan-g9-enablement-runbook.md](../../knowledgebase/hunyuan-g9-enablement-runbook.md)
