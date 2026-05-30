from __future__ import annotations

import argparse
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT / "src") not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT / "src"))

from imageezgen3d.hunyuan_neural_enablement_record import (  # noqa: E402
    verify_neural_enablement_fixture_files,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Verify neural-enablement-preflight fixture JSON files.",
    )
    parser.add_argument(
        "fixtures_dir",
        type=Path,
        nargs="?",
        default=Path("tests/fixtures"),
        help="Directory containing neural-enablement-preflight-*.json fixtures",
    )
    args = parser.parse_args(argv)

    issues = verify_neural_enablement_fixture_files(args.fixtures_dir.resolve())
    if issues:
        for issue in issues:
            print(f"issue={issue}", file=sys.stderr)
        return 1
    print("neural_enablement_record_fixtures=ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
