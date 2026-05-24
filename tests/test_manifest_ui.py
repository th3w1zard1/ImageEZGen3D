from __future__ import annotations

import unittest

from imageezgen3d import manifest_ui as mu
from imageezgen3d.orchestrator import PREVIEW_FALLBACK_DISCLAIMER


class ManifestUiTests(unittest.TestCase):
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


if __name__ == "__main__":
    unittest.main()
