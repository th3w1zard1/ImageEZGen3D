from __future__ import annotations

import uuid
from datetime import datetime, timezone
from pathlib import Path

from ..storage import atomic_write_json
from .models import JobRecord, JobStatus


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


class JobStore:
    def __init__(self, root: str | Path) -> None:
        self.root = Path(root).resolve()
        self.root.mkdir(parents=True, exist_ok=True)

    def _path_for(self, job_id: str) -> Path:
        safe_id = Path(job_id).name
        return self.root / f"{safe_id}.json"

    def create(self, *, request: dict[str, object]) -> JobRecord:
        job_id = uuid.uuid4().hex
        now = utc_now()
        record = JobRecord(
            job_id=job_id,
            status="queued",
            created_at=now,
            updated_at=now,
            request=dict(request),
            webhook_url=str(request.get("webhook_url") or "") or None,
        )
        self.save(record)
        return record

    def save(self, record: JobRecord) -> None:
        record.updated_at = utc_now()
        atomic_write_json(self._path_for(record.job_id), record.to_dict())

    def load(self, job_id: str) -> JobRecord:
        path = self._path_for(job_id)
        if not path.exists():
            raise FileNotFoundError(f"Job not found: {job_id}")
        import json

        payload = json.loads(path.read_text(encoding="utf-8"))
        return JobRecord.from_dict(payload)

    def update_status(
        self,
        job_id: str,
        status: JobStatus,
        *,
        run_id: str | None = None,
        error: str | None = None,
        webhook_delivered: bool | None = None,
        webhook_error: str | None = None,
    ) -> JobRecord:
        record = self.load(job_id)
        record.status = status
        if run_id is not None:
            record.run_id = run_id
        if error is not None:
            record.error = error
        if webhook_delivered is not None:
            record.webhook_delivered = webhook_delivered
        if webhook_error is not None:
            record.webhook_error = webhook_error
        self.save(record)
        return record
