from __future__ import annotations

import unittest

from imageezgen3d.generation_pipeline import (
    PipelineStageTracker,
    build_pipeline_spec,
    finalize_pipeline_stages_for_lane,
    preview_lane_export_formats,
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

    def test_preview_lane_defaults_to_draft_quality(self) -> None:
        lane, quality = resolve_lane_and_quality(lane="preview", quality=None)
        self.assertEqual(lane, "preview")
        self.assertEqual(quality, "draft")

    def test_refine_lane_defaults_to_balanced_quality(self) -> None:
        lane, quality = resolve_lane_and_quality(lane="refine", quality=None)
        self.assertEqual(lane, "refine")
        self.assertEqual(quality, "balanced")

    def test_preview_lane_export_formats_subset(self) -> None:
        formats = preview_lane_export_formats(
            ("glb", "obj", "ply", "stl", "fbx", "usdz", "3mf")
        )
        self.assertEqual(formats, ("glb", "obj"))

    def test_finalize_preview_lane_skips_texture_and_pbr(self) -> None:
        tracker = PipelineStageTracker()
        finalize_pipeline_stages_for_lane(
            tracker,
            lane="preview",
            adapter="cpu-demo",
            adapter_note="preview mesh",
            pbr_available=False,
        )
        stages = {item["name"]: item for item in tracker.to_list()}
        self.assertEqual(stages["shape"]["status"], "succeeded")
        self.assertEqual(stages["texture"]["status"], "skipped")
        self.assertEqual(stages["pbr"]["status"], "skipped")
        self.assertIn("refine lane", stages["texture"]["notes"].lower())

    def test_finalize_refine_lane_marks_texture_when_pbr_available(self) -> None:
        tracker = PipelineStageTracker()
        finalize_pipeline_stages_for_lane(
            tracker,
            lane="refine",
            adapter="cpu-demo",
            adapter_note="refine mesh",
            pbr_available=True,
        )
        stages = {item["name"]: item for item in tracker.to_list()}
        self.assertEqual(stages["texture"]["status"], "succeeded")
        self.assertEqual(stages["pbr"]["status"], "pending")

    def test_text_modality_requires_prompt(self) -> None:
        with self.assertRaisesRegex(ValueError, "text prompt"):
            build_pipeline_spec(
                input_modality="text",
                lane="draft",
                quality=None,
                prompt_text="",
            )

    def test_multi_image_modality_maps_explicit_label(self) -> None:
        spec = build_pipeline_spec(
            input_modality="multi-image-to-3d",
            lane="draft",
            quality=None,
            prompt_text="",
        )
        self.assertEqual(spec.input_modality, "multi-image-to-3d")

    def test_staged_shape_texture_progression(self) -> None:
        tracker = PipelineStageTracker()
        tracker.mark_shape_running("hunyuan-zerogpu")
        tracker.mark_shape_succeeded_staged("hunyuan-zerogpu")
        tracker.mark_texture_running("hunyuan-zerogpu")
        tracker.mark_texture_succeeded("hunyuan-zerogpu")
        tracker.mark_export_succeeded()
        stages = {item["name"]: item["status"] for item in tracker.to_list()}
        self.assertEqual(stages["shape"], "succeeded")
        self.assertEqual(stages["texture"], "succeeded")
        self.assertEqual(stages["pbr"], "pending")
        self.assertEqual(stages["export"], "succeeded")

    def test_apply_stage_snapshot_replaces_tracker_state(self) -> None:
        tracker = PipelineStageTracker()
        snapshot = [
            {"name": "shape", "status": "succeeded", "adapter": "hunyuan-zerogpu", "notes": ""},
            {"name": "texture", "status": "succeeded", "adapter": "hunyuan-zerogpu", "notes": ""},
            {"name": "pbr", "status": "skipped", "adapter": None, "notes": "deferred"},
            {"name": "export", "status": "pending", "adapter": None, "notes": ""},
        ]
        tracker.apply_stage_snapshot(snapshot)
        self.assertEqual(tracker.stages[1]["status"], "succeeded")

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
