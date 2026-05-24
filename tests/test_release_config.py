from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from imageezgen3d.release_config import (
    load_release_settings,
    resolve_default_branch_names,
    resolve_image_tags,
    resolve_registry_image,
    resolve_repository_ref,
    resolve_target_enablement,
    resolve_target_repo_slug,
)


class ReleaseConfigTests(unittest.TestCase):
    def test_load_release_defaults_when_missing(self) -> None:
        settings = load_release_settings(Path("missing.toml"))
        self.assertTrue(settings.forge.gitlab.enabled)
        self.assertTrue(settings.forge.huggingface.enabled)
        self.assertTrue(settings.registry.ghcr.enabled)
        self.assertFalse(settings.registry.dockerhub.enabled)
        self.assertEqual(resolve_default_branch_names(settings), ("main", "master"))

    def test_load_release_from_pyproject_sections(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "pyproject.toml"
            path.write_text(
                "[tool.imageezgen3d.release.repository]\n"
                "owner = 'demo-owner'\n"
                "repo = 'demo-repo'\n"
                "[tool.imageezgen3d.release.branches]\n"
                "primary_branch = 'stable'\n"
                "fallback_branches = ['legacy']\n"
                "[tool.imageezgen3d.release.registry.ghcr]\n"
                "image = 'custom-image'\n",
                encoding="utf-8",
            )
            with patch.dict(os.environ, {}, clear=True):
                settings = load_release_settings(path)
            self.assertEqual(settings.repository.owner, "demo-owner")
            self.assertEqual(settings.repository.repo, "demo-repo")
            self.assertEqual(settings.branches.primary_branch, "stable")
            self.assertEqual(settings.branches.fallback_branches, ("legacy",))
            self.assertEqual(settings.registry.ghcr.image, "custom-image")

    def test_environment_overrides_release_settings(self) -> None:
        with patch.dict(
            os.environ,
            {
                "IMAGEEZ_RELEASE_PRIMARY_BRANCH": "production",
                "IMAGEEZ_RELEASE_FALLBACK_BRANCHES": "main,master",
                "IMAGEEZ_RELEASE_DOCKERHUB_ENABLED": "true",
            },
            clear=False,
        ):
            settings = load_release_settings(Path("missing.toml"))
        self.assertEqual(settings.branches.primary_branch, "production")
        self.assertEqual(settings.branches.fallback_branches, ("main", "master"))
        self.assertTrue(settings.registry.dockerhub.enabled)

    def test_resolve_repository_ref_uses_github_repository(self) -> None:
        settings = load_release_settings(Path("missing.toml"))
        resolved = resolve_repository_ref(
            settings,
            {"GITHUB_REPOSITORY": "th3w1zard1/ImageEZGen3D"},
        )
        self.assertEqual(resolved.owner, "th3w1zard1")
        self.assertEqual(resolved.repo, "ImageEZGen3D")

    def test_resolve_repository_ref_uses_git_remote_when_github_repository_missing(self) -> None:
        settings = load_release_settings(Path("missing.toml"))
        with patch(
            "imageezgen3d.release_config._remote_repository_slug",
            return_value="th3w1zard1/ImageEZGen3D",
        ):
            resolved = resolve_repository_ref(settings, {})
        self.assertEqual(resolved.owner, "th3w1zard1")
        self.assertEqual(resolved.repo, "ImageEZGen3D")

    def test_resolve_target_repo_slug_defaults_to_current_repository(self) -> None:
        settings = load_release_settings(Path("missing.toml"))
        slug = resolve_target_repo_slug(
            settings,
            env={"GITHUB_REPOSITORY": "th3w1zard1/ImageEZGen3D"},
        )
        self.assertEqual(slug, "th3w1zard1/ImageEZGen3D")

    def test_resolve_target_repo_slug_uses_git_remote_when_environment_missing(self) -> None:
        settings = load_release_settings(Path("missing.toml"))
        with patch(
            "imageezgen3d.release_config._remote_repository_slug",
            return_value="th3w1zard1/ImageEZGen3D",
        ):
            slug = resolve_target_repo_slug(settings, env={})
        self.assertEqual(slug, "th3w1zard1/ImageEZGen3D")

    def test_resolve_registry_image_uses_lowercase_defaults(self) -> None:
        settings = load_release_settings(Path("missing.toml"))
        image = resolve_registry_image(
            settings,
            settings.registry.ghcr,
            {"GITHUB_REPOSITORY": "Th3W1zard1/ImageEZGen3D"},
        )
        self.assertEqual(image, "ghcr.io/th3w1zard1/imageezgen3d")

    def test_resolve_image_tags_defaults_to_latest_on_default_branch(self) -> None:
        settings = load_release_settings(Path("missing.toml"))
        resolution = resolve_image_tags(
            settings,
            env={
                "GITHUB_EVENT_NAME": "push",
                "GITHUB_REF": "refs/heads/main",
                "GITHUB_SHA": "1234567890abcdef",
            },
        )
        self.assertEqual(resolution.primary_tag, "latest")
        self.assertEqual(resolution.additional_tags, ("sha-1234567",))
        self.assertTrue(resolution.publish_latest)
        self.assertEqual(resolution.source, "default_branch")

    def test_resolve_image_tags_uses_pr_prefix_for_pull_requests(self) -> None:
        settings = load_release_settings(Path("missing.toml"))
        resolution = resolve_image_tags(
            settings,
            env={
                "GITHUB_EVENT_NAME": "pull_request",
                "GITHUB_REF": "refs/pull/42/merge",
                "GITHUB_SHA": "abcdef0123456789",
            },
        )
        self.assertEqual(resolution.primary_tag, "pr-42")
        self.assertEqual(resolution.additional_tags, ("sha-abcdef0",))
        self.assertFalse(resolution.publish_latest)

    def test_resolve_image_tags_prefers_explicit_input(self) -> None:
        settings = load_release_settings(Path("missing.toml"))
        resolution = resolve_image_tags(
            settings,
            env={
                "GITHUB_EVENT_NAME": "workflow_dispatch",
                "GITHUB_REF": "refs/heads/main",
                "GITHUB_SHA": "fedcba9876543210",
            },
            image_tag="release-1.2.3",
        )
        self.assertEqual(resolution.primary_tag, "release-1.2.3")
        self.assertEqual(resolution.source, "input")
        self.assertFalse(resolution.publish_latest)

    def test_resolve_target_enablement_best_effort_skip(self) -> None:
        decision = resolve_target_enablement(
            enabled=True,
            required=False,
            credentials_present=False,
        )
        self.assertEqual(decision.action, "skip")
        self.assertIn("credentials", decision.reason)

    def test_resolve_target_enablement_forced_target_fails_without_credentials(self) -> None:
        decision = resolve_target_enablement(
            enabled=True,
            required=False,
            credentials_present=False,
            force=True,
        )
        self.assertEqual(decision.action, "fail")
        self.assertIn("forced", decision.reason)


if __name__ == "__main__":
    unittest.main()