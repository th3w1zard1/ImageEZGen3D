from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from imageezgen3d.adapters.base import GenerationRequest
from imageezgen3d.generation_pipeline import PipelineStageTracker
from imageezgen3d.hunyuan_inference import (
    HUNYUAN_ADAPTER,
    run_hunyuan_shape_texture,
    to_generation_result,
)


class _MockHunyuanBackend:
    def run_shape_texture(
        self,
        request: GenerationRequest,
        *,
        tracker: PipelineStageTracker,
    ) -> dict[str, Path]:
        export_dir = request.run_dir / "exports"
        export_dir.mkdir(parents=True, exist_ok=True)
        glb = export_dir / "hunyuan_mesh.glb"
        obj = export_dir / "hunyuan_mesh.obj"
        glb.write_bytes(b"glTF")
        obj.write_text("v 0 0 0\n", encoding="utf-8")
        tracker.mark_shape_succeeded_staged(HUNYUAN_ADAPTER, notes="shape tower")
        tracker.mark_texture_running(HUNYUAN_ADAPTER)
        tracker.mark_texture_succeeded(HUNYUAN_ADAPTER, notes="paint tower")
        return {"glb": glb, "obj": obj}


class HunyuanInferenceTests(unittest.TestCase):
    def test_run_raises_not_implemented_without_backend(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            request = GenerationRequest(
                run_dir=Path(directory),
                processed_image=None,
                view_images={},
                quality="balanced",
                seed=1,
            )
            with self.assertRaises(NotImplementedError):
                run_hunyuan_shape_texture(request)

    def test_mock_backend_records_shape_texture_stages(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            request = GenerationRequest(
                run_dir=Path(directory),
                processed_image=None,
                view_images={},
                quality="balanced",
                seed=1,
            )
            result = run_hunyuan_shape_texture(
                request,
                backend=_MockHunyuanBackend(),
            )
            stages = {item["name"]: item["status"] for item in result.pipeline_stages}
            self.assertEqual(stages["shape"], "succeeded")
            self.assertEqual(stages["texture"], "succeeded")
            self.assertEqual(stages["pbr"], "skipped")
            self.assertTrue(result.artifacts["glb"].exists())

    def test_to_generation_result_includes_pipeline_stages(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            request = GenerationRequest(
                run_dir=Path(directory),
                processed_image=None,
                view_images={},
                quality="draft",
                seed=0,
            )
            inference = run_hunyuan_shape_texture(
                request,
                backend=_MockHunyuanBackend(),
            )
            gen = to_generation_result(inference)
            self.assertIn("pipeline_stages", gen.metadata)
            self.assertEqual(gen.adapter, HUNYUAN_ADAPTER)
