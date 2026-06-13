from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from PIL import Image

from imageezgen3d.config import AppConfig, AppSettings, StorageSettings
from imageezgen3d.jobs import JobService
from imageezgen3d.jobs.gradio_bridge import (
    build_job_request_from_gradio,
    run_via_job_queue,
)


class GradioJobBridgeTests(unittest.TestCase):
    def test_build_job_request_stages_primary_image(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            intake_root = Path(directory) / "intake"
            image = Image.new("RGB", (32, 32), (10, 20, 30))
            request = build_job_request_from_gradio(
                intake_root=intake_root,
                primary_image=image,
                view_images={"front": image},
                adapter_name="cpu-demo",
                quality_name="draft",
                seed_value=7,
                project_brief_text="brief",
                starter_flow="block",
                starter_flow_label="Block",
                reference_brief_file=None,
                input_modality_name="image",
                text_prompt_value="",
                generation_lane_name="draft",
            )
            self.assertEqual(request.input_modality, "multi-image-to-3d")
            self.assertTrue(Path(request.image_path or "").is_file())
            self.assertIn("front", request.view_image_paths or {})

    def test_run_via_job_queue_returns_orchestrator_payload(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            config = AppConfig(
                app=AppSettings(output_dir=Path(directory)),
                storage=StorageSettings(retention_runs=10),
            )
            service = JobService(config, max_workers=1)
            try:
                request = build_job_request_from_gradio(
                    intake_root=Path(directory) / "intake",
                    primary_image=None,
                    view_images={},
                    adapter_name="auto",
                    quality_name="draft",
                    seed_value=1,
                    project_brief_text="",
                    starter_flow=None,
                    starter_flow_label=None,
                    reference_brief_file=None,
                    input_modality_name="text",
                    text_prompt_value="Simple crate",
                    generation_lane_name="draft",
                )
                result = run_via_job_queue(service, request, timeout_seconds=120.0)
                self.assertTrue(result["parameters"]["generation"]["async_capable"])
                self.assertIn("job_id", result["parameters"])
                self.assertIn("glb", result["artifacts"])
            finally:
                service.shutdown(wait=True)


if __name__ == "__main__":
    unittest.main()
