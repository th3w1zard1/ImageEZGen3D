from __future__ import annotations

import argparse
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT / "src") not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT / "src"))

from imageezgen3d.hunyuan_g9_enablement_evidence_record import (  # noqa: E402
    verify_g9_enablement_evidence_record_file,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Verify g9-enablement-evidence.json schema and gates.",
    )
    parser.add_argument(
        "record_json",
        type=Path,
        nargs="?",
        default=Path("g9-enablement-evidence.json"),
        help="Path to g9-enablement-evidence.json",
    )
    args = parser.parse_args(argv)

    issues = verify_g9_enablement_evidence_record_file(args.record_json)
    if issues:
        for issue in issues:
            print(f"issue={issue}", file=sys.stderr)
        return 1
    print("g9_enablement_evidence_record=ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
