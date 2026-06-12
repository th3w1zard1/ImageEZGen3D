from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from PIL import Image

from imageezgen3d.adapters.animation_demo import AnimationDemoAdapter
from imageezgen3d.adapters.base import GenerationRequest
from imageezgen3d.adapters.creative_lab import CreativeLabDemoAdapter
from imageezgen3d.adapters.image_to_image_demo import ImageToImageDemoAdapter
from imageezgen3d.adapters.rigging_demo import RiggingDemoAdapter
from imageezgen3d.adapters.text_to_image_demo import TextToImageDemoAdapter
from imageezgen3d.config import AppConfig, AppSettings, StorageSettings
from imageezgen3d.generation_pipeline import build_pipeline_spec
from imageezgen3d.jobs import JobRequest, JobService
from imageezgen3d.orchestrator import ImageEZOrchestrator


def _image(path: Path, color: tuple[int, int, int] = (120, 80, 200)) -> Path:
    Image.new("RGB", (96, 96), color).save(path)
    return path


class MeshyAdapterPipelineTests(unittest.TestCase):
    def test_text_to_image_modality_requires_prompt(self) -> None:
        with self.assertRaisesRegex(ValueError, "text prompt"):
            build_pipeline_spec(
                input_modality="text-to-image",
                lane="draft",
                quality=None,
                prompt_text=None,
            )

    def test_creative_lab_modality_optional_prompt(self) -> None:
        spec = build_pipeline_spec(
            input_modality="creative-lab",
            lane="draft",
            quality=None,
            prompt_text=None,
        )
        self.assertEqual(spec.input_modality, "creative-lab")


class TextToImageDemoTests(unittest.TestCase):
    def test_adapter_requires_prompt(self) -> None:
        adapter = TextToImageDemoAdapter()
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(ValueError, "non-empty prompt"):
                adapter.generate(
                    GenerationRequest(
                        run_dir=Path(tmp),
                        processed_image=None,
                        view_images={},
                        quality="draft",
                        seed=0,
                        input_modality="text-to-image",
                    )
                )

    def test_adapter_exports_png(self) -> None:
        adapter = TextToImageDemoAdapter()
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = Path(tmp)
            result = adapter.generate(
                GenerationRequest(
                    run_dir=run_dir,
                    processed_image=None,
                    view_images={},
                    quality="draft",
                    seed=2,
                    input_modality="text-to-image",
                    prompt_text="sunset canyon",
                    aspect_ratio="16:9",
                )
            )
            self.assertEqual(result.adapter, "text-to-image-demo")
            self.assertTrue(result.artifacts["png"].exists())
            self.assertEqual(result.metadata["task_type"], "text-to-image")


class ImageToImageDemoTests(unittest.TestCase):
    def test_adapter_requires_processed_image(self) -> None:
        adapter = ImageToImageDemoAdapter()
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(ValueError, "processed reference"):
                adapter.generate(
                    GenerationRequest(
                        run_dir=Path(tmp),
                        processed_image=None,
                        view_images={},
                        quality="draft",
                        seed=0,
                        input_modality="image-to-image",
                    )
                )


class RiggingDemoTests(unittest.TestCase):
    def test_adapter_exports_bones_and_mesh(self) -> None:
        adapter = RiggingDemoAdapter()
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = Path(tmp)
            result = adapter.generate(
                GenerationRequest(
                    run_dir=run_dir,
                    processed_image=None,
                    view_images={},
                    quality="draft",
                    seed=1,
                    input_modality="rig",
                )
            )
            self.assertEqual(result.adapter, "rigging-demo")
            self.assertTrue(result.artifacts["glb"].exists())
            bones_path = result.artifacts["rig_bones"]
            payload = json.loads(bones_path.read_text(encoding="utf-8"))
            self.assertIn("bones", payload)
            self.assertGreaterEqual(result.metadata["bone_count"], 1)


class AnimationDemoTests(unittest.TestCase):
    def test_adapter_resolves_catalog_entry(self) -> None:
        adapter = AnimationDemoAdapter()
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = Path(tmp)
            result = adapter.generate(
                GenerationRequest(
                    run_dir=run_dir,
                    processed_image=None,
                    view_images={},
                    quality="draft",
                    seed=4,
                    input_modality="animate",
                    action_id="Walking_man",
                )
            )
            self.assertEqual(result.adapter, "animation-demo")
            preset_path = result.artifacts["animation_preset"]
            preset = json.loads(preset_path.read_text(encoding="utf-8"))
            self.assertIn("action_key", preset)
            self.assertTrue(result.artifacts["glb"].exists())


class CreativeLabDemoTests(unittest.TestCase):
    def test_prototype_stage_exports_png_only(self) -> None:
        adapter = CreativeLabDemoAdapter()
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = Path(tmp)
            result = adapter.generate(
                GenerationRequest(
                    run_dir=run_dir,
                    processed_image=None,
                    view_images={},
                    quality="draft",
                    seed=0,
                    input_modality="creative-lab",
                    creative_lab_flow="keychain",
                    creative_lab_stage="prototype",
                    prompt_text="cute robot",
                )
            )
            self.assertEqual(result.metadata["creative_lab_stage"], "prototype")
            self.assertTrue(result.artifacts["png"].exists())
            self.assertNotIn("glb", result.artifacts)

    def test_build_stage_exports_mesh(self) -> None:
        adapter = CreativeLabDemoAdapter()
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = Path(tmp)
            result = adapter.generate(
                GenerationRequest(
                    run_dir=run_dir,
                    processed_image=None,
                    view_images={},
                    quality="draft",
                    seed=0,
                    input_modality="creative-lab",
                    creative_lab_flow="figure",
                    creative_lab_stage="build",
                )
            )
            self.assertTrue(result.artifacts["glb"].exists())
            self.assertTrue(result.artifacts["prototype"].exists())


class MeshyAdapterOrchestratorTests(unittest.TestCase):
    def test_select_adapter_routes_new_modalities(self) -> None:
        orchestrator = ImageEZOrchestrator(AppConfig())
        cases = [
            ("text-to-image", "text-to-image-demo"),
            ("image-to-image", "image-to-image-demo"),
            ("rig", "rigging-demo"),
            ("animate", "animation-demo"),
            ("creative-lab", "creative-lab-demo"),
        ]
        for modality, expected in cases:
            key, adapter, fallback = orchestrator.select_adapter(
                "auto", input_modality=modality
            )
            self.assertEqual(key, expected, modality)
            self.assertTrue(adapter.capabilities.configured)
            self.assertIsNone(fallback)

    def test_text_to_image_run(self) -> None:
        orchestrator = ImageEZOrchestrator(AppConfig())
        with tempfile.TemporaryDirectory() as tmp:
            orchestrator.store.root = Path(tmp)
            result = orchestrator.generate(
                primary_image=None,
                input_modality="text-to-image",
                prompt_text="neon jellyfish",
                lane="draft",
            )
            self.assertEqual(
                result["parameters"]["selected_adapter"], "text-to-image-demo"
            )
            self.assertIn("png", result["artifacts"])

    def test_rig_run_exports_bones(self) -> None:
        orchestrator = ImageEZOrchestrator(AppConfig())
        with tempfile.TemporaryDirectory() as tmp:
            orchestrator.store.root = Path(tmp)
            result = orchestrator.generate(
                primary_image=None,
                input_modality="rig",
                lane="draft",
            )
            self.assertEqual(result["parameters"]["selected_adapter"], "rigging-demo")
            self.assertIn("rig_bones", result["artifacts"])


class MeshyAdapterJobServiceTests(unittest.TestCase):
    def _service(self, tmp: Path) -> JobService:
        config = AppConfig(
            app=AppSettings(output_dir=tmp),
            storage=StorageSettings(retention_runs=10),
        )
        return JobService(config, max_workers=1)

    def test_text_to_image_job_completes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            service = self._service(Path(directory))
            try:
                job_id = service.submit(
                    JobRequest(
                        input_modality="text-to-image",
                        prompt_text="orbital station",
                        aspect_ratio="1:1",
                    )
                )
                poll = service.wait_for(job_id, timeout_seconds=60.0)
                self.assertEqual(poll.status, "succeeded")
                manifest = service.get_result(job_id)
                self.assertEqual(
                    manifest["parameters"]["selected_adapter"], "text-to-image-demo"
                )
            finally:
                service.shutdown(wait=True)

    def test_image_to_image_job_completes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            tmp = Path(directory)
            image_path = _image(tmp / "ref.png")
            service = self._service(tmp)
            try:
                job_id = service.submit(
                    JobRequest(
                        input_modality="image-to-image",
                        image_path=str(image_path),
                        prompt_text="stylize",
                    )
                )
                poll = service.wait_for(job_id, timeout_seconds=60.0)
                self.assertEqual(poll.status, "succeeded")
            finally:
                service.shutdown(wait=True)

    def test_job_request_round_trip_extended_fields(self) -> None:
        request = JobRequest(
            input_modality="animate",
            action_id="Walking_man",
            aspect_ratio="16:9",
            creative_lab_flow="lamp",
            creative_lab_stage="build",
        )
        restored = JobRequest.from_dict(request.to_dict())
        self.assertEqual(restored.action_id, "Walking_man")
        self.assertEqual(restored.aspect_ratio, "16:9")
        self.assertEqual(restored.creative_lab_flow, "lamp")
        self.assertEqual(restored.creative_lab_stage, "build")


if __name__ == "__main__":
    unittest.main()
