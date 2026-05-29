from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from PIL import Image

from imageezgen3d.adapters.base import GenerationRequest
from imageezgen3d.generation_pipeline import PipelineStageTracker
from imageezgen3d.hunyuan_backend import (
    DevPreviewHunyuanBackend,
    WeightVerifiedHunyuanBackend,
    resolve_hunyuan_backend_from_config,
    resolve_hunyuan_dev_backend,
    resolve_hunyuan_weight_backend,
)
from imageezgen3d.config import HunyuanSettings
from imageezgen3d.hunyuan_inference import run_hunyuan_shape_texture
from imageezgen3d.hunyuan_tier_c_runtime import TierCReadinessError


class HunyuanBackendTests(unittest.TestCase):
    def test_resolve_dev_backend_disabled_returns_none(self) -> None:
        self.assertIsNone(resolve_hunyuan_dev_backend(dev_enabled=False))

    def test_resolve_dev_backend_enabled_returns_preview_backend(self) -> None:
        backend = resolve_hunyuan_dev_backend(dev_enabled=True)
        self.assertIsInstance(backend, DevPreviewHunyuanBackend)

    def test_dev_backend_env_runs_preview_pipeline(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            run_dir = Path(directory)
            image = run_dir / "input.png"
            Image.new("RGB", (32, 32), color=(120, 80, 200)).save(image)
            request = GenerationRequest(
                run_dir=run_dir,
                processed_image=image,
                view_images={},
                quality="draft",
                seed=1,
                decimation_target=25_000,
            )
            with patch.dict(os.environ, {"IMAGEEZ_HUNYUAN_DEV_BACKEND": "true"}, clear=True):
                result = run_hunyuan_shape_texture(request)

            self.assertTrue(result.metadata.get("dev_preview"))
            self.assertIn("preview_disclaimer", result.metadata)
            self.assertIn("export_sidecar", result.artifacts)
            stages = {item["name"]: item["status"] for item in result.pipeline_stages}
            self.assertEqual(stages["texture"], "succeeded")

    def test_weight_verified_backend_raises_after_cache_warm(self) -> None:
        def fake_prepare(**_: object) -> dict[str, object]:
            raise NotImplementedError(
                "Tier-C dependencies satisfied; Hunyuan inference runner is not wired yet."
            )

        backend = WeightVerifiedHunyuanBackend(prepare_runtime=fake_prepare)
        with tempfile.TemporaryDirectory() as directory:
            image = Path(directory) / "input.png"
            Image.new("RGB", (8, 8), color=(10, 20, 30)).save(image)
            request = GenerationRequest(
                run_dir=Path(directory),
                processed_image=image,
                view_images={},
                quality="draft",
                seed=1,
            )
            with self.assertRaisesRegex(NotImplementedError, "inference runner is not wired"):
                backend.run_shape_texture(
                    request,
                    tracker=PipelineStageTracker(),
                )

    def test_weight_verified_backend_reports_missing_tier_c(self) -> None:
        def fake_prepare(**_: object) -> dict[str, object]:
            raise TierCReadinessError(
                "Missing tier C modules: open3d, bpy",
                report={"missing_tier_c": ["open3d", "bpy"]},
            )

        backend = WeightVerifiedHunyuanBackend(prepare_runtime=fake_prepare)
        with tempfile.TemporaryDirectory() as directory:
            image = Path(directory) / "input.png"
            Image.new("RGB", (8, 8), color=(10, 20, 30)).save(image)
            request = GenerationRequest(
                run_dir=Path(directory),
                processed_image=image,
                view_images={},
                quality="draft",
                seed=1,
            )
            with self.assertRaisesRegex(NotImplementedError, "Missing tier C modules"):
                backend.run_shape_texture(
                    request,
                    tracker=PipelineStageTracker(),
                )

    def test_resolve_weight_backend_enabled(self) -> None:
        backend = resolve_hunyuan_weight_backend(weight_enabled=True)
        self.assertIsInstance(backend, WeightVerifiedHunyuanBackend)

    def test_resolve_backend_from_config_prefers_dev_backend(self) -> None:
        settings = HunyuanSettings(dev_backend=True, weight_backend=True)
        backend = resolve_hunyuan_backend_from_config(settings)
        self.assertIsInstance(backend, DevPreviewHunyuanBackend)

    def test_weight_backend_env_raises_with_missing_tier_c(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            run_dir = Path(directory)
            image = run_dir / "input.png"
            Image.new("RGB", (32, 32), color=(120, 80, 200)).save(image)
            request = GenerationRequest(
                run_dir=run_dir,
                processed_image=image,
                view_images={},
                quality="draft",
                seed=1,
                decimation_target=25_000,
            )
            env = {
                "IMAGEEZ_HUNYUAN_WEIGHT_BACKEND": "true",
                "IMAGEEZ_HUNYUAN_DEV_BACKEND": "false",
            }
            with patch.dict(os.environ, env, clear=True):
                with self.assertRaises(NotImplementedError):
                    run_hunyuan_shape_texture(request)


if __name__ == "__main__":
    unittest.main()
