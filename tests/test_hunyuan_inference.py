from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from imageezgen3d.adapters.base import GenerationRequest
from imageezgen3d.exporters import make_box_mesh
from imageezgen3d.generation_pipeline import PipelineStageTracker
from imageezgen3d.hunyuan_inference import (
    HUNYUAN_ADAPTER,
    HunyuanMeshResult,
    finalize_hunyuan_exports,
    run_hunyuan_shape_texture,
    to_generation_result,
)


class _MockHunyuanBackend:
    def run_shape_texture(
        self,
        request: GenerationRequest,
        *,
        tracker: PipelineStageTracker,
    ) -> HunyuanMeshResult:
        mesh = make_box_mesh(
            width=1.0,
            depth=0.8,
            height=1.0,
            color=(0.45, 0.45, 0.5, 1.0),
        )
        subdivide_levels = {"draft": 0, "balanced": 7, "high": 8}.get(
            request.quality, 0
        )
        raw_mesh = None
        if subdivide_levels > 0:
            from imageezgen3d.mesh_decimation import subdivide_mesh

            raw_mesh = subdivide_mesh(mesh, subdivide_levels)
        tracker.mark_shape_succeeded_staged(HUNYUAN_ADAPTER, notes="shape tower")
        tracker.mark_texture_running(HUNYUAN_ADAPTER)
        tracker.mark_texture_succeeded(HUNYUAN_ADAPTER, notes="paint tower")
        return HunyuanMeshResult(mesh=mesh, raw_mesh=raw_mesh)


class HunyuanInferenceTests(unittest.TestCase):
    def test_run_raises_not_implemented_without_backend(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            request = GenerationRequest(
                run_dir=Path(directory),
                processed_image=None,
                view_images={},
                quality="balanced",
                seed=1,
                decimation_target=150_000,
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
                decimation_target=150_000,
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

    def test_finalize_includes_export_sidecar(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            request = GenerationRequest(
                run_dir=Path(directory),
                processed_image=None,
                view_images={},
                quality="balanced",
                seed=1,
                decimation_target=150_000,
            )
            result = run_hunyuan_shape_texture(
                request,
                backend=_MockHunyuanBackend(),
            )
            sidecar_path = result.artifacts["export_sidecar"]
            self.assertTrue(sidecar_path.is_file())
            payload = json.loads(sidecar_path.read_text(encoding="utf-8"))
            self.assertEqual(payload.get("adapter"), HUNYUAN_ADAPTER)
            self.assertIn("pbr_delivery", payload)

    def test_balanced_quality_exports_raw_glb_when_subdivided(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            request = GenerationRequest(
                run_dir=Path(directory),
                processed_image=None,
                view_images={},
                quality="balanced",
                seed=1,
                decimation_target=150_000,
            )
            result = run_hunyuan_shape_texture(
                request,
                backend=_MockHunyuanBackend(),
            )
            self.assertIn("raw_glb", result.artifacts)
            self.assertTrue(result.metadata.get("raw_exported"))

    def test_to_generation_result_includes_pipeline_stages(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            request = GenerationRequest(
                run_dir=Path(directory),
                processed_image=None,
                view_images={},
                quality="draft",
                seed=0,
                decimation_target=25_000,
            )
            inference = run_hunyuan_shape_texture(
                request,
                backend=_MockHunyuanBackend(),
            )
            gen = to_generation_result(inference)
            self.assertIn("pipeline_stages", gen.metadata)
            self.assertEqual(gen.adapter, HUNYUAN_ADAPTER)

    def test_finalize_hunyuan_exports_standalone(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            request = GenerationRequest(
                run_dir=Path(directory),
                processed_image=None,
                view_images={},
                quality="draft",
                seed=0,
                decimation_target=25_000,
            )
            mesh = make_box_mesh(1.0, 0.8, 1.0, (0.5, 0.5, 0.5, 1.0))
            paths, metadata = finalize_hunyuan_exports(mesh, request)
            self.assertIn("export_sidecar", paths)
            self.assertEqual(metadata["neural_backend"], HUNYUAN_ADAPTER)


if __name__ == "__main__":
    unittest.main()
