from __future__ import annotations

import unittest

from imageezgen3d.generation_pipeline import (
    PipelineStageTracker,
    build_pipeline_spec,
    resolve_lane_and_quality,
)


class GenerationPipelineTests(unittest.TestCase):
    def test_resolve_lane_and_quality_defaults_to_draft(self) -> None:
        lane, quality = resolve_lane_and_quality(lane=None, quality=None)
        self.assertEqual(lane, "draft")
        self.assertEqual(quality, "draft")

    def test_production_lane_maps_to_balanced_when_quality_unset(self) -> None:
        lane, quality = resolve_lane_and_quality(lane="production", quality=None)
        self.assertEqual(lane, "production")
        self.assertEqual(quality, "balanced")

    def test_explicit_quality_overrides_lane_default(self) -> None:
        lane, quality = resolve_lane_and_quality(lane="production", quality="high")
        self.assertEqual(lane, "production")
        self.assertEqual(quality, "high")

    def test_text_modality_requires_prompt(self) -> None:
        with self.assertRaisesRegex(ValueError, "text prompt"):
            build_pipeline_spec(
                input_modality="text",
                lane="draft",
                quality=None,
                prompt_text="",
            )

    def test_pipeline_stages_mark_shape_and_skip_texture(self) -> None:
        tracker = PipelineStageTracker()
        tracker.mark_shape_running("text-demo")
        tracker.mark_shape_succeeded("text-demo", notes="ok")
        tracker.mark_export_succeeded()
        stages = {item["name"]: item["status"] for item in tracker.to_list()}
        self.assertEqual(stages["shape"], "succeeded")
        self.assertEqual(stages["texture"], "skipped")
        self.assertEqual(stages["pbr"], "skipped")
        self.assertEqual(stages["export"], "succeeded")
