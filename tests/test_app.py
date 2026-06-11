from __future__ import annotations

import unittest
from pathlib import Path
from unittest.mock import patch

import app
from imageezgen3d.orchestrator import PREVIEW_FALLBACK_DISCLAIMER, AdapterResolution
from imageezgen3d.runtime import RuntimeStatus
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
        self.assertIn("What backend ran", overview)
        self.assertIn("CPU fallback", overview)

    def test_history_overview_shows_idle_backend_chips_from_resolution(self) -> None:
        resolution = AdapterResolution(
            requested="auto",
            selected="cpu-demo",
            runtime=RuntimeStatus(
                requested_mode="auto",
                prefer_zerogpu=True,
                zerogpu_enabled=False,
                zerogpu_runtime_available=True,
                cpu_fallback_allowed=True,
                reason="adapter disabled",
            ),
            zerogpu_runnable=False,
            fallback_reason="ZeroGPU adapter is not enabled yet.",
            message="Using CPU preview fallback.",
        )
        overview = app._history_overview_html([], resolution=resolution)

        self.assertIn("What backend ran", overview)
        self.assertIn("Local CPU Preview", overview)
        self.assertIn("CPU fallback", overview)

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

    def test_history_inspect_html_composes_status_card_and_artifact_strip(self) -> None:
        html = app._history_inspect_html(
            {
                "run_id": "run-123",
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
                "artifacts": {"glb": "/tmp/mesh.glb", "obj": "/tmp/mesh.obj"},
            },
            missing_keys=[],
        )

        self.assertIn("run-status-card", html)
        self.assertIn("artifact-strip", html)
        self.assertIn("run-123", html)

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

    def test_create_tab_places_composer_before_starter_cards(self) -> None:
        source = Path(app.__file__).read_text(encoding="utf-8")
        create_section = source.split('with gr.Tab("Create"):')[1].split(
            'with gr.Tab("History")'
        )[0]
        composer_idx = create_section.index('elem_classes="composer-grid"')
        starter_idx = create_section.index('elem_classes="starter-card-row"')
        self.assertLess(composer_idx, starter_idx)

    def test_create_and_history_tabs_expose_export_tier_downloads(self) -> None:
        source = Path(app.__file__).read_text(encoding="utf-8")
        create_section = source.split('with gr.Tab("Create"):')[1].split(
            'with gr.Tab("History")'
        )[0]
        history_section = source.split('with gr.Tab("History"):')[1].split(
            'with gr.Tab("Guide")'
        )[0]

        self.assertIn("UI_ARTIFACT_LABELS[key]", create_section)
        self.assertIn("UI_ARTIFACT_LABELS[key]", history_section)
        self.assertIn("create_artifact_files", create_section)
        self.assertIn("history_artifact_files", history_section)

        self.assertIn("resolve_gradio_download_keys", source)
        self.assertIn(
            "*[create_artifact_files[key] for key in download_keys]",
            source,
        )
        self.assertIn(
            "*[history_artifact_files[key] for key in download_keys]",
            source,
        )

    def test_advanced_controls_expose_background_job_queue_toggle(self) -> None:
        source = Path(app.__file__).read_text(encoding="utf-8")
        advanced_section = source.split('"Advanced run controls"')[1].split(
            "starter-card-row"
        )[0]
        self.assertIn("Queue as background job", advanced_section)
        self.assertIn("queue_as_job", advanced_section)

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

    def _sample_resolution(
        self,
        *,
        selected: str = "cpu-demo",
        fallback_reason: str | None = None,
    ) -> AdapterResolution:
        return AdapterResolution(
            requested="auto",
            selected=selected,
            runtime=RuntimeStatus(
                requested_mode="auto",
                prefer_zerogpu=True,
                zerogpu_enabled=True,
                zerogpu_runtime_available=True,
                cpu_fallback_allowed=True,
                reason="ZeroGPU runtime is available and preferred.",
            ),
            zerogpu_runnable=False,
            message="Using CPU preview fallback.",
            fallback_reason=fallback_reason,
        )

    def test_is_preview_fallback_requires_cpu_demo_and_reason(self) -> None:
        self.assertTrue(
            app._is_preview_fallback(
                self._sample_resolution(fallback_reason="adapter disabled")
            )
        )
        self.assertFalse(
            app._is_preview_fallback(
                self._sample_resolution(
                    selected="hunyuan-zerogpu", fallback_reason="adapter disabled"
                )
            )
        )
        self.assertFalse(
            app._is_preview_fallback(self._sample_resolution(fallback_reason=None))
        )

    def test_fallback_notice_html_surfaces_reason_and_disclaimer(self) -> None:
        html = app._fallback_notice_html(
            self._sample_resolution(
                fallback_reason="ZeroGPU adapter is not enabled yet."
            )
        )

        self.assertIn("CPU preview fallback is active", html)
        self.assertIn("ZeroGPU adapter is not enabled yet.", html)
        self.assertIn(PREVIEW_FALLBACK_DISCLAIMER, html)

    def test_fallback_notice_html_empty_when_fallback_not_preview(self) -> None:
        self.assertEqual(
            app._fallback_notice_html(
                self._sample_resolution(
                    selected="hunyuan-zerogpu",
                    fallback_reason="adapter disabled",
                )
            ),
            "",
        )

    def test_format_report_includes_preview_disclaimer_for_cpu_fallback(self) -> None:
        report = app._format_report(
            {
                "stage": "done",
                "run_id": "run-456",
                "adapter": "cpu-demo",
                "validation": {"score": 88, "issues": []},
                "mesh_report": {"status": "ok", "warnings": []},
                "parameters": {
                    "fallback_reason": "ZeroGPU adapter is not enabled yet.",
                    "selected_adapter": "cpu-demo",
                },
            }
        )

        self.assertIn("**Preview Disclaimer**", report)
        self.assertIn(PREVIEW_FALLBACK_DISCLAIMER, report)
        self.assertIn("**Runtime Fallback**", report)

    def test_format_report_uses_manifest_preview_disclaimer_when_present(self) -> None:
        custom = "Custom disclaimer from manifest."
        report = app._format_report(
            {
                "stage": "done",
                "run_id": "run-789",
                "adapter": "cpu-demo",
                "validation": {"score": 90, "issues": []},
                "mesh_report": {"status": "ok", "warnings": []},
                "parameters": {
                    "fallback_reason": "ZeroGPU adapter is not enabled yet.",
                    "preview_disclaimer": custom,
                    "selected_adapter": "cpu-demo",
                },
            }
        )

        self.assertIn(custom, report)
        self.assertNotIn(PREVIEW_FALLBACK_DISCLAIMER, report)

    def test_comprehension_exit_explains_preview_mesh_and_next_steps(self) -> None:
        summary = app._comprehension_exit_markdown(
            {
                "adapter": "cpu-demo",
                "parameters": {
                    "quality": "draft",
                    "selected_adapter": "cpu-demo",
                    "fallback_reason": "ZeroGPU adapter is not enabled yet.",
                },
            }
        )

        self.assertIn("## What happened", summary)
        self.assertIn("Output tier", summary)
        self.assertIn("Preview geometry", summary)
        self.assertIn("Suggested next steps", summary)

    def test_quality_intake_html_lists_all_tiers(self) -> None:
        html = app._quality_intake_html("draft")

        self.assertIn("Choose your output tier", html)
        self.assertIn("Draft (selected)", html)
        self.assertIn("Balanced", html)
        self.assertIn("High", html)

    def test_hero_shell_includes_output_tier_chip(self) -> None:
        html = app._hero_shell_html(
            "ImageEZGen3D",
            self._sample_resolution(),
            quality_name="balanced",
        )

        self.assertIn("Output tier", html)
        self.assertIn("Balanced", html)

    def test_format_report_includes_comprehension_exit_and_output_tier(self) -> None:
        report = app._format_report(
            {
                "stage": "done",
                "run_id": "run-comp",
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
