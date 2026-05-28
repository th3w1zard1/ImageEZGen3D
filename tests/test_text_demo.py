from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from imageezgen3d.adapters.base import GenerationRequest
from imageezgen3d.adapters.text_demo import TextDemoAdapter
from imageezgen3d.config import AppConfig
from imageezgen3d.generation_pipeline import TEXT_STUB_DISCLAIMER
from imageezgen3d.orchestrator import ImageEZOrchestrator


class TextDemoAdapterTests(unittest.TestCase):
    def test_adapter_requires_prompt(self) -> None:
        adapter = TextDemoAdapter()
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(ValueError, "non-empty prompt"):
                adapter.generate(
                    GenerationRequest(
                        run_dir=Path(tmp),
                        processed_image=None,
                        view_images={},
                        quality="draft",
                        seed=0,
                        input_modality="text",
                        prompt_text="",
                    )
                )

    def test_adapter_produces_exports(self) -> None:
        adapter = TextDemoAdapter()
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = Path(tmp)
            (run_dir / "exports").mkdir()
            result = adapter.generate(
                GenerationRequest(
                    run_dir=run_dir,
                    processed_image=None,
                    view_images={},
                    quality="draft",
                    seed=1,
                    decimation_target=25_000,
                    input_modality="text",
                    lane="draft",
                    prompt_text="A ceramic mug with a curved handle",
                )
            )
            self.assertEqual(result.adapter, "text-demo")
            self.assertTrue(result.artifacts["glb"].exists())
            self.assertIn("preview_disclaimer", result.metadata)
            self.assertEqual(result.metadata["preview_disclaimer"], TEXT_STUB_DISCLAIMER)

    def test_orchestrator_text_run_writes_generation_block(self) -> None:
        orchestrator = ImageEZOrchestrator(AppConfig())
        with tempfile.TemporaryDirectory() as tmp:
            orchestrator.store.root = Path(tmp)
            result = orchestrator.generate(
                primary_image=None,
                input_modality="text",
                prompt_text="Low-poly tree with a thick trunk",
                lane="draft",
            )
            generation = result["parameters"]["generation"]
            self.assertEqual(generation["input_modality"], "text")
            self.assertEqual(generation["lane"], "draft")
            self.assertEqual(result["parameters"]["selected_adapter"], "text-demo")
            self.assertEqual(
                result["parameters"]["preview_disclaimer"],
                TEXT_STUB_DISCLAIMER,
            )
            stages = {
                item["name"]: item["status"]
                for item in generation["pipeline_stages"]
            }
            self.assertEqual(stages["shape"], "succeeded")

    def test_adapter_choices_include_text_demo(self) -> None:
        orchestrator = ImageEZOrchestrator(AppConfig())
        self.assertIn("text-demo", orchestrator.adapter_choices())
