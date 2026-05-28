from __future__ import annotations

import json
import re
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any
from urllib.parse import urlparse

from .models import JobRequest
from .service import JobService

_JOB_ID_PATTERN = re.compile(r"^[0-9a-f]{32}$")


class JobApiHandler(BaseHTTPRequestHandler):
    service: JobService
    poll_url_template: str | None = None

    def log_message(self, format: str, *args: object) -> None:
        return

    def do_GET(self) -> None:  # noqa: N802
        self._dispatch("GET")

    def do_POST(self) -> None:  # noqa: N802
        self._dispatch("POST")

    def _dispatch(self, method: str) -> None:
        parsed = urlparse(self.path)
        segments = [segment for segment in parsed.path.split("/") if segment]
        try:
            if method == "GET" and segments == ["health"]:
                self._write_json(200, {"ok": True, "service": "imageezgen3d-jobs"})
                return
            if method == "POST" and segments == ["v1", "jobs"]:
                payload = self._read_json_body()
                job_id = self.service.submit(JobRequest.from_dict(payload))
                poll = self.service.poll(
                    job_id,
                    poll_url_template=self.poll_url_template,
                )
                self._write_json(202, poll.to_dict())
                return
            if (
                method == "GET"
                and len(segments) == 4
                and segments[:2] == ["v1", "jobs"]
                and segments[3] == "result"
            ):
                job_id = segments[2]
                self._validate_job_id(job_id)
                manifest = self.service.get_result(job_id)
                self._write_json(200, manifest)
                return
            if method == "GET" and len(segments) == 3 and segments[:2] == ["v1", "jobs"]:
                job_id = segments[2]
                self._validate_job_id(job_id)
                poll = self.service.poll(
                    job_id,
                    poll_url_template=self.poll_url_template,
                )
                self._write_json(200, poll.to_dict())
                return
        except FileNotFoundError as exc:
            self._write_json(404, {"error": str(exc)})
            return
        except (ValueError, json.JSONDecodeError) as exc:
            self._write_json(400, {"error": str(exc)})
            return
        except RuntimeError as exc:
            self._write_json(409, {"error": str(exc)})
            return

        self._write_json(404, {"error": f"Unknown route: {self.path}"})

    def _read_json_body(self) -> dict[str, Any]:
        length = int(self.headers.get("Content-Length", "0"))
        if length <= 0:
            raise ValueError("Request body required.")
        raw = self.rfile.read(length)
        payload = json.loads(raw.decode("utf-8"))
        if not isinstance(payload, dict):
            raise ValueError("JSON body must be an object.")
        return payload

    def _validate_job_id(self, job_id: str) -> None:
        if not _JOB_ID_PATTERN.match(job_id):
            raise ValueError(f"Invalid job_id: {job_id!r}")

    def _write_json(self, status: int, payload: dict[str, Any]) -> None:
        body = json.dumps(payload, indent=2, sort_keys=True).encode("utf-8") + b"\n"
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def create_job_api_server(
    service: JobService,
    *,
    host: str = "127.0.0.1",
    port: int = 8765,
    poll_url_template: str | None = "http://{host}:{port}/v1/jobs/{{job_id}}",
) -> ThreadingHTTPServer:
    template = (
        poll_url_template.format(host=host, port=port) if poll_url_template else None
    )
    handler = type(
        "ConfiguredJobApiHandler",
        (JobApiHandler,),
        {"service": service, "poll_url_template": template},
    )
    return ThreadingHTTPServer((host, port), handler)
