---
title: "feat: Gradio background job queue toggle (Phase H)"
type: feat
status: completed
date: 2026-05-28
origin: docs/plans/2026-05-28-125-feat-job-ui-poll-cli-phase-g-plan.md
---

# feat: Gradio background job queue toggle (Phase H)

## Summary

Wire **Queue as background job** in Gradio Advanced controls through `JobService`, with image staging, multi-view job requests, and orchestrator-shaped payloads for the existing Create flow.

---

## Requirements

- R1. **`gradio_bridge.py`** — stage PIL inputs, build `JobRequest`, run via job queue.
- R2. **`JobService.get_generation_payload`** — UI-compatible result dict.
- R3. **Extended `JobRequest`** — starter flow, reference brief, view image paths.
- R4. **app.py** — checkbox in Advanced accordion; default off.
- R5. **Tests** — bridge + end-to-end text job through Gradio bridge.

---

## Scope Boundaries

- Separate Gradio tab for job polling
- Space deployment of HTTP jobs API
- Changing default generate path to async
