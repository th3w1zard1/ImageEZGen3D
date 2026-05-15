from __future__ import annotations

import unittest

from imageezgen3d.hf_cli import hf_cli_status


class HfCliTests(unittest.TestCase):
    def test_recommended_commands_include_upload(self) -> None:
        status = hf_cli_status("user/space")
        joined = "\n".join(status.recommended_commands)
        self.assertIn("hf auth whoami", joined)
        self.assertIn("hf upload user/space", joined)


if __name__ == "__main__":
    unittest.main()
