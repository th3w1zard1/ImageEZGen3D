from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from imageezgen3d.adapters.base import GenerationRequest
from imageezgen3d.generation_pipeline import PipelineStageTracker
from imageezgen3d.text_neural_inference import (
    TEXT_NEURAL_ADAPTER,
    run_text_neural_shape,
    to_generation_result,
)


class _MockTextNeuralBackend:
    def run_text_shape(
        self,
        request: GenerationRequest,
        *,
        tracker: PipelineStageTracker,
    ) -> dict[str, Path]:
        export_dir = request.run_dir / "exports"
        export_dir.mkdir(parents=True, exist_ok=True)
        glb = export_dir / "text_neural_mesh.glb"
        obj = export_dir / "text_neural_mesh.obj"
        glb.write_bytes(b"glTF")
        obj.write_text("v 0 0 0\n", encoding="utf-8")
        tracker.mark_shape_succeeded_staged(TEXT_NEURAL_ADAPTER, notes="text shape tower")
        tracker.set_stage(
            "texture",
            "skipped",
            notes="Text-conditioned shape; separate paint stage not run.",
        )
        return {"glb": glb, "obj": obj}


class TextNeuralInferenceTests(unittest.TestCase):
    def test_run_raises_not_implemented_without_backend(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            request = GenerationRequest(
                run_dir=Path(directory),
                processed_image=None,
                view_images={},
                quality="draft",
                seed=1,
                input_modality="text",
                prompt_text="A wooden chair",
            )
            with self.assertRaises(NotImplementedError):
                run_text_neural_shape(request)

    def test_run_requires_prompt(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            request = GenerationRequest(
                run_dir=Path(directory),
                processed_image=None,
                view_images={},
                quality="draft",
                seed=1,
                input_modality="text",
                prompt_text="",
            )
            with self.assertRaisesRegex(ValueError, "non-empty prompt"):
                run_text_neural_shape(request)

    def test_mock_backend_records_shape_stage(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            request = GenerationRequest(
                run_dir=Path(directory),
                processed_image=None,
                view_images={},
                quality="balanced",
                seed=1,
                input_modality="text",
                prompt_text="Ceramic vase",
            )
            result = run_text_neural_shape(
                request,
                backend=_MockTextNeuralBackend(),
            )
            stages = {item["name"]: item["status"] for item in result.pipeline_stages}
            self.assertEqual(stages["shape"], "succeeded")
            self.assertEqual(stages["texture"], "skipped")
            self.assertTrue(result.artifacts["glb"].exists())

    def test_to_generation_result_includes_pipeline_stages(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            request = GenerationRequest(
                run_dir=Path(directory),
                processed_image=None,
                view_images={},
                quality="draft",
                seed=0,
                input_modality="text",
                prompt_text="Sphere",
            )
            inference = run_text_neural_shape(
                request,
                backend=_MockTextNeuralBackend(),
            )
            gen = to_generation_result(inference)
            self.assertIn("pipeline_stages", gen.metadata)
            self.assertEqual(gen.adapter, TEXT_NEURAL_ADAPTER)


if __name__ == "__main__":
    unittest.main()
