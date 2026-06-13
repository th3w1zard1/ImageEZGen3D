from __future__ import annotations

import re
import unittest
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[1]
_PARITY_MATRIX = _REPO_ROOT / "docs/reference/meshy/PARITY-MATRIX.md"
_PLANS_DIR = _REPO_ROOT / "docs/plans"
_LEGACY_MESHY_GAP_PLAN_FILES = (
    "2026-06-03-185-feat-meshy-parity-gap-program-plan.md",
    "2026-06-03-189-feat-meshy-target-formats-api-plan.md",
    "2026-06-03-190-feat-meshy-pbr-map-file-export-plan.md",
    "2026-06-03-191-feat-meshy-preview-refine-lanes-plan.md",
    "2026-06-03-192-feat-meshy-retexture-adapter-hook-plan.md",
)


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


def _meshy_parity_plan_paths() -> list[Path]:
    return sorted(
        path
        for path in _PLANS_DIR.glob("*.md")
        if _plan_frontmatter(path).get("program") == "meshy-parity"
    )


def _table_row_cells(row: str) -> list[str]:
    return [cell.strip() for cell in row.strip().strip("|").split("|")]


def _capability_table_rows(markdown: str) -> list[str]:
    lines = markdown.splitlines()
    rows: list[str] = []
    in_meshy_table = False
    for line in lines:
        if line.startswith("| Meshy capability"):
            in_meshy_table = True
            continue
        if in_meshy_table:
            if not line.startswith("|"):
                break
            if line.startswith("| ---"):
                continue
            rows.append(line)
    return rows


class MeshyParityMatrixTests(unittest.TestCase):
    def test_header_documents_program_through_phase_18(self) -> None:
        text = _PARITY_MATRIX.read_text(encoding="utf-8")
        self.assertIn("Phases U–18", text)
        self.assertIn("12–18", text)

    def test_capability_rows_are_not_partial_or_stub(self) -> None:
        text = _PARITY_MATRIX.read_text(encoding="utf-8")
        for row in _capability_table_rows(text):
            status_cell = _table_row_cells(row)[-1]
            self.assertNotIn(
                "**partial**",
                status_cell,
                msg=f"Unexpected partial status: {row}",
            )
            self.assertNotIn(
                "**stub**",
                status_cell,
                msg=f"Unexpected stub status: {row}",
            )

    def test_capability_status_parser_catches_stub_marker(self) -> None:
        sample = "| Example | 1 | `module` | **stub** |"
        status_cell = _table_row_cells(sample)[-1]
        self.assertIn("**stub**", status_cell)

    def test_viewer_row_mentions_empty_stub_list(self) -> None:
        text = _PARITY_MATRIX.read_text(encoding="utf-8")
        viewer_rows = [
            row
            for row in _capability_table_rows(text)
            if "Viewer action bar" in row
        ]
        self.assertEqual(len(viewer_rows), 1)
        self.assertIn("VIEWER_ACTION_STUBS", viewer_rows[0])

    def test_beyond_meshy_boolean_and_uv_are_real(self) -> None:
        text = _PARITY_MATRIX.read_text(encoding="utf-8")
        beyond_section = text.split("Beyond-Meshy extras", maxsplit=1)[-1]
        real_rows = re.findall(r"\| [^|]+ \| [^|]+ \| \*\*real\*\*", beyond_section)
        self.assertGreaterEqual(len(real_rows), 2)

    def test_meshy_parity_plans_are_marked_completed(self) -> None:
        plan_paths = _meshy_parity_plan_paths()
        self.assertGreaterEqual(len(plan_paths), 9)
        incomplete = [
            path.name
            for path in plan_paths
            if _plan_frontmatter(path).get("status") != "completed"
        ]
        self.assertEqual(
            incomplete,
            [],
            msg=f"meshy-parity plans must be completed: {incomplete}",
        )

    def test_legacy_meshy_gap_plans_are_marked_completed(self) -> None:
        incomplete = [
            name
            for name in _LEGACY_MESHY_GAP_PLAN_FILES
            if _plan_frontmatter(_PLANS_DIR / name).get("status") != "completed"
        ]
        self.assertEqual(
            incomplete,
            [],
            msg=f"legacy meshy gap plans must be completed: {incomplete}",
        )


if __name__ == "__main__":
    unittest.main()
