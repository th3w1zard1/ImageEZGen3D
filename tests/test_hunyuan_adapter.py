from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from imageezgen3d.adapters.base import GenerationRequest
from imageezgen3d.adapters.hunyuan import (
    HunyuanPlaceholderAdapter,
    _run_hunyuan_inference_on_gpu,
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
    def test_adapter_remains_disabled(self) -> None:
        self.assertFalse(HunyuanPlaceholderAdapter().capabilities.configured)

    def test_generate_raises_while_disabled(self) -> None:
        adapter = HunyuanPlaceholderAdapter()
        with tempfile.TemporaryDirectory() as directory:
            request = _sample_request(Path(directory))
            with self.assertRaises(RuntimeError) as context:
                adapter.generate(request)
        self.assertIn("intentionally disabled", str(context.exception))

    def test_gpu_inference_shell_raises_not_implemented(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            request = _sample_request(Path(directory))
            with self.assertRaises(NotImplementedError):
                _run_hunyuan_inference_on_gpu(request)

    def test_gpu_function_is_callable_without_spaces(self) -> None:
        self.assertTrue(callable(_run_hunyuan_inference_on_gpu))


if __name__ == "__main__":
    unittest.main()
