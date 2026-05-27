from __future__ import annotations

import re
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[2]
HOSTED_VALIDATION_PATH = (
    _REPO_ROOT / "docs/knowledgebase/40-operational-risk/hosted-validation-2026-05-23.md"
)


def read_repo_text(path: Path) -> str:
    """Read a repository file as UTF-8 text; missing paths yield empty string."""
    if not path.is_file():
        return ""
    return path.read_text(encoding="utf-8")


def hosted_validation_section(text: str, heading: str) -> str:
    """Extract body of a `## {heading}` section from hosted-validation markdown."""
    pattern = rf"## {re.escape(heading)}\s*\n(.*?)(?=\n## |\Z)"
    match = re.search(pattern, text, re.DOTALL)
    return match.group(1) if match else ""
