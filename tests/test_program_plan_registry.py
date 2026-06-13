from __future__ import annotations

import re
import unittest
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[1]
_PLANS_DIR = _REPO_ROOT / "docs/plans"


def _plan_frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    if not match:
        return {}
    frontmatter: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", maxsplit=1)
        frontmatter[key.strip()] = value.strip().strip('"')
    return frontmatter


class ProgramPlanRegistryTests(unittest.TestCase):
    def test_all_docs_plans_are_marked_completed(self) -> None:
        missing_status: list[str] = []
        not_completed: list[str] = []
        for path in sorted(_PLANS_DIR.glob("*.md")):
            status = _plan_frontmatter(path).get("status")
            if not status:
                missing_status.append(path.name)
            elif status != "completed":
                not_completed.append(f"{path.name}:{status}")
        self.assertEqual(
            missing_status,
            [],
            msg=f"plans missing status frontmatter: {missing_status}",
        )
        self.assertEqual(
            not_completed,
            [],
            msg=f"plans must be completed (found active/other): {not_completed}",
        )


if __name__ == "__main__":
    unittest.main()
