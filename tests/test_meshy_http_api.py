from __future__ import annotations

import json
import tempfile
import threading
import time
import unittest
from pathlib import Path
from urllib import request

from imageezgen3d.config import AppConfig, AppSettings, StorageSettings
from imageezgen3d.exporters import export_all, make_box_mesh
from imageezgen3d.jobs import JobService
from imageezgen3d.jobs.http_api import create_job_api_server
from imageezgen3d.jobs.meshy_api import job_request_from_meshy, meshy_status


class MeshyApiTranslationTests(unittest.TestCase):
    def test_text_to_3d_preview_maps_lane(self) -> None:
        job = job_request_from_meshy(
            "text-to-3d",
            {"mode": "preview", "prompt": "wooden crate"},
        )
        self.assertEqual(job.input_modality, "text")
        self.assertEqual(job.lane, "preview")
        self.assertEqual(job.prompt_text, "wooden crate")

    def test_animation_maps_action_id(self) -> None:
        job = job_request_from_meshy(
            "animations",
            {"action_id": "Walking_man", "model_url": "/tmp/mesh.glb"},
        )
        self.assertEqual(job.input_modality, "animate")
        self.assertEqual(job.action_id, "Walking_man")

    def test_multi_image_to_3d_maps_views_and_modality(self) -> None:
        job = job_request_from_meshy(
            "multi-image-to-3d",
            {
                "image_urls": ["/tmp/front.png", "/tmp/back.png"],
                "enable_pbr": False,
            },
        )
        self.assertEqual(job.input_modality, "multi-image-to-3d")
        self.assertEqual(job.task_type, "multi-image-to-3d")
        self.assertEqual(
            job.view_image_paths,
            {"front": "/tmp/front.png", "back": "/tmp/back.png"},
        )
        self.assertEqual(job.image_path, "/tmp/front.png")

    def test_print_multi_color_maps_parameters(self) -> None:
        job = job_request_from_meshy(
            "print-multi-color",
            {
                "model_url": "/tmp/mesh.glb",
                "max_colors": 8,
                "max_depth": 5,
            },
        )
        self.assertEqual(job.input_modality, "print-multi-color")
        self.assertEqual(job.task_type, "print-multi-color")
        self.assertEqual(job.mesh_input_path, "/tmp/mesh.glb")
        self.assertEqual(job.max_colors, 8)
        self.assertEqual(job.max_depth, 5)

    def test_print_multi_color_rejects_invalid_max_colors(self) -> None:
        with self.assertRaisesRegex(ValueError, "max_colors"):
            job_request_from_meshy(
                "print-multi-color",
                {"model_url": "/tmp/mesh.glb", "max_colors": 32},
            )

    def test_status_mapping(self) -> None:
        self.assertEqual(meshy_status("queued"), "PENDING")
        self.assertEqual(meshy_status("running"), "IN_PROGRESS")
        self.assertEqual(meshy_status("succeeded"), "SUCCEEDED")


class MeshyHttpApiTests(unittest.TestCase):
    def _start_server(self, tmp: Path) -> tuple[JobService, object, int]:
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

    def _sample_glb(self, path: Path) -> Path:
        export_dir = path.parent
        export_dir.mkdir(parents=True, exist_ok=True)
        paths = export_all(
            make_box_mesh(width=0.5, depth=0.5, height=0.5, color=(0.7, 0.7, 0.7, 1.0)),
            export_dir,
            stem="sample",
        )
        return paths["glb"]

    def test_balance_endpoint(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            service, server, port = self._start_server(Path(directory))
            try:
                with request.urlopen(
                    f"http://127.0.0.1:{port}/openapi/v1/balance",
                    timeout=5,
                ) as resp:
                    payload = json.loads(resp.read().decode("utf-8"))
                self.assertGreater(payload["balance"], 0)
            finally:
                server.shutdown()
                server.server_close()
                service.shutdown(wait=True)

    def test_text_to_image_meshy_route(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            service, server, port = self._start_server(Path(directory))
            base = f"http://127.0.0.1:{port}"
            try:
                body = json.dumps({"prompt": "neon jellyfish"}).encode("utf-8")
                submit_req = request.Request(
                    f"{base}/openapi/v1/text-to-image",
                    data=body,
                    headers={"Content-Type": "application/json"},
                    method="POST",
                )
                with request.urlopen(submit_req, timeout=5) as resp:
                    self.assertEqual(resp.status, 202)
                    submit_payload = json.loads(resp.read().decode("utf-8"))
                self.assertIn(
                    submit_payload["status"],
                    ("PENDING", "IN_PROGRESS", "SUCCEEDED"),
                )
                task_id = submit_payload["id"]
                deadline = time.monotonic() + 60.0
                status = submit_payload["status"]
                while status != "SUCCEEDED" and time.monotonic() < deadline:
                    time.sleep(0.05)
                    with request.urlopen(
                        f"{base}/openapi/v1/text-to-image/{task_id}",
                        timeout=5,
                    ) as poll_resp:
                        poll_payload = json.loads(poll_resp.read().decode("utf-8"))
                        status = poll_payload["status"]
                self.assertEqual(status, "SUCCEEDED")
                self.assertIn("png", poll_payload.get("model_urls", {}))
            finally:
                server.shutdown()
                server.server_close()
                service.shutdown(wait=True)

    def test_remesh_meshy_route(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            tmp = Path(directory)
            mesh_path = self._sample_glb(tmp / "exports" / "sample.glb")
            service, server, port = self._start_server(tmp)
            base = f"http://127.0.0.1:{port}"
            try:
                body = json.dumps(
                    {
                        "model_url": str(mesh_path),
                        "target_polycount": 500,
                        "topology": "triangle",
                    }
                ).encode("utf-8")
                submit_req = request.Request(
                    f"{base}/openapi/v1/remesh",
                    data=body,
                    headers={"Content-Type": "application/json"},
                    method="POST",
                )
                with request.urlopen(submit_req, timeout=5) as resp:
                    submit_payload = json.loads(resp.read().decode("utf-8"))
                task_id = submit_payload["id"]
                deadline = time.monotonic() + 60.0
                status = submit_payload["status"]
                while status != "SUCCEEDED" and time.monotonic() < deadline:
                    time.sleep(0.05)
                    with request.urlopen(
                        f"{base}/openapi/v1/remesh/{task_id}",
                        timeout=5,
                    ) as poll_resp:
                        poll_payload = json.loads(poll_resp.read().decode("utf-8"))
                        status = poll_payload["status"]
                self.assertEqual(status, "SUCCEEDED")
                self.assertIn("glb", poll_payload.get("model_urls", {}))
            finally:
                server.shutdown()
                server.server_close()
                service.shutdown(wait=True)

    def test_multi_color_print_meshy_route(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            tmp = Path(directory)
            mesh_path = self._sample_glb(tmp / "exports" / "sample.glb")
            service, server, port = self._start_server(tmp)
            base = f"http://127.0.0.1:{port}"
            try:
                body = json.dumps(
                    {
                        "model_url": str(mesh_path),
                        "max_colors": 4,
                        "max_depth": 4,
                    }
                ).encode("utf-8")
                submit_req = request.Request(
                    f"{base}/openapi/v1/print/multi-color",
                    data=body,
                    headers={"Content-Type": "application/json"},
                    method="POST",
                )
                with request.urlopen(submit_req, timeout=5) as resp:
                    submit_payload = json.loads(resp.read().decode("utf-8"))
                self.assertEqual(submit_payload["type"], "print-multi-color")
                task_id = submit_payload["id"]
                deadline = time.monotonic() + 60.0
                status = submit_payload["status"]
                while status != "SUCCEEDED" and time.monotonic() < deadline:
                    time.sleep(0.05)
                    with request.urlopen(
                        f"{base}/openapi/v1/print/multi-color/{task_id}",
                        timeout=5,
                    ) as poll_resp:
                        poll_payload = json.loads(poll_resp.read().decode("utf-8"))
                        status = poll_payload["status"]
                self.assertEqual(status, "SUCCEEDED")
                self.assertEqual(poll_payload.get("type"), "print-multi-color")
                self.assertEqual(poll_payload.get("consumed_credits"), 10)
                self.assertIn("3mf", poll_payload.get("model_urls", {}))
            finally:
                server.shutdown()
                server.server_close()
                service.shutdown(wait=True)


if __name__ == "__main__":
    unittest.main()
