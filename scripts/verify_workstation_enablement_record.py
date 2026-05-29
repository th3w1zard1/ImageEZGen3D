from __future__ import annotations

import argparse
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT / "src") not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT / "src"))

from imageezgen3d.hunyuan_workstation_enablement_record import (  # noqa: E402
    verify_workstation_enablement_record_file,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Verify workstation-enablement-preflight.json schema and gates.",
    )
    parser.add_argument(
        "record_json",
        type=Path,
        nargs="?",
        default=Path("workstation-enablement-preflight.json"),
        help="Path to workstation-enablement-preflight.json",
    )
    args = parser.parse_args(argv)

    issues = verify_workstation_enablement_record_file(args.record_json)
    if issues:
        for issue in issues:
            print(f"issue={issue}", file=sys.stderr)
        return 1
    print("workstation_enablement_record=ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
