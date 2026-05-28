from __future__ import annotations

import json
import tempfile
import threading
import time
import unittest
from pathlib import Path
from urllib import request

from imageezgen3d.config import AppConfig, AppSettings, StorageSettings
from imageezgen3d.jobs import JobService
from imageezgen3d.jobs.http_api import create_job_api_server


class JobHttpApiTests(unittest.TestCase):
    def _start_server(self, tmp: Path) -> tuple[JobService, object]:
        config = AppConfig(
            app=AppSettings(output_dir=tmp),
            storage=StorageSettings(retention_runs=10),
        )
        service = JobService(config, max_workers=1)
        server = create_job_api_server(service, host="127.0.0.1", port=0)
        port = server.server_address[1]
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        return service, server, port

    def test_health_endpoint(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            service, server, port = self._start_server(Path(directory))
            try:
                with request.urlopen(f"http://127.0.0.1:{port}/health", timeout=5) as resp:
                    payload = json.loads(resp.read().decode("utf-8"))
                self.assertTrue(payload["ok"])
            finally:
                server.shutdown()
                server.server_close()
                service.shutdown(wait=True)

    def test_submit_poll_and_result_over_http(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            service, server, port = self._start_server(Path(directory))
            base = f"http://127.0.0.1:{port}"
            try:
                body = json.dumps(
                    {
                        "input_modality": "text",
                        "prompt_text": "HTTP API mug",
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
                    self.assertEqual(resp.status, 202)
                    submit_payload = json.loads(resp.read().decode("utf-8"))
                job_id = submit_payload["job_id"]
                self.assertIn(job_id, submit_payload.get("poll_url", ""))

                deadline = time.monotonic() + 60.0
                status = submit_payload["status"]
                while status not in ("succeeded", "failed") and time.monotonic() < deadline:
                    time.sleep(0.05)
                    with request.urlopen(
                        f"{base}/v1/jobs/{job_id}",
                        timeout=5,
                    ) as poll_resp:
                        poll_payload = json.loads(poll_resp.read().decode("utf-8"))
                        status = poll_payload["status"]

                self.assertEqual(status, "succeeded")
                with request.urlopen(
                    f"{base}/v1/jobs/{job_id}/result",
                    timeout=5,
                ) as result_resp:
                    manifest = json.loads(result_resp.read().decode("utf-8"))
                self.assertEqual(manifest["parameters"]["job_id"], job_id)
            finally:
                server.shutdown()
                server.server_close()
                service.shutdown(wait=True)


if __name__ == "__main__":
    unittest.main()
