from __future__ import annotations

import unittest

from imageezgen3d.hunyuan_g8_preflight import (
    g8_enablement_validation_passed,
    validate_g8_cpu_fallback_status,
)


def _honest_cpu_status() -> str:
    return "\n".join(
        [
            "Run `20260527-120000-abcdef01` complete.",
            "- **Export budget:** up to 25,000 faces",
            "- **Backend used:** Local CPU Preview",
            "- **Fallback:** ZeroGPU adapter is not enabled yet.",
            "- **Preview disclaimer:** CPU preview fallback is active.",
            "Downloads: manifest, glb, obj",
        ]
    )


class HunyuanG8PreflightTests(unittest.TestCase):
    def test_validate_g8_cpu_fallback_accepts_honest_status(self) -> None:
        self.assertEqual(validate_g8_cpu_fallback_status(_honest_cpu_status()), [])

    def test_validate_g8_rejects_missing_fallback(self) -> None:
        status = "\n".join(
            [
                "Run `20260527-120000-abcdef01` complete.",
                "- **Backend used:** Local CPU Preview",
                "- **Preview disclaimer:** CPU preview is active.",
            ]
        )
        issues = validate_g8_cpu_fallback_status(status)
        self.assertTrue(any("fallback" in issue.lower() for issue in issues))

    def test_validate_g8_rejects_neural_only_claim(self) -> None:
        status = "\n".join(
            [
                "Run `20260527-120000-abcdef01` complete.",
                "- **Backend used:** Hosted ZeroGPU (hunyuan-zerogpu)",
                "- **Fallback:** none",
                "preview disclaimer",
            ]
        )
        issues = validate_g8_cpu_fallback_status(status)
        self.assertTrue(any("neural" in issue.lower() or "hunyuan" in issue for issue in issues))

    def test_g8_enablement_section_passes_when_documented(self) -> None:
        text = "## G8 validation\n\nG8_STATUS: PASS\n- CPU fallback honesty re-verified\n"
        self.assertTrue(g8_enablement_validation_passed(text))

    def test_g8_enablement_ignores_prose(self) -> None:
        self.assertFalse(
            g8_enablement_validation_passed("Plan notes G8_STATUS: PASS in prose\n")
        )

    def test_g8_placeholder_open_does_not_close_gate(self) -> None:
        text = "\n".join(
            [
                "## G8 validation",
                "",
                "G8_STATUS: OPEN",
                "Interim CPU fallback honesty via golden smoke only",
            ]
        )
        self.assertFalse(g8_enablement_validation_passed(text))


if __name__ == "__main__":
    unittest.main()
