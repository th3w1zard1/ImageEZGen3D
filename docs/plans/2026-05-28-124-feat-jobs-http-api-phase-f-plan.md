---
title: "feat: Jobs HTTP API server (Phase F REST poll endpoints)"
type: feat
status: completed
date: 2026-05-28
origin: docs/plans/2026-05-28-123-feat-async-jobs-phase-e-plan.md
---

# feat: Jobs HTTP API server (Phase F REST poll endpoints)

## Summary

Wrap Phase E `JobService` with a stdlib HTTP server exposing submit/poll/result routes for automation clients, plus CI lint fix for `batch_generate.py`.

---

## Requirements

- R1. `POST /v1/jobs`, `GET /v1/jobs/{id}`, `GET /v1/jobs/{id}/result`, `GET /health`.
- R2. `scripts/jobs_api_server.py` standalone runner.
- R3. Poll responses include `poll_url` when served over HTTP.
- R4. Tests via `tests/test_jobs_http_api.py`.
- R5. Update `docs/knowledgebase/jobs-api.md`.

---

## Scope Boundaries

- Hugging Face Space deployment of HTTP server
- Auth / API keys
- FastAPI or third-party HTTP frameworks
