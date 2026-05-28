from __future__ import annotations

import argparse
import json
import sys
import tempfile
import threading
import time
from pathlib import Path
from urllib import request

from imageezgen3d.config import AppConfig, AppSettings, StorageSettings
from imageezgen3d.jobs import JobRequest, JobService
from imageezgen3d.jobs.http_api import create_job_api_server


def verify_job_stack(*, exercise_http: bool = False) -> list[str]:
    issues: list[str] = []
    with tempfile.TemporaryDirectory() as directory:
        tmp = Path(directory)
        config = AppConfig(
            app=AppSettings(output_dir=tmp),
            storage=StorageSettings(retention_runs=10),
        )
        service = JobService(config, max_workers=1)
        try:
            job_id = service.submit(
                JobRequest(
                    input_modality="text",
                    prompt_text="Job stack smoke crate",
                    lane="draft",
                )
            )
            poll = service.wait_for(job_id, timeout_seconds=120.0)
            if poll.status != "succeeded":
                issues.append(
                    f"job_service: expected succeeded, got {poll.status!r}: {poll.error}"
                )
                return issues
            payload = service.get_generation_payload(job_id)
            generation = payload.get("parameters", {}).get("generation", {})
            if not isinstance(generation, dict) or not generation.get("async_capable"):
                issues.append("job_service: manifest missing generation.async_capable")
            if payload.get("parameters", {}).get("job_id") != job_id:
                issues.append("job_service: manifest job_id mismatch")
            artifacts = payload.get("artifacts", {})
            if not isinstance(artifacts, dict) or not artifacts.get("glb"):
                issues.append("job_service: missing glb artifact in payload")
            if exercise_http:
                issues.extend(_verify_http_api(service, config))
        finally:
            service.shutdown(wait=True)
    return issues


def _verify_http_api(service: JobService, config: AppConfig) -> list[str]:
    issues: list[str] = []
    server = create_job_api_server(service, host="127.0.0.1", port=0)
    port = server.server_address[1]
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    base = f"http://127.0.0.1:{port}"
    try:
        with request.urlopen(f"{base}/health", timeout=5) as resp:
            health = json.loads(resp.read().decode("utf-8"))
        if not health.get("ok"):
            issues.append("http_api: /health not ok")
        body = json.dumps(
            {
                "input_modality": "text",
                "prompt_text": "HTTP smoke sphere",
                "lane": "draft",
            }
        ).encode("utf-8")
        submit_req = request.Request(
            f"{base}/v1/jobs",
            data=body,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with request.urlopen(submit_req, timeout=5) as resp:
            if resp.status != 202:
                issues.append(f"http_api: submit status {resp.status}")
            submit_payload = json.loads(resp.read().decode("utf-8"))
        job_id = str(submit_payload.get("job_id") or "")
        deadline = time.monotonic() + 120.0
        status = str(submit_payload.get("status") or "")
        while status not in ("succeeded", "failed") and time.monotonic() < deadline:
            time.sleep(0.05)
            with request.urlopen(f"{base}/v1/jobs/{job_id}", timeout=5) as poll_resp:
                poll_payload = json.loads(poll_resp.read().decode("utf-8"))
                status = str(poll_payload.get("status") or "")
        if status != "succeeded":
            issues.append(f"http_api: job {job_id} ended with {status!r}")
    except OSError as exc:
        issues.append(f"http_api: request failed: {exc}")
    finally:
        server.shutdown()
        server.server_close()
    return issues


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Verify local JobService + optional HTTP jobs API smoke path.",
    )
    parser.add_argument(
        "--http",
        action="store_true",
        help="Also exercise POST/GET /v1/jobs on an ephemeral local server.",
    )
    args = parser.parse_args(argv)
    issues = verify_job_stack(exercise_http=args.http)
    if issues:
        for issue in issues:
            print(f"issue={issue}", file=sys.stderr)
        return 1
    print("job_stack_smoke=ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
