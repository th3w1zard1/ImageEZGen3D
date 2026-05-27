from __future__ import annotations

import re
from dataclasses import dataclass
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
    return evaluate_g8_enablement_status(hosted_text).documented


@dataclass(frozen=True)
class G8EnablementStatus:
    """Structured G8 closure state for CI artifacts and enablement preflight."""

    section_present: bool
    documented: bool
    interim_open: bool
    gate_status: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "section_present": self.section_present,
            "documented": self.documented,
            "interim_open": self.interim_open,
            "gate_status": self.gate_status,
        }


def evaluate_g8_enablement_status(
    hosted_text: str,
    *,
    g8_gate_status: str | None = None,
) -> G8EnablementStatus:
    """Summarize ## G8 validation section and admission gate G8 status."""
    section = _hosted_validation_section(hosted_text, "G8 validation")
    section_present = bool(section)
    interim_open = section_present and "G8_STATUS: OPEN" in section
    documented = (
        section_present
        and not interim_open
        and "G8_STATUS: PASS" in section
    )
    gate_status = g8_gate_status if g8_gate_status is not None else "unknown"
    return G8EnablementStatus(
        section_present=section_present,
        documented=documented,
        interim_open=interim_open,
        gate_status=gate_status,
    )


def format_g8_issues(issues: list[str]) -> dict[str, Any]:
    return {"ok": not issues, "issues": issues}
