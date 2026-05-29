from __future__ import annotations

import argparse
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT / "src") not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT / "src"))

from imageezgen3d.hunyuan_g9_workstation_artifact_parity import (  # noqa: E402
    verify_g9_workstation_artifact_files,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Verify G9 workstation JSON artifact parity in a record directory.",
    )
    parser.add_argument(
        "--record-dir",
        type=Path,
        default=Path("."),
        help="Directory containing g9-workstation-bundle.json and related records.",
    )
    args = parser.parse_args(argv)

    issues = verify_g9_workstation_artifact_files(args.record_dir)
    if issues:
        for issue in issues:
            print(f"issue={issue}", file=sys.stderr)
        return 1
    print("g9_workstation_artifact_parity=ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
