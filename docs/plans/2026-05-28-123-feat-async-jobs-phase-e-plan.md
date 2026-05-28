---
title: "feat: Async jobs module and batch CLI (Phase E automation API)"
type: feat
status: completed
date: 2026-05-28
origin: docs/plans/2026-05-28-119-feat-meshy-class-platform-foundation-plan.md
---

# feat: Async jobs module and batch CLI (Phase E automation API)

## Summary

Land **`src/imageezgen3d/jobs/`** with submit/poll/result surfaces, optional webhook delivery, JSONL batch CLI, and manifest `async_capable: true` for job-completed runs — while Gradio stays synchronous.

---

## Requirements

- R1. **Job store** — durable JSON job records under `{output_dir}/jobs/`.
- R2. **JobService** — `submit`, `poll`, `get_result`, `wait_for` (poll endpoint shape for future HTTP).
- R3. **Webhooks** — optional POST on terminal status; record delivery outcome on job.
- R4. **Batch CLI** — `scripts/batch_generate.py` reads JSONL requests.
- R5. **Manifest truth** — job runs set `generation.async_capable: true` and `parameters.job_id`.
- R6. **Docs + tests** — `docs/knowledgebase/jobs-api.md` and unit tests.

---

## Scope Boundaries

- Public HTTP REST server
- Distributed queue / worker fleet
- Gradio UI job panel (future)
- Changing synchronous Gradio generate path

---

## Implementation Units

- U1. `jobs/models.py`, `store.py`, `service.py`, `webhooks.py`, `batch.py`
- U2. `scripts/batch_generate.py`
- U3. Tests + jobs-api doc

---

## Key Technical Decisions

- In-process `ThreadPoolExecutor` with `max_workers=1` default (safe for local/CI).
- Poll API returns structured dict ready for HTTP wrapping.
- Webhook payload includes job status and result manifest on success.
