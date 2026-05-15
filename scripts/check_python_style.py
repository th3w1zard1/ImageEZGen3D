from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXCLUDED_PARTS = {".venv", "outputs", "tmp", ".history", ".mypy_cache", ".pytest_cache"}
CAPITAL_GENERIC_PATTERN = re.compile(
    r"\b(?:List|Dict|Tuple|Set|FrozenSet|Optional|Union)\["
)


def iter_python_files() -> list[Path]:
    files: list[Path] = []
    for path in ROOT.rglob("*.py"):
        if any(part in EXCLUDED_PARTS for part in path.relative_to(ROOT).parts):
            continue
        files.append(path)
    return sorted(files)


def main() -> None:
    failures: list[str] = []
    for path in iter_python_files():
        text = path.read_text(encoding="utf-8")
        first_line = text.splitlines()[0] if text.splitlines() else ""
        if first_line != "from __future__ import annotations":
            failures.append(
                f"{path.relative_to(ROOT)} must begin with future annotations"
            )
        if CAPITAL_GENERIC_PATTERN.search(text):
            failures.append(
                f"{path.relative_to(ROOT)} uses capitalized typing generics; use list/dict/tuple/set and | instead"
            )
    if failures:
        raise SystemExit("\n".join(failures))
    print(f"checked {len(iter_python_files())} Python files")


if __name__ == "__main__":
    main()
