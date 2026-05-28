from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .models import JobPollResponse, JobRequest, JobStatus
from .service import JobService


def load_batch_requests(path: str | Path) -> list[JobRequest]:
    """Load JSONL batch file (one JobRequest object per line)."""
    requests: list[JobRequest] = []
    for line_number, line in enumerate(
        Path(path).read_text(encoding="utf-8").splitlines(),
        start=1,
    ):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        try:
            payload = json.loads(stripped)
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid JSON on line {line_number}: {exc}") from exc
        if not isinstance(payload, dict):
            raise ValueError(f"Line {line_number} must be a JSON object.")
        requests.append(JobRequest.from_dict(payload))
    return requests


def run_batch(
    service: JobService,
    requests: list[JobRequest],
    *,
    wait: bool = True,
    timeout_seconds: float = 120.0,
) -> list[dict[str, Any]]:
    """Submit each request and optionally wait for completion."""
    summaries: list[dict[str, Any]] = []
    job_ids: list[str] = []
    for item in requests:
        job_ids.append(service.submit(item))

    if not wait:
        for job_id in job_ids:
            summaries.append(service.poll(job_id).to_dict())
        return summaries

    for job_id in job_ids:
        poll = service.wait_for(job_id, timeout_seconds=timeout_seconds)
        entry: dict[str, Any] = poll.to_dict()
        if poll.status == "succeeded":
            entry["manifest"] = service.get_result(job_id)
        summaries.append(entry)
    return summaries
