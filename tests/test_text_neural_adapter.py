from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from imageezgen3d.adapters.base import GenerationRequest
from imageezgen3d.adapters.text_neural import (
    TextNeuralPlaceholderAdapter,
    _run_text_neural_inference_on_gpu,
    resolve_text_neural_configured,
)


def _sample_request(tmp: Path) -> GenerationRequest:
    return GenerationRequest(
        run_dir=tmp,
        processed_image=None,
        view_images={},
        quality="draft",
        seed=42,
        input_modality="text",
        prompt_text="A low-poly tree",
    )


class TextNeuralAdapterTests(unittest.TestCase):
    def test_adapter_defaults_to_disabled(self) -> None:
        self.assertFalse(
            TextNeuralPlaceholderAdapter(configured=False).capabilities.configured
        )

    def test_resolve_text_neural_configured_honors_env(self) -> None:
        with patch.dict(
            os.environ, {"IMAGEEZ_TEXT_NEURAL_CONFIGURED": "true"}, clear=True
        ):
            self.assertTrue(resolve_text_neural_configured())

    def test_adapter_honors_configured_constructor_flag(self) -> None:
        self.assertTrue(
            TextNeuralPlaceholderAdapter(configured=True).capabilities.configured
        )

    def test_generate_raises_while_disabled(self) -> None:
        adapter = TextNeuralPlaceholderAdapter()
        with tempfile.TemporaryDirectory() as directory:
            request = _sample_request(Path(directory))
            with self.assertRaises(RuntimeError) as context:
                adapter.generate(request)
        self.assertIn("intentionally disabled", str(context.exception))

    def test_generate_raises_not_implemented_when_configured(self) -> None:
        adapter = TextNeuralPlaceholderAdapter(configured=True)
        with tempfile.TemporaryDirectory() as directory:
            request = _sample_request(Path(directory))
            with self.assertRaises(NotImplementedError):
                adapter.generate(request)

    def test_gpu_inference_shell_raises_not_implemented(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            request = _sample_request(Path(directory))
            with self.assertRaises(NotImplementedError):
                _run_text_neural_inference_on_gpu(request)

    def test_gpu_function_is_callable_without_spaces(self) -> None:
        self.assertTrue(callable(_run_text_neural_inference_on_gpu))


if __name__ == "__main__":
    unittest.main()
