from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from imageezgen3d.adapters.base import GenerationRequest
from imageezgen3d.adapters.retexture_demo import RetextureDemoAdapter
from imageezgen3d.config import AppConfig, AppSettings, StorageSettings
from imageezgen3d.generation_pipeline import (
    RETEXTURE_STUB_DISCLAIMER,
    build_pipeline_spec,
)
from imageezgen3d.jobs import JobRequest, JobService
from imageezgen3d.orchestrator import ImageEZOrchestrator
from PIL import Image


def _texture(path: Path) -> Path:
    Image.new("RGB", (96, 96), (180, 90, 40)).save(path)
    return path


class RetexturePipelineSpecTests(unittest.TestCase):
    def test_retexture_modality_resolution(self) -> None:
        spec = build_pipeline_spec(
            input_modality="retexture",
            lane="draft",
            quality=None,
            prompt_text=None,
        )
        self.assertEqual(spec.input_modality, "retexture")

    def test_retexture_prompt_optional(self) -> None:
        spec = build_pipeline_spec(
            input_modality="retexture",
            lane="draft",
            quality=None,
            prompt_text="brushed bronze",
        )
        self.assertEqual(spec.prompt_text, "brushed bronze")


class RetextureDemoAdapterTests(unittest.TestCase):
    def test_adapter_requires_texture_image(self) -> None:
        adapter = RetextureDemoAdapter()
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(ValueError, "texture reference"):
                adapter.generate(
                    GenerationRequest(
                        run_dir=Path(tmp),
                        processed_image=None,
                        view_images={},
                        quality="draft",
                        seed=0,
                        input_modality="retexture",
                    )
                )

    def test_adapter_missing_source_mesh_raises(self) -> None:
        adapter = RetextureDemoAdapter()
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = Path(tmp)
            texture = _texture(run_dir / "texture.png")
            with self.assertRaises(FileNotFoundError):
                adapter.generate(
                    GenerationRequest(
                        run_dir=run_dir,
                        processed_image=texture,
                        view_images={},
                        quality="draft",
                        seed=0,
                        input_modality="retexture",
                        source_mesh_path=run_dir / "missing.glb",
                    )
                )

    def test_adapter_produces_exports_and_pbr_maps(self) -> None:
        adapter = RetextureDemoAdapter()
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = Path(tmp)
            (run_dir / "exports").mkdir()
            texture = _texture(run_dir / "texture.png")
            result = adapter.generate(
                GenerationRequest(
                    run_dir=run_dir,
                    processed_image=texture,
                    view_images={},
                    quality="draft",
                    seed=3,
                    decimation_target=25_000,
                    input_modality="retexture",
                    lane="draft",
                )
            )
            self.assertEqual(result.adapter, "retexture-demo")
            self.assertTrue(result.artifacts["glb"].exists())
            self.assertEqual(result.metadata["task_type"], "retexture")
            self.assertFalse(result.metadata["source_mesh_provided"])
            pbr_keys = [key for key in result.artifacts if key.startswith("pbr_")]
            self.assertTrue(pbr_keys, "expected reference PBR map artifacts")


class RetextureOrchestratorTests(unittest.TestCase):
    def test_select_adapter_routes_retexture(self) -> None:
        orchestrator = ImageEZOrchestrator(AppConfig())
        key, adapter, fallback = orchestrator.select_adapter(
            "auto", input_modality="retexture"
        )
        self.assertEqual(key, "retexture-demo")
        self.assertTrue(adapter.capabilities.configured)
        self.assertIsNone(fallback)

    def test_select_adapter_rejects_mismatched_adapter(self) -> None:
        orchestrator = ImageEZOrchestrator(AppConfig())
        with self.assertRaisesRegex(ValueError, "does not support retexture"):
            orchestrator.select_adapter("cpu-demo", input_modality="retexture")

    def test_retexture_run_skips_shape_and_marks_texture(self) -> None:
        orchestrator = ImageEZOrchestrator(AppConfig())
        with tempfile.TemporaryDirectory() as tmp:
            orchestrator.store.root = Path(tmp)
            texture = Image.new("RGB", (128, 128), (60, 140, 200))
            result = orchestrator.generate(
                primary_image=texture,
                input_modality="retexture",
                lane="draft",
            )
            params = result["parameters"]
            generation = params["generation"]
            self.assertEqual(generation["input_modality"], "retexture")
            self.assertEqual(params["selected_adapter"], "retexture-demo")
            self.assertEqual(
                params["preview_disclaimer"], RETEXTURE_STUB_DISCLAIMER
            )
            self.assertEqual(params["task_type"], "retexture")
            stages = {
                item["name"]: item["status"]
                for item in generation["pipeline_stages"]
            }
            self.assertEqual(stages["shape"], "skipped")
            self.assertEqual(stages["texture"], "succeeded")
            self.assertEqual(stages["export"], "succeeded")
            self.assertIn("texture_reference", result["artifacts"])

    def test_retexture_run_records_source_mesh(self) -> None:
        orchestrator = ImageEZOrchestrator(AppConfig())
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            orchestrator.store.root = tmp_path / "runs"
            mesh_path = tmp_path / "input_mesh.glb"
            mesh_path.write_bytes(b"glTF-stub")
            texture = Image.new("RGB", (128, 128), (90, 90, 90))
            result = orchestrator.generate(
                primary_image=texture,
                input_modality="retexture",
                lane="draft",
                source_mesh_path=mesh_path,
            )
            self.assertIn("source_mesh", result["artifacts"])
            self.assertEqual(
                result["parameters"]["source_mesh_name"], "input_mesh.glb"
            )

    def test_retexture_requires_texture_image(self) -> None:
        orchestrator = ImageEZOrchestrator(AppConfig())
        with tempfile.TemporaryDirectory() as tmp:
            orchestrator.store.root = Path(tmp)
            with self.assertRaisesRegex(ValueError, "texture reference"):
                orchestrator.generate(
                    primary_image=None,
                    input_modality="retexture",
                    lane="draft",
                )


class RetextureJobServiceTests(unittest.TestCase):
    def _service(self, tmp: Path) -> JobService:
        config = AppConfig(
            app=AppSettings(output_dir=tmp),
            storage=StorageSettings(retention_runs=10),
        )
        return JobService(config, max_workers=1)

    def test_submit_requires_texture_path(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            service = self._service(Path(directory))
            try:
                with self.assertRaisesRegex(ValueError, "texture_image_path"):
                    service.submit(JobRequest(input_modality="retexture"))
            finally:
                service.shutdown(wait=True)

    def test_submit_rejects_missing_source_mesh(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            tmp = Path(directory)
            texture_path = _texture(tmp / "texture.png")
            service = self._service(tmp)
            try:
                with self.assertRaises(FileNotFoundError):
                    service.submit(
                        JobRequest(
                            input_modality="retexture",
                            texture_image_path=str(texture_path),
                            source_mesh_path=str(tmp / "missing.glb"),
                        )
                    )
            finally:
                service.shutdown(wait=True)

    def test_retexture_job_completes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            tmp = Path(directory)
            texture_path = _texture(tmp / "texture.png")
            service = self._service(tmp)
            try:
                job_id = service.submit(
                    JobRequest(
                        input_modality="retexture",
                        texture_image_path=str(texture_path),
                        lane="draft",
                    )
                )
                poll = service.wait_for(job_id, timeout_seconds=60.0)
                self.assertEqual(poll.status, "succeeded")
                manifest = service.get_result(job_id)
                self.assertEqual(
                    manifest["parameters"]["selected_adapter"], "retexture-demo"
                )
                self.assertEqual(
                    manifest["parameters"]["task_type"], "retexture"
                )
            finally:
                service.shutdown(wait=True)

    def test_retexture_job_round_trip_payload(self) -> None:
        request = JobRequest(
            input_modality="retexture",
            texture_image_path="/tmp/texture.png",
            source_mesh_path="/tmp/mesh.glb",
        )
        payload = request.to_dict()
        restored = JobRequest.from_dict(payload)
        self.assertEqual(restored.texture_image_path, "/tmp/texture.png")
        self.assertEqual(restored.source_mesh_path, "/tmp/mesh.glb")


if __name__ == "__main__":
    unittest.main()
