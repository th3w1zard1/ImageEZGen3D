from __future__ import annotations

import unittest

from imageezgen3d.hosted_validation import (
    HOSTED_VALIDATION_PATH,
    hosted_validation_section,
    read_repo_text,
)


class HostedValidationSectionTests(unittest.TestCase):
    def test_read_repo_text_returns_empty_for_missing_path(self) -> None:
        self.assertEqual(read_repo_text(HOSTED_VALIDATION_PATH.parent / "missing.md"), "")

    def test_hosted_validation_path_exists(self) -> None:
        self.assertTrue(HOSTED_VALIDATION_PATH.is_file())

    def test_extracts_section_body_until_next_heading(self) -> None:
        text = "\n".join(
            [
                "## G7 validation",
                "",
                "G7_STATUS: OPEN",
                "",
                "## Plan 066",
                "prose",
            ]
        )
        section = hosted_validation_section(text, "G7 validation")
        self.assertIn("G7_STATUS: OPEN", section)
        self.assertNotIn("Plan 066", section)


if __name__ == "__main__":
    unittest.main()
