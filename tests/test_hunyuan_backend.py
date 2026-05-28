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
    resolve_hunyuan_dev_backend,
)
from imageezgen3d.hunyuan_inference import run_hunyuan_shape_texture


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
        backend = WeightVerifiedHunyuanBackend(
            ensure_weights=lambda **_: Path("/tmp/hunyuan-weights"),
        )
        with tempfile.TemporaryDirectory() as directory:
            image = Path(directory) / "input.png"
            image.write_bytes(b"png")
            request = GenerationRequest(
                run_dir=Path(directory),
                processed_image=image,
                view_images={},
                quality="draft",
                seed=1,
            )
            with self.assertRaisesRegex(NotImplementedError, "tier-C inference runtime"):
                backend.run_shape_texture(
                    request,
                    tracker=PipelineStageTracker(),
                )


if __name__ == "__main__":
    unittest.main()
