from __future__ import annotations

import unittest

from imageezgen3d.hosted_validation import hosted_validation_section


class HostedValidationSectionTests(unittest.TestCase):
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
