from __future__ import annotations

import argparse
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT / "src") not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT / "src"))

from imageezgen3d.hunyuan_g9_enablement_evidence_record import (  # noqa: E402
    verify_g9_enablement_evidence_fixture_files,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Verify g9-enablement-evidence fixture JSON files.",
    )
    parser.add_argument(
        "fixtures_dir",
        type=Path,
        nargs="?",
        default=Path("tests/fixtures"),
        help="Directory containing g9-enablement-evidence-*.json fixtures",
    )
    args = parser.parse_args(argv)

    issues = verify_g9_enablement_evidence_fixture_files(args.fixtures_dir.resolve())
    if issues:
        for issue in issues:
            print(f"issue={issue}", file=sys.stderr)
        return 1
    print("g9_enablement_evidence_record_fixtures=ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
