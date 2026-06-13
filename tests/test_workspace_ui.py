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

    def test_viewer_action_stub_bar_empty_when_all_wired(self) -> None:
        self.assertEqual(workspace_ui.VIEWER_ACTION_STUBS, ())
        self.assertEqual(workspace_ui.viewer_action_stub_bar_html(), "")

    def test_viewer_action_bar_lists_all_wired_actions(self) -> None:
        html = workspace_ui.viewer_action_bar_html()
        self.assertIn("Retry", html)
        self.assertIn("Send to Animate", html)
        self.assertIn("Multi-Color 3MF", html)
        self.assertIn("viewer-action-bar", html)

    def test_wired_viewer_mesh_ops_cover_remesh_and_print(self) -> None:
        modalities = {item[0] for item in workspace_ui.WIRED_VIEWER_MESH_OPS}
        self.assertEqual(
            modalities,
            {
                "remesh",
                "print-analyze",
                "print-repair",
                "print-multi-color",
                "unwrap-uv",
            },
        )

    def test_wired_viewer_generation_ops_include_retexture(self) -> None:
        labels = {item[1] for item in workspace_ui.WIRED_VIEWER_GENERATION_OPS}
        self.assertIn("Edit Texture", labels)

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

    def test_filter_asset_runs_by_phase_and_search(self) -> None:
        runs = [
            {
                "run_id": "run-gen",
                "adapter": "cpu-demo",
                "starter_flow": "Block",
                "input_modality": "image",
            },
            {
                "run_id": "run-remesh",
                "adapter": "cpu-demo",
                "starter_flow": "Remesh",
                "input_modality": "remesh",
            },
            {
                "run_id": "run-print",
                "adapter": "cpu-demo",
                "input_modality": "print-analyze",
            },
        ]
        mesh_only = workspace_ui.filter_asset_runs(runs, phase="mesh-ops")
        self.assertEqual(
            {item["run_id"] for item in mesh_only},
            {"run-remesh", "run-print"},
        )
        uv_only = workspace_ui.filter_asset_runs(
            [
                *runs,
                {"run_id": "run-uv", "adapter": "cpu-demo", "input_modality": "unwrap-uv"},
            ],
            phase="mesh-ops",
        )
        self.assertIn("run-uv", {item["run_id"] for item in uv_only})
        print_only = workspace_ui.filter_asset_runs(runs, phase="print")
        self.assertEqual([item["run_id"] for item in print_only], ["run-print"])
        searched = workspace_ui.filter_asset_runs(runs, search="block")
        self.assertEqual([item["run_id"] for item in searched], ["run-gen"])

    def test_assets_gallery_groups_generation_and_mesh_ops(self) -> None:
        html = workspace_ui.assets_gallery_html(
            [
                {"run_id": "a", "adapter": "cpu-demo", "input_modality": "image"},
                {"run_id": "b", "adapter": "cpu-demo", "input_modality": "remesh"},
            ],
            total_count=2,
        )
        self.assertIn("Generation", html)
        self.assertIn("Mesh operations", html)
        self.assertIn("assets-run-card", html)


if __name__ == "__main__":
    unittest.main()
