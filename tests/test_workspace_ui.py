from __future__ import annotations

import unittest

from imageezgen3d import workspace_ui


class WorkspaceUiTests(unittest.TestCase):
    def test_credit_footer_renders_estimate(self) -> None:
        html = workspace_ui.credit_footer_html(
            {"input_modality": "image", "lane": "draft"}
        )
        self.assertIn("credit-footer", html)
        self.assertIn("credits", html)

    def test_model_helper_includes_bear_warrior_sections(self) -> None:
        markdown = workspace_ui.model_helper_markdown()
        self.assertIn("Stylized Bear Warrior", markdown)
        self.assertIn("Character type", markdown)

    def test_pbr_strip_uses_filename_labels_not_img_tags(self) -> None:
        html = workspace_ui.pbr_channel_strip_html(
            {"pbr_base_color": "/tmp/run/pbr_base_color.png"}
        )
        self.assertIn("Base Color", html)
        self.assertIn("pbr_base_color.png", html)
        self.assertNotIn("<img", html)

    def test_viewer_action_bar_lists_meshy_actions(self) -> None:
        html = workspace_ui.viewer_action_bar_html()
        self.assertIn("Remesh", html)
        self.assertIn("Send to Animate", html)

    def test_mesh_stats_card_reads_mesh_report(self) -> None:
        html = workspace_ui.mesh_stats_card_html(
            {
                "topology": "triangle",
                "mesh_report": {
                    "face_count": 1200,
                    "vertex_count": 600,
                    "status": "ok",
                },
            }
        )
        self.assertIn("1200", html)
        self.assertIn("600", html)
        self.assertIn("triangle", html)


if __name__ == "__main__":
    unittest.main()
