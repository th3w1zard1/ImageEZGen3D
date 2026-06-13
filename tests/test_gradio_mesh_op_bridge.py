from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from PIL import Image

from imageezgen3d.config import AppConfig, AppSettings, StorageSettings
from imageezgen3d.exporters import make_box_mesh, write_glb
from imageezgen3d.jobs import JobService
from imageezgen3d.jobs.gradio_bridge import (
    build_animate_job_request,
    build_mesh_op_job_request,
    build_retexture_job_request,
    capture_retry_snapshot,
    resolve_generation_input_modality,
    run_via_job_queue,
)


class GradioMeshOpBridgeTests(unittest.TestCase):
    def test_build_mesh_op_job_request_sets_remesh_defaults(self) -> None:
        request = build_mesh_op_job_request("remesh", "/tmp/mesh.glb")
        self.assertEqual(request.input_modality, "remesh")
        self.assertEqual(request.mesh_input_path, "/tmp/mesh.glb")
        self.assertEqual(request.target_polycount, 30_000)

    def test_build_mesh_op_job_request_normalizes_modality(self) -> None:
        request = build_mesh_op_job_request(" Print-Analyze ", "/tmp/mesh.glb")
        self.assertEqual(request.input_modality, "print-analyze")
        self.assertIsNone(request.target_polycount)

    def test_build_mesh_op_job_request_stages_boolean_second_mesh(self) -> None:
        request = build_mesh_op_job_request(
            "boolean-difference",
            "/tmp/first.glb",
            second_mesh_path="/tmp/second.glb",
        )
        self.assertEqual(request.input_modality, "boolean-difference")
        self.assertEqual(request.second_mesh_path, "/tmp/second.glb")

    def test_resolve_generation_input_modality_promotes_labeled_views(self) -> None:
        self.assertEqual(
            resolve_generation_input_modality(
                "image",
                Image.new("RGB", (8, 8)),
                {"front": Image.new("RGB", (8, 8)), "back": None},
            ),
            "multi-image-to-3d",
        )
        self.assertEqual(
            resolve_generation_input_modality("image", Image.new("RGB", (8, 8)), {}),
            "image",
        )

    def test_build_retexture_job_request_stages_texture_image(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            intake_root = Path(directory) / "intake"
            texture = Image.new("RGB", (32, 32), (120, 80, 40))
            request = build_retexture_job_request(
                intake_root=intake_root,
                source_mesh_path="/tmp/mesh.glb",
                texture_image=texture,
                prompt_text="brushed bronze",
            )
            self.assertEqual(request.input_modality, "retexture")
            self.assertEqual(request.source_mesh_path, "/tmp/mesh.glb")
            self.assertTrue(Path(request.texture_image_path or "").is_file())
            self.assertEqual(request.prompt_text, "brushed bronze")

    def test_build_animate_job_request_targets_animation_demo(self) -> None:
        request = build_animate_job_request("/tmp/mesh.glb", action_id="Walking_man")
        self.assertEqual(request.input_modality, "animate")
        self.assertEqual(request.source_mesh_path, "/tmp/mesh.glb")
        self.assertEqual(request.action_id, "Walking_man")
        self.assertEqual(request.adapter_name, "animation-demo")

    def test_capture_retry_snapshot_records_generate_inputs(self) -> None:
        snapshot = capture_retry_snapshot(
            starter_flow="single-photo-draft",
            project_brief_text="Keep silhouette",
            reference_brief_file=None,
            adapter_name="cpu-demo",
            quality_name="draft",
            seed_value=9,
            input_modality_name="image",
            text_prompt_value="",
            generation_lane_name="draft",
            queue_as_job_enabled=True,
        )
        self.assertEqual(snapshot["starter_flow"], "single-photo-draft")
        self.assertEqual(snapshot["seed_value"], 9)
        self.assertTrue(snapshot["queue_as_job_enabled"])

    def test_run_remesh_via_job_queue_returns_glb(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            config = AppConfig(
                app=AppSettings(output_dir=Path(directory)),
                storage=StorageSettings(retention_runs=10),
            )
            input_glb = Path(directory) / "input.glb"
            write_glb(
                make_box_mesh(1.0, 0.74, 1.35, (0.12, 0.58, 0.55, 1.0)),
                input_glb,
            )
            service = JobService(config, max_workers=1)
            try:
                request = build_mesh_op_job_request("remesh", str(input_glb))
                result = run_via_job_queue(service, request, timeout_seconds=120.0)
                self.assertIn("glb", result["artifacts"])
                self.assertEqual(
                    result["parameters"].get("input_modality"),
                    "remesh",
                )
            finally:
                service.shutdown(wait=True)


if __name__ == "__main__":
    unittest.main()
