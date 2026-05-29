from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from PIL import Image

from imageezgen3d.config import HunyuanSettings
from imageezgen3d.generation_pipeline import PipelineStageTracker
from imageezgen3d.adapters.base import GenerationRequest
from imageezgen3d.hunyuan_inference_runner import (
    resolve_hunyuan_inference_runner,
)
from imageezgen3d.exporters import SimpleMesh, write_obj
from imageezgen3d.tencent_hunyuan_runner import TencentHunyuanInferenceRunner

_SHAPE_SYMBOL = "hy3dshape.hy3dshape.pipelines.Hunyuan3DDiTPipeline"
_TEXTURE_SYMBOL = "hy3dpaint.textureGenPipeline.Hunyuan3DPaintPipeline"


def _ready_report() -> dict[str, object]:
    return {
        "shape_ready": True,
        "texture_ready": True,
        "bindings_ready": True,
        "missing_shape": [],
        "missing_texture": [],
        "bindings": {
            "shape_class": {
                "available": True,
                "module": "hy3dshape.hy3dshape.pipelines",
                "attr": "Hunyuan3DDiTPipeline",
                "symbol": _SHAPE_SYMBOL,
            },
            "texture_class": {
                "available": True,
                "module": "hy3dpaint.textureGenPipeline",
                "attr": "Hunyuan3DPaintPipeline",
                "symbol": _TEXTURE_SYMBOL,
            },
            "missing_bindings": [],
        },
    }


def _stub_mesh() -> SimpleMesh:
    return SimpleMesh(
        vertices=((0.0, 0.0, 0.0), (1.0, 0.0, 0.0), (0.0, 1.0, 0.0)),
        faces=((0, 1, 2),),
        color=(0.4, 0.5, 0.6, 1.0),
    )


class TencentHunyuanRunnerTests(unittest.TestCase):
    def test_resolve_tencent_runner_from_settings(self) -> None:
        settings = HunyuanSettings(inference_runner="tencent")
        runner = resolve_hunyuan_inference_runner(settings)
        self.assertIsInstance(runner, TencentHunyuanInferenceRunner)

    def test_resolve_unknown_runner_raises(self) -> None:
        settings = HunyuanSettings(inference_runner="unknown-vendor")
        with self.assertRaisesRegex(ValueError, "Unknown Hunyuan inference runner"):
            resolve_hunyuan_inference_runner(settings)

    def test_tencent_runner_raises_before_neural_inference(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            checkpoint = root / "hunyuan3d-dit-v2-1"
            checkpoint.mkdir(parents=True)
            (checkpoint / "model.fp16.ckpt").write_bytes(b"ckpt")
            image = root / "input.png"
            Image.new("RGB", (8, 8), color=(10, 20, 30)).save(image)
            request = GenerationRequest(
                run_dir=root,
                processed_image=image,
                view_images={},
                quality="draft",
                seed=1,
            )
            runner = TencentHunyuanInferenceRunner()
            tracker = PipelineStageTracker()
            with self.assertRaisesRegex(
                NotImplementedError,
                "Missing Tencent shape pipeline modules",
            ):
                runner.run_shape_texture(
                    request,
                    tracker=tracker,
                    weight_root=root,
                    shape_checkpoint=checkpoint / "model.fp16.ckpt",
                )
            stages = {item["name"]: item["status"] for item in tracker.to_list()}
            self.assertEqual(stages["shape"], "failed")

    def test_tencent_runner_env_wires_probe(self) -> None:
        with mock.patch.dict(
            os.environ,
            {"IMAGEEZ_HUNYUAN_INFERENCE_RUNNER": "tencent"},
            clear=True,
        ):
            from imageezgen3d.hunyuan_inference_runner import (
                describe_hunyuan_inference_runner,
            )

            payload = describe_hunyuan_inference_runner()
            self.assertTrue(payload["inference_wired"])
            self.assertEqual(payload["runner_id"], "TencentHunyuanInferenceRunner")

    @mock.patch("imageezgen3d.tencent_hunyuan_pipeline.resolve_tencent_symbol")
    @mock.patch("imageezgen3d.tencent_hunyuan_pipeline.ensure_tencent_pipeline_ready")
    @mock.patch("imageezgen3d.tencent_hunyuan_runner.ensure_tencent_pipeline_ready")
    def test_runner_returns_mesh_with_injected_executors(
        self,
        runner_ensure_ready: mock.MagicMock,
        pipeline_ensure_ready: mock.MagicMock,
        resolve_symbol: mock.MagicMock,
    ) -> None:
        runner_ensure_ready.return_value = _ready_report()
        pipeline_ensure_ready.return_value = _ready_report()
        resolve_symbol.side_effect = lambda module, attr, **kwargs: {
            "available": True,
            "module": module,
            "attr": attr,
            "symbol": f"{module}.{attr}",
        }

        def shape_executor(plan: object, _pipeline_cls: object) -> Path:
            mesh_plan = plan
            mesh_plan.output_mesh.parent.mkdir(parents=True, exist_ok=True)
            write_obj(_stub_mesh(), mesh_plan.output_mesh)
            return mesh_plan.output_mesh

        def texture_executor(plan: object, _pipeline_cls: object) -> Path:
            mesh_plan = plan
            mesh_plan.output_mesh.parent.mkdir(parents=True, exist_ok=True)
            write_obj(_stub_mesh(), mesh_plan.output_mesh)
            return mesh_plan.output_mesh

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            checkpoint = root / "hunyuan3d-dit-v2-1"
            checkpoint.mkdir(parents=True)
            (checkpoint / "model.fp16.ckpt").write_bytes(b"ckpt")
            image = root / "input.png"
            Image.new("RGB", (8, 8), color=(10, 20, 30)).save(image)
            request = GenerationRequest(
                run_dir=root,
                processed_image=image,
                view_images={},
                quality="draft",
                seed=1,
            )
            runner = TencentHunyuanInferenceRunner(
                shape_executor=shape_executor,
                texture_executor=texture_executor,
            )
            tracker = PipelineStageTracker()
            result = runner.run_shape_texture(
                request,
                tracker=tracker,
                weight_root=root,
                shape_checkpoint=checkpoint / "model.fp16.ckpt",
            )
            self.assertEqual(len(result.mesh.vertices), 3)
            stages = {item["name"]: item["status"] for item in tracker.to_list()}
            self.assertEqual(stages["shape"], "succeeded")
            self.assertEqual(stages["texture"], "succeeded")


if __name__ == "__main__":
    unittest.main()
