from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from imageezgen3d.config import HunyuanSettings, load_config
from imageezgen3d.hunyuan_weights import (
    HUNYUAN_MODEL_REPO,
    HUNYUAN_MODEL_REVISION,
    describe_hunyuan_weight_pin,
    ensure_hunyuan_weights,
    resolve_hunyuan_cache_dir,
)


class HunyuanWeightsTests(unittest.TestCase):
    def test_default_pin_matches_g2_documentation(self) -> None:
        with patch.dict(os.environ, {}, clear=True):
            config = load_config(Path("missing.yaml"))
        self.assertEqual(config.hunyuan.model_repo, HUNYUAN_MODEL_REPO)
        self.assertEqual(config.hunyuan.model_revision, HUNYUAN_MODEL_REVISION)

    def test_env_overrides_model_pin(self) -> None:
        env = {
            "IMAGEEZ_HUNYUAN_MODEL_REPO": "org/custom-hunyuan",
            "IMAGEEZ_HUNYUAN_MODEL_REVISION": "deadbeef",
            "IMAGEEZ_HUNYUAN_CACHE_DIR": "/tmp/hunyuan-cache",
        }
        with patch.dict(os.environ, env, clear=True):
            config = load_config(Path("missing.yaml"))
        self.assertEqual(config.hunyuan.model_repo, "org/custom-hunyuan")
        self.assertEqual(config.hunyuan.model_revision, "deadbeef")
        self.assertEqual(config.hunyuan.cache_dir, "/tmp/hunyuan-cache")

    def test_resolve_cache_dir_empty_returns_none(self) -> None:
        settings = HunyuanSettings(cache_dir="")
        self.assertIsNone(resolve_hunyuan_cache_dir(settings))

    def test_describe_weight_pin_includes_repo_and_revision(self) -> None:
        settings = HunyuanSettings(
            model_repo="tencent/Hunyuan3D-2.1",
            model_revision="abc123",
            cache_dir="/data/hunyuan",
        )
        payload = describe_hunyuan_weight_pin(settings)
        self.assertEqual(payload["repo_id"], "tencent/Hunyuan3D-2.1")
        self.assertEqual(payload["revision"], "abc123")
        self.assertEqual(payload["cache_dir"], "/data/hunyuan")

    @patch("huggingface_hub.snapshot_download")
    def test_ensure_hunyuan_weights_downloads_and_validates_sentinel(
        self,
        snapshot_download: object,
    ) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            checkpoint = root / "hunyuan3d-dit-v2-1"
            checkpoint.mkdir(parents=True)
            (checkpoint / "model.fp16.ckpt").write_bytes(b"ckpt")
            snapshot_download.return_value = str(root)

            local = ensure_hunyuan_weights(
                settings=HunyuanSettings(),
                cache_dir=root,
                token="test-token",
            )

            self.assertEqual(local, root)
            snapshot_download.assert_called_once()
            call_kwargs = snapshot_download.call_args.kwargs
            self.assertEqual(call_kwargs["repo_id"], HUNYUAN_MODEL_REPO)
            self.assertEqual(call_kwargs["revision"], HUNYUAN_MODEL_REVISION)
            self.assertEqual(call_kwargs["token"], "test-token")

    @patch("huggingface_hub.snapshot_download")
    def test_ensure_hunyuan_weights_rejects_incomplete_snapshot(
        self,
        snapshot_download: object,
    ) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            snapshot_download.return_value = str(root)
            with self.assertRaisesRegex(FileNotFoundError, "missing expected checkpoint"):
                ensure_hunyuan_weights(settings=HunyuanSettings(), cache_dir=root)


if __name__ == "__main__":
    unittest.main()
