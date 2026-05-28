---
title: "feat: Job metadata in UI and poll CLI (Phase G automation surfacing)"
type: feat
status: completed
date: 2026-05-28
origin: docs/plans/2026-05-28-124-feat-jobs-http-api-phase-f-plan.md
---

# feat: Job metadata in UI and poll CLI (Phase G automation surfacing)

## Summary

Surface async job truth in Gradio run cards (`job_id`, async queue chip), add `scripts/poll_job.py` for automation polling, and fix Ruff lint failures on the jobs stack.

---

## Requirements

- R1. **manifest_ui** — show job id prefix + "Async queue" when `async_capable`.
- R2. **`poll_job.py`** — poll/wait/result CLI for submitted jobs.
- R3. **Ruff clean** — remove unused imports; fix `batch_generate.py` module layout.
- R4. **Tests** — manifest_ui job chip coverage.

---

## Scope Boundaries

- Gradio "submit as job" button (future)
- Space deployment of jobs HTTP server
