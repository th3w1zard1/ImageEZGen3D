from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from imageezgen3d.adapters.base import GenerationRequest
from imageezgen3d.adapters.hunyuan import (
    HunyuanPlaceholderAdapter,
    _run_hunyuan_inference_on_gpu,
    resolve_hunyuan_configured,
)


def _sample_request(tmp: Path) -> GenerationRequest:
    image = tmp / "input.png"
    image.write_bytes(b"\x89PNG\r\n\x1a\n")
    return GenerationRequest(
        run_dir=tmp,
        processed_image=image,
        view_images={},
        quality="draft",
        seed=42,
    )


class HunyuanAdapterTests(unittest.TestCase):
    def test_adapter_defaults_to_disabled(self) -> None:
        self.assertFalse(HunyuanPlaceholderAdapter(configured=False).capabilities.configured)

    def test_resolve_hunyuan_configured_honors_env(self) -> None:
        with patch.dict(os.environ, {"IMAGEEZ_HUNYUAN_CONFIGURED": "true"}, clear=True):
            self.assertTrue(resolve_hunyuan_configured())

    def test_adapter_honors_configured_constructor_flag(self) -> None:
        self.assertTrue(HunyuanPlaceholderAdapter(configured=True).capabilities.configured)

    def test_generate_raises_while_disabled(self) -> None:
        adapter = HunyuanPlaceholderAdapter()
        with tempfile.TemporaryDirectory() as directory:
            request = _sample_request(Path(directory))
            with self.assertRaises(RuntimeError) as context:
                adapter.generate(request)
        self.assertIn("intentionally disabled", str(context.exception))

    def test_generate_raises_not_implemented_when_configured(self) -> None:
        adapter = HunyuanPlaceholderAdapter(configured=True)
        with tempfile.TemporaryDirectory() as directory:
            request = _sample_request(Path(directory))
            with self.assertRaises(NotImplementedError):
                adapter.generate(request)

    def test_gpu_inference_shell_raises_not_implemented(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            request = _sample_request(Path(directory))
            with self.assertRaises(NotImplementedError):
                _run_hunyuan_inference_on_gpu(request)

    def test_gpu_function_is_callable_without_spaces(self) -> None:
        self.assertTrue(callable(_run_hunyuan_inference_on_gpu))


if __name__ == "__main__":
    unittest.main()
