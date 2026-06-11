from __future__ import annotations

import json
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

from imageezgen3d.config import AppConfig, AppSettings, ExportSettings, StorageSettings
from imageezgen3d.jobs import JobRequest, JobService, load_batch_requests, run_batch
from imageezgen3d.jobs.models import JobRequest as JobRequestModel
from imageezgen3d.jobs.store import JobStore
from PIL import Image


class JobStoreTests(unittest.TestCase):
    def test_create_and_load_round_trip(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            store = JobStore(Path(directory))
            record = store.create(request={"input_modality": "text", "prompt_text": "mug"})
            loaded = store.load(record.job_id)
            self.assertEqual(loaded.status, "queued")
            self.assertEqual(loaded.request["prompt_text"], "mug")


class JobServiceTests(unittest.TestCase):
    def _service(self, tmp: Path) -> JobService:
        config = AppConfig(
            app=AppSettings(output_dir=tmp),
            storage=StorageSettings(retention_runs=10),
        )
        return JobService(config, max_workers=1)

    def test_submit_text_job_completes_with_async_capable(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            tmp = Path(directory)
            service = self._service(tmp)
            try:
                job_id = service.submit(
                    JobRequest(
                        input_modality="text",
                        prompt_text="Wooden crate",
                        lane="draft",
                    )
                )
                poll = service.wait_for(job_id, timeout_seconds=60.0)
                self.assertEqual(poll.status, "succeeded")
                manifest = service.get_result(job_id)
                self.assertEqual(
                    manifest["parameters"]["generation"]["async_capable"],
                    True,
                )
                self.assertEqual(manifest["parameters"]["job_id"], job_id)
            finally:
                service.shutdown(wait=True)

    def test_submit_image_job_from_path(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            tmp = Path(directory)
            image_path = tmp / "input.png"
            Image.new("RGB", (64, 64), (120, 80, 40)).save(image_path)
            service = self._service(tmp)
            try:
                job_id = service.submit(
                    JobRequest(
                        input_modality="image",
                        image_path=str(image_path),
                        adapter_name="cpu-demo",
                        quality="draft",
                    )
                )
                poll = service.wait_for(job_id, timeout_seconds=60.0)
                self.assertEqual(poll.status, "succeeded")
            finally:
                service.shutdown(wait=True)

    def test_target_formats_exports_subset(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            tmp = Path(directory)
            config = AppConfig(
                app=AppSettings(output_dir=tmp),
                storage=StorageSettings(retention_runs=10),
                exports=ExportSettings(formats=("glb", "obj", "fbx")),
            )
            service = JobService(config, max_workers=1)
            try:
                job_id = service.submit(
                    JobRequest(
                        input_modality="text",
                        prompt_text="Format subset mug",
                        target_formats=("glb", "fbx"),
                    )
                )
                poll = service.wait_for(job_id, timeout_seconds=60.0)
                self.assertEqual(poll.status, "succeeded")
                manifest = service.get_result(job_id)
                self.assertEqual(
                    manifest["parameters"]["target_formats"],
                    ["glb", "fbx"],
                )
                self.assertEqual(
                    manifest["parameters"]["export_formats"],
                    ["glb", "fbx"],
                )
                artifacts = manifest["artifacts"]
                self.assertIn("glb", artifacts)
                self.assertIn("fbx", artifacts)
                self.assertNotIn("obj", artifacts)
            finally:
                service.shutdown(wait=True)

    def test_invalid_target_formats_rejected_at_submit(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            service = self._service(Path(directory))
            try:
                with self.assertRaisesRegex(ValueError, "Unknown export format"):
                    service.submit(
                        JobRequest(
                            input_modality="text",
                            prompt_text="Bad format",
                            target_formats=("glb", "dae"),
                        )
                    )
            finally:
                service.shutdown(wait=True)

    def test_poll_reports_running_then_succeeded(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            service = self._service(Path(directory))
            try:
                job_id = service.submit(
                    JobRequest(input_modality="text", prompt_text="Sphere")
                )
                terminal = service.wait_for(job_id, timeout_seconds=60.0)
                self.assertIn(terminal.status, ("succeeded", "failed"))
                self.assertTrue(terminal.result_ready)
            finally:
                service.shutdown(wait=True)

    def test_failed_job_records_error(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            service = self._service(Path(directory))
            try:
                job_id = service.submit(
                    JobRequest(input_modality="image", image_path="/missing/file.png")
                )
                poll = service.wait_for(job_id, timeout_seconds=60.0)
                self.assertEqual(poll.status, "failed")
                self.assertTrue(poll.error)
            finally:
                service.shutdown(wait=True)

    def test_webhook_delivery_on_success(self) -> None:
        received: list[dict[str, object]] = []

        class Handler(BaseHTTPRequestHandler):
            def do_POST(self) -> None:  # noqa: N802
                length = int(self.headers.get("Content-Length", "0"))
                body = self.rfile.read(length)
                received.append(json.loads(body.decode("utf-8")))
                self.send_response(204)
                self.end_headers()

            def log_message(self, format: str, *args: object) -> None:
                return

        server = HTTPServer(("127.0.0.1", 0), Handler)
        port = server.server_address[1]
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        webhook_url = f"http://127.0.0.1:{port}/hook"

        with tempfile.TemporaryDirectory() as directory:
            service = self._service(Path(directory))
            try:
                job_id = service.submit(
                    JobRequest(
                        input_modality="text",
                        prompt_text="Hook test mug",
                        webhook_url=webhook_url,
                    )
                )
                poll = service.wait_for(job_id, timeout_seconds=60.0)
                self.assertEqual(poll.status, "succeeded")
                record = service.job_store.load(job_id)
                self.assertTrue(record.webhook_delivered)
                self.assertEqual(received[0]["job_id"], job_id)
            finally:
                service.shutdown(wait=True)
                server.shutdown()
                server.server_close()


class BatchTests(unittest.TestCase):
    def test_load_batch_requests_skips_comments(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "batch.jsonl"
            path.write_text(
                "# comment\n"
                '{"input_modality":"text","prompt_text":"A"}\n'
                "\n"
                '{"input_modality":"text","prompt_text":"B"}\n',
                encoding="utf-8",
            )
            items = load_batch_requests(path)
            self.assertEqual(len(items), 2)

    def test_run_batch_wait_returns_summaries(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            tmp = Path(directory)
            config = AppConfig(
                app=AppSettings(output_dir=tmp),
                storage=StorageSettings(retention_runs=10),
            )
            service = JobService(config, max_workers=1)
            try:
                summaries = run_batch(
                    service,
                    [
                        JobRequestModel(input_modality="text", prompt_text="One"),
                        JobRequestModel(input_modality="text", prompt_text="Two"),
                    ],
                    wait=True,
                    timeout_seconds=120.0,
                )
                self.assertEqual(len(summaries), 2)
                self.assertTrue(all(item["status"] == "succeeded" for item in summaries))
            finally:
                service.shutdown(wait=True)


if __name__ == "__main__":
    unittest.main()
