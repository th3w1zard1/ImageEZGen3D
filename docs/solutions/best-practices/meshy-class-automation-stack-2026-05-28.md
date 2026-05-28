---
title: Meshy-class automation stack (jobs E–H)
date: 2026-05-28
category: best-practices
module: jobs
problem_type: best_practice
component: automation
severity: medium
applies_when:
  - "Changing JobService, HTTP jobs API, or Gradio queue toggle"
  - "Adding automation clients beside Gradio"
  - "Verifying async_capable manifest truth before ship"
tags: [jobs, async-jobs, gradio, http-api, meshy-class, automation]
---

# Meshy-class automation stack (Phases E–H)

## Context

Plans 119–126 landed an automation path **beside** synchronous Gradio: in-process job queue, stdlib HTTP poll API, batch/poll CLIs, UI job chips, and optional Gradio **Queue as background job**. Hunyuan G7–G9 remain OPEN — this stack does not claim neural enablement.

## Layer map

| Layer | Path | Purpose |
| --- | --- | --- |
| Queue | `src/imageezgen3d/jobs/service.py` | submit / poll / wait / webhooks |
| HTTP | `src/imageezgen3d/jobs/http_api.py` | `POST/GET /v1/jobs` for automation |
| Gradio | `jobs/gradio_bridge.py` + Advanced checkbox | Same queue, orchestrator-shaped UI payload |
| CLIs | `scripts/batch_generate.py`, `scripts/poll_job.py`, `scripts/jobs_api_server.py` | Agent-friendly automation |
| Truth | manifest `parameters.job_id`, `generation.async_capable` | Distinguish sync Gradio vs queued runs |

## Local verify (copy-paste)

```bash
PYTHONPATH=src python -m unittest discover -s tests -q
PYTHONPATH=src python scripts/verify_job_stack_smoke.py
PYTHONPATH=src python scripts/verify_job_stack_smoke.py --http
```

## Lint gotchas (CI)

- All `.py` files must start with `from __future__ import annotations` (**no shebang first**).
- Ruff F401: keep `jobs/batch.py` imports minimal.
- Scripts using `sys.path` insert: imports after path setup need `# noqa: E402` where used.

## Trust boundaries

- **Sync Gradio** (checkbox off): `async_capable: false` — default Create path unchanged.
- **Queued runs**: `async_capable: true` + `job_id` — includes Gradio Advanced toggle and external CLIs/HTTP.
- **Do not** deploy `jobs_api_server.py` on Space by default; Gradio remains primary surface.

## PR stack (merge bottom-up)

#76 → #77 → #78 → #79 → #80 → #81 → #82 → #83 — see [127-ship-meshy-class-stack-a-h-plan.md](../../plans/2026-05-28-127-ship-meshy-class-stack-a-h-plan.md).

## Related

- [jobs-api.md](../../knowledgebase/jobs-api.md) — API contract
- [g7-enablement-readiness-2026-05-28.md](g7-enablement-readiness-2026-05-28.md) — next frontier after stack merge
