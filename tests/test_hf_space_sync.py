from __future__ import annotations

import unittest

from imageezgen3d.hf_cli import deploy_commit_message


class HfSpaceSyncTests(unittest.TestCase):
    def test_deploy_commit_message_uses_tag_name(self) -> None:
        message = deploy_commit_message(
            {"GITHUB_REF": "refs/tags/v1.2.3", "GITHUB_EVENT_NAME": "push"}
        )
        self.assertEqual(message, "Deploy ImageEZGen3D v1.2.3")

    def test_deploy_commit_message_uses_default_on_branch_push(self) -> None:
        message = deploy_commit_message(
            {
                "GITHUB_REF": "refs/heads/main",
                "GITHUB_EVENT_NAME": "push",
            }
        )
        self.assertEqual(message, "Deploy ImageEZGen3D")


if __name__ == "__main__":
    unittest.main()
