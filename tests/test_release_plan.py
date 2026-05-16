from __future__ import annotations

import unittest

from imageezgen3d.release_config import load_release_settings
from imageezgen3d.release_plan import build_release_plan, format_release_plan


class ReleasePlanTests(unittest.TestCase):
    def test_build_release_plan_uses_best_effort_defaults(self) -> None:
        settings = load_release_settings()
        plan = build_release_plan(
            settings=settings,
            env={
                "GITHUB_REPOSITORY": "th3w1zard1/ImageEZGen3D",
                "GITHUB_EVENT_NAME": "pull_request",
                "GITHUB_REF": "refs/pull/12/merge",
                "GITHUB_SHA": "1234567890abcdef",
            },
        )
        self.assertEqual(plan.repository, "th3w1zard1/ImageEZGen3D")
        self.assertEqual(plan.image.primary_tag, "pr-12")
        self.assertFalse(plan.image.publish_latest)
        actions = {target.name: target.action for target in plan.targets}
        self.assertEqual(actions["gitlab"], "skip")
        self.assertEqual(actions["codeberg"], "skip")
        self.assertEqual(actions["huggingface"], "skip")
        self.assertEqual(actions["ghcr"], "skip")
        self.assertEqual(actions["helm"], "render")

    def test_build_release_plan_promotes_targets_when_credentials_exist(self) -> None:
        settings = load_release_settings()
        plan = build_release_plan(
            settings=settings,
            env={
                "GITHUB_REPOSITORY": "th3w1zard1/ImageEZGen3D",
                "GITHUB_EVENT_NAME": "push",
                "GITHUB_REF": "refs/heads/main",
                "GITHUB_SHA": "abcdef0123456789",
                "GITHUB_TOKEN": "github-token",
                "GITLAB_TOKEN": "gitlab-token",
                "CODEBERG_TOKEN": "codeberg-token",
                "HF_TOKEN": "hf-token",
            },
        )
        actions = {target.name: target.action for target in plan.targets}
        self.assertEqual(actions["gitlab"], "push")
        self.assertEqual(actions["codeberg"], "push")
        self.assertEqual(actions["huggingface"], "push")
        self.assertEqual(actions["ghcr"], "push")
        self.assertEqual(plan.image.primary_tag, "latest")
        self.assertTrue(plan.image.publish_latest)

    def test_format_release_plan_contains_target_summary(self) -> None:
        settings = load_release_settings()
        plan = build_release_plan(
            settings=settings,
            env={
                "GITHUB_REPOSITORY": "th3w1zard1/ImageEZGen3D",
                "GITHUB_EVENT_NAME": "workflow_dispatch",
                "GITHUB_REF": "refs/heads/main",
                "GITHUB_SHA": "abcdef0123456789",
            },
            image_tag="demo-tag",
        )
        rendered = "\n".join(format_release_plan(plan))
        self.assertIn("image tag: demo-tag", rendered)
        self.assertIn("gitlab:", rendered)
        self.assertIn("github-release:", rendered)


if __name__ == "__main__":
    unittest.main()