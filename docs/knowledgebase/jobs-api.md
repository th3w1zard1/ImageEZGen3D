# Async Jobs API

`[REPO]` Phase E adds an in-process job queue for automation clients. Gradio remains synchronous; batch and poll flows use `src/imageezgen3d/jobs/`.

## Surfaces

| Surface | Purpose |
| --- | --- |
| `JobService.submit()` | Queue a generation job; returns `job_id` |
| `JobService.poll()` | Poll job status (automation poll endpoint shape) |
| `JobService.get_result()` | Read completed run manifest |
| `JobService.wait_for()` | Block until terminal status |
| `scripts/batch_generate.py` | JSONL batch CLI |
| Webhook POST | Optional `webhook_url` on submit; JSON body on completion |

## Job request (JSONL / dict)

```json
{
  "input_modality": "text",
  "prompt_text": "A ceramic mug with a curved handle",
  "lane": "draft",
  "adapter_name": "auto",
  "webhook_url": "https://example.com/hooks/imageez"
}
```

Image jobs require `"input_modality": "image"` and `"image_path": "/path/to/photo.png"`.

## Poll response

```json
{
  "job_id": "abc123",
  "status": "running",
  "run_id": null,
  "error": null,
  "poll_url": null,
  "result_ready": false
}
```

Terminal statuses: `succeeded`, `failed`.

## Manifest markers

Runs completed via the job queue set:

- `parameters.generation.async_capable: true`
- `parameters.job_id: <job_id>`

Gradio synchronous runs keep `async_capable: false`.

## Batch CLI

```bash
PYTHONPATH=src python scripts/batch_generate.py --input batch.jsonl --json
```

Use `--no-wait` to submit and receive poll handles immediately.

## Scope boundaries

- No public HTTP server in this slice (poll functions are ready for a future FastAPI/Gradio mount).
- Webhooks use best-effort POST; failures are recorded on the job record (`webhook_delivered`, `webhook_error`).
- In-process `ThreadPoolExecutor` only — not distributed queue infrastructure.
