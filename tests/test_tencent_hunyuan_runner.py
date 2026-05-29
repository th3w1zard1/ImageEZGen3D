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
from imageezgen3d.tencent_hunyuan_runner import TencentHunyuanInferenceRunner


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


if __name__ == "__main__":
    unittest.main()
