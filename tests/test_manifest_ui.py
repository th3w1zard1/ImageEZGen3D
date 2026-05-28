from __future__ import annotations

import json
import unittest

from imageezgen3d import manifest_ui as mu
from imageezgen3d.orchestrator import PREVIEW_FALLBACK_DISCLAIMER


class ManifestUiTests(unittest.TestCase):
    def test_generation_summary_chips_show_modality_and_lane(self) -> None:
        html = mu.generation_summary_chips_html(
            {
                "generation": {
                    "input_modality": "text",
                    "lane": "production",
                }
            }
        )
        self.assertIn("Text prompt", html)
        self.assertIn("Production lane", html)

    def test_backend_label_for_text_demo(self) -> None:
        self.assertEqual(mu.backend_display_label("text-demo"), "Text-to-3D Stub")

    def test_backend_label_for_text_neural(self) -> None:
        self.assertEqual(mu.backend_display_label("text-neural"), "Text-to-3D Neural")

    def test_backend_rail_chips_show_adapter_and_fallback(self) -> None:
        html = mu.backend_rail_chips_html(
            adapter_key="cpu-demo",
            fallback_reason="ZeroGPU adapter is not enabled yet.",
        )

        self.assertIn("What backend ran", html)
        self.assertIn("Local CPU Preview", html)
        self.assertIn("CPU fallback", html)
        self.assertIn("ZeroGPU adapter is not enabled yet.", html)

    def test_fallback_banner_renders_for_cpu_fallback_parameters(self) -> None:
        html = mu.fallback_banner_html(
            {
                "selected_adapter": "cpu-demo",
                "fallback_reason": "ZeroGPU adapter is not enabled yet.",
            }
        )

        self.assertIn("CPU preview fallback is active", html)
        self.assertIn(PREVIEW_FALLBACK_DISCLAIMER, html)

    def test_run_status_card_includes_quality_badge_and_fallback(self) -> None:
        html = mu.run_status_card_html(
            {
                "run_id": "run-abc",
                "stage": "done",
                "adapter": "cpu-demo",
                "quality": "draft",
                "score": 91,
                "starter_flow": "Single Photo Draft",
                "fallback_reason": "adapter disabled",
                "parameters": {
                    "selected_adapter": "cpu-demo",
                    "fallback_reason": "adapter disabled",
                },
            }
        )

        self.assertIn("run-abc", html)
        self.assertIn("Draft tier", html)
        self.assertIn("Fallback", html)
        self.assertIn("Image", html)

    def test_run_status_card_includes_modality_when_present(self) -> None:
        html = mu.run_status_card_html(
            {
                "run_id": "run-text",
                "stage": "done",
                "adapter": "text-demo",
                "parameters": {
                    "generation": {
                        "input_modality": "text",
                        "lane": "draft",
                    }
                },
            }
        )
        self.assertIn("Text prompt", html)
        self.assertIn("Draft lane", html)

    def test_artifact_strip_marks_missing_keys(self) -> None:
        html = mu.artifact_strip_html(
            {"glb": "/tmp/mesh.glb", "obj": "/tmp/mesh.obj"},
            missing=["obj"],
        )

        self.assertIn("GLB", html)
        self.assertIn("available", html)
        self.assertIn("OBJ", html)
        self.assertIn("missing", html)

    def test_format_run_report_includes_comprehension_exit(self) -> None:
        report = mu.format_run_report_markdown(
            {
                "stage": "done",
                "run_id": "run-xyz",
                "adapter": "cpu-demo",
                "validation": {"score": 88, "issues": []},
                "mesh_report": {"status": "ok", "warnings": []},
                "parameters": {"quality": "balanced", "selected_adapter": "cpu-demo"},
            }
        )

        self.assertIn("## What happened", report)
        self.assertIn("Output tier: **Balanced**", report)

    def test_compare_runs_rejects_same_run_identity(self) -> None:
        payload = {
            "run_id": "run-a",
            "stage": "done",
            "adapter": "cpu-demo",
            "quality": "draft",
            "validation": {"score": 80},
            "artifacts": {"glb": "/tmp/a.glb"},
        }
        report = mu.compare_runs_markdown(payload, payload)

        self.assertIn("## Run comparison", report)
        self.assertIn("All compared fields match", report)

    def test_compare_runs_payload_lists_changed_fields(self) -> None:
        payload = mu.compare_runs_payload(
            {
                "run_id": "run-left",
                "adapter": "cpu-demo",
                "quality": "draft",
                "validation": {"score": 70},
                "parameters": {"quality": "draft"},
                "artifacts": {"glb": "/tmp/left.glb", "obj": "/tmp/left.obj"},
            },
            {
                "run_id": "run-right",
                "adapter": "hunyuan-zerogpu",
                "quality": "balanced",
                "validation": {"score": 88},
                "parameters": {"quality": "balanced"},
                "artifacts": {"glb": "/tmp/right.glb"},
            },
        )

        self.assertEqual(payload["left_run_id"], "run-left")
        self.assertIn("Backend", payload["changed_fields"])
        self.assertEqual(payload["artifacts_only_on_left"], ["obj"])

    def test_compare_runs_json_is_valid_payload(self) -> None:
        raw = mu.compare_runs_json(
            {"run_id": "a", "adapter": "cpu-demo", "artifacts": {}},
            {"run_id": "b", "adapter": "cpu-demo", "artifacts": {"glb": "/x"}},
        )
        parsed = json.loads(raw)
        self.assertEqual(parsed["left_run_id"], "a")
        self.assertIn("glb", parsed["artifacts_only_on_right"])

    def test_compare_runs_highlights_adapter_and_artifact_diffs(self) -> None:
        left = {
            "run_id": "run-left",
            "stage": "done",
            "adapter": "cpu-demo",
            "quality": "draft",
            "validation": {"score": 70},
            "parameters": {"quality": "draft", "selected_adapter": "cpu-demo"},
            "artifacts": {"glb": "/tmp/left.glb", "obj": "/tmp/left.obj"},
        }
        right = {
            "run_id": "run-right",
            "stage": "done",
            "adapter": "hunyuan-zerogpu",
            "quality": "balanced",
            "validation": {"score": 88},
            "parameters": {
                "quality": "balanced",
                "selected_adapter": "hunyuan-zerogpu",
            },
            "artifacts": {"glb": "/tmp/right.glb"},
        }
        report = mu.compare_runs_markdown(left, right)

        self.assertIn("### Changed", report)
        self.assertIn("**Backend**", report)
        self.assertIn("**Quality tier**", report)
        self.assertIn("Only on left: obj", report)


if __name__ == "__main__":
    unittest.main()
