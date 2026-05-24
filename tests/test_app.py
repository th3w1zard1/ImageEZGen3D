from __future__ import annotations

import unittest
from pathlib import Path
from unittest.mock import patch

import app
from imageezgen3d.storage import RunStore


class RepoLocalWorkspaceTests(unittest.TestCase):
    def test_backend_display_label_normalizes_runtime_ids(self) -> None:
        self.assertEqual(app._backend_display_label("cpu-demo"), "Local CPU Preview")
        self.assertEqual(
            app._backend_display_label("hunyuan-zerogpu"), "Hosted ZeroGPU"
        )

    def test_repo_sample_packs_group_generated_examples(self) -> None:
        packs = app._repo_sample_packs()

        self.assertEqual(
            [pack["key"] for pack in packs],
            ["shape-basics", "product-focus", "character-forms"],
        )
        self.assertEqual([pack["count"] for pack in packs], [2, 2, 2])
        self.assertEqual(packs[0]["example_labels"], ["Block", "Vase"])
        self.assertEqual(packs[1]["example_labels"], ["Canister", "Bottle"])
        self.assertEqual(packs[2]["example_labels"], ["Figurine", "Bust"])

    def test_sample_packs_note_describes_repo_local_behavior(self) -> None:
        note = app._sample_packs_note(app._repo_sample_packs())

        self.assertIn("Repo-local sample packs", note)
        self.assertIn("Shape Basics", note)
        self.assertIn("hosted runs", note)

    def test_prompt_template_card_html_surfaces_badge_and_starter(self) -> None:
        card_html = app._prompt_template_card_html(app._PROMPT_TEMPLATES[0])

        self.assertIn(app._PROMPT_TEMPLATES[0]["badge"], card_html)
        self.assertIn(app._PROMPT_TEMPLATES[0]["title"], card_html)
        self.assertIn(
            app._STARTER_FLOW_BY_KEY[app._PROMPT_TEMPLATES[0]["starter"]]["label"],
            card_html,
        )

    def test_history_overview_html_reports_latest_run(self) -> None:
        overview = app._history_overview_html(
            [
                {
                    "run_id": "run-123",
                    "adapter": "cpu-demo",
                    "starter_flow": "Single Photo Draft",
                    "fallback_reason": "zerogpu unavailable",
                },
                {
                    "run_id": "run-122",
                    "adapter": "cpu-demo",
                    "starter_flow": "Studio Product",
                },
            ]
        )

        self.assertIn("run-123", overview)
        self.assertIn("Local CPU Preview", overview)
        self.assertIn("Fallbacks logged", overview)

    def test_history_choice_label_uses_normalized_backend_name(self) -> None:
        label = app._history_choice_label(
            {
                "run_id": "run-123",
                "adapter": "hunyuan-zerogpu",
                "stage": "done",
                "score": 92,
            }
        )

        self.assertIn("Hosted ZeroGPU", label)
        self.assertNotIn("hunyuan-zerogpu", label)

    def test_prompt_templates_target_known_starters(self) -> None:
        self.assertEqual(len(app._PROMPT_TEMPLATES), 5)
        for template in app._PROMPT_TEMPLATES:
            starter_key = template["starter"]
            self.assertIn(starter_key, app._STARTER_FLOW_BY_KEY)
            self.assertEqual(
                template["quality"],
                app._STARTER_FLOW_BY_KEY[starter_key]["quality"],
            )
            self.assertTrue(str(template["brief"]).strip())

    def test_mode_summary_markdown_combines_path_and_quality(self) -> None:
        summary = app._mode_summary_markdown("single-photo-draft", "high")

        self.assertIn("Single Photo Draft", summary)
        self.assertIn("High mode", summary)
        self.assertIn("Capture hint:", summary)

    def test_verified_artifact_state_filters_missing_files(self) -> None:
        store = RunStore(Path.cwd() / "outputs")
        with patch.object(store, "artifact_value", side_effect=["/tmp/mesh.glb", None]):
            verified, missing = app._verified_artifact_state(
                store,
                {"glb": "/tmp/mesh.glb", "obj": "/tmp/missing.obj"},
            )

        self.assertEqual(verified, {"glb": "/tmp/mesh.glb"})
        self.assertEqual(missing, ["obj"])

    def test_generation_pending_report_mentions_verified_outputs(self) -> None:
        self.assertIn("verified output files", app._generation_pending_report())

    def test_stale_artifact_report_lists_missing_keys(self) -> None:
        report = app._stale_artifact_report("run-123", ["glb", "obj"])

        self.assertIn("run-123", report)
        self.assertIn("`glb`", report)
        self.assertIn("`obj`", report)


if __name__ == "__main__":
    unittest.main()
