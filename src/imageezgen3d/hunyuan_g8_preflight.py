from __future__ import annotations

import re
from typing import Any

_NEURAL_MARKERS = ("hosted zerogpu", "hunyuan-zerogpu", "neural reconstruction")


def validate_g8_cpu_fallback_status(status_markdown: str) -> list[str]:
    """Validate hosted CPU fallback status is honest (G8 while Hunyuan disabled)."""
    issues: list[str] = []
    text = str(status_markdown or "")
    lower = text.lower()

    if "cpu-demo" not in lower and "local cpu preview" not in lower:
        issues.append(
            "G8 fallback smoke must label cpu-demo or Local CPU Preview in status"
        )
    if "fallback" not in lower:
        issues.append("G8 status must document fallback (Fallback: or fallback_reason)")
    if "preview" not in lower and "disclaimer" not in lower:
        issues.append("G8 status must reference preview disclaimer")

    for marker in _NEURAL_MARKERS:
        if marker in lower and "not enabled" not in lower:
            issues.append(
                f"G8 cpu fallback status must not imply successful neural path ({marker})"
            )

    return issues


def _hosted_validation_section(text: str, heading: str) -> str:
    pattern = rf"## {re.escape(heading)}\s*\n(.*?)(?=\n## |\Z)"
    match = re.search(pattern, text, re.DOTALL)
    return match.group(1) if match else ""


def g8_enablement_validation_passed(hosted_text: str) -> bool:
    """True when ## G8 validation records post-enablement UX re-verify."""
    section = _hosted_validation_section(hosted_text, "G8 validation")
    if not section:
        return False
    return "G8_STATUS: PASS" in section


def format_g8_issues(issues: list[str]) -> dict[str, Any]:
    return {"ok": not issues, "issues": issues}
