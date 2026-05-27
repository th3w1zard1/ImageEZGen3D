from __future__ import annotations

import re


def hosted_validation_section(text: str, heading: str) -> str:
    """Extract body of a `## {heading}` section from hosted-validation markdown."""
    pattern = rf"## {re.escape(heading)}\s*\n(.*?)(?=\n## |\Z)"
    match = re.search(pattern, text, re.DOTALL)
    return match.group(1) if match else ""
