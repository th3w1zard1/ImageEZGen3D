from __future__ import annotations

import unittest

from imageezgen3d.forge_sync import build_forgejo_remote_url, build_gitlab_remote_url


class ForgeSyncTests(unittest.TestCase):
    def test_build_gitlab_remote_url_uses_oauth2_username(self) -> None:
        remote_url = build_gitlab_remote_url(
            "https://gitlab.com",
            "th3w1zard1/ImageEZGen3D",
            "token-value",
        )
        self.assertEqual(
            remote_url,
            "https://oauth2:token-value@gitlab.com/th3w1zard1/ImageEZGen3D.git",
        )

    def test_build_forgejo_remote_url_includes_username(self) -> None:
        remote_url = build_forgejo_remote_url(
            "https://codeberg.org",
            "th3w1zard1/ImageEZGen3D",
            "th3w1zard1",
            "token-value",
        )
        self.assertEqual(
            remote_url,
            "https://th3w1zard1:token-value@codeberg.org/th3w1zard1/ImageEZGen3D.git",
        )


if __name__ == "__main__":
    unittest.main()