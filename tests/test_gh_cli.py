from __future__ import annotations

import unittest

from imageezgen3d.gh_cli import gh_cli_status


class GhCliTests(unittest.TestCase):
    def test_recommended_commands_include_release_flow(self) -> None:
        status = gh_cli_status("owner/repo", release_tag="sha-abcdef0")
        joined = "\n".join(status.recommended_commands)
        self.assertIn("gh auth status", joined)
        self.assertIn("gh repo view owner/repo", joined)
        self.assertIn("gh workflow list --repo owner/repo", joined)
        self.assertIn("gh release view sha-abcdef0 --repo owner/repo", joined)
        self.assertIn("gh release create sha-abcdef0 --repo owner/repo", joined)
        self.assertIn("gh release upload sha-abcdef0 dist/runtime-artifacts/runtime-artifacts.tgz --repo owner/repo --clobber", joined)


if __name__ == "__main__":
    unittest.main()