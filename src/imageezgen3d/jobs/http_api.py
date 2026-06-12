from __future__ import annotations

import json
import re
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any
from urllib.parse import urlparse

from .meshy_api import (
    job_request_from_meshy,
    match_meshy_route,
    meshy_balance_payload,
    meshy_status,
    meshy_task_payload,
)
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
            meshy_route = match_meshy_route(segments, method)
            if meshy_route is not None:
                self._handle_meshy_route(meshy_route, method)
                return
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

    def _handle_meshy_route(self, route, method: str) -> None:
        if route.action == "balance":
            self._write_json(200, meshy_balance_payload())
            return
        if route.action == "create":
            assert route.task_kind is not None
            payload = self._read_json_body()
            job_request = job_request_from_meshy(route.task_kind, payload)
            job_id = self.service.submit(job_request)
            poll = self.service.poll(job_id)
            response = meshy_task_payload(
                task_kind=route.task_kind,
                task_id=job_id,
                poll=poll,
            )
            self._write_json(202, response)
            return
        if route.action == "retrieve":
            assert route.task_kind is not None and route.task_id is not None
            self._validate_job_id(route.task_id)
            poll = self.service.poll(route.task_id)
            manifest = None
            if poll.status == "succeeded":
                manifest = self.service.get_result(route.task_id)
            response = meshy_task_payload(
                task_kind=route.task_kind,
                task_id=route.task_id,
                poll=poll,
                manifest=manifest,
            )
            self._write_json(200, response)
            return
        if route.action == "stream":
            assert route.task_kind is not None and route.task_id is not None
            self._validate_job_id(route.task_id)
            self._write_meshy_stream(route.task_kind, route.task_id)
            return
        raise ValueError(f"Unsupported Meshy route action: {route.action}")

    def _write_meshy_stream(self, task_kind: str, task_id: str) -> None:
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream")
        self.send_header("Cache-Control", "no-cache")
        self.send_header("Connection", "keep-alive")
        self.end_headers()
        deadline = time.monotonic() + 120.0
        last_status: str | None = None
        while time.monotonic() < deadline:
            poll = self.service.poll(task_id)
            status = meshy_status(poll.status)
            manifest = None
            if poll.status == "succeeded":
                manifest = self.service.get_result(task_id)
            payload = meshy_task_payload(
                task_kind=task_kind,
                task_id=task_id,
                poll=poll,
                manifest=manifest,
            )
            if status != last_status:
                chunk = f"data: {json.dumps(payload, sort_keys=True)}\n\n".encode("utf-8")
                self.wfile.write(chunk)
                self.wfile.flush()
                last_status = status
            if status in ("SUCCEEDED", "FAILED", "CANCELED"):
                break
            time.sleep(0.1)

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
