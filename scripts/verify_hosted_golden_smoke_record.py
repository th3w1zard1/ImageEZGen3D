from __future__ import annotations

import argparse
import sys
from pathlib import Path

from imageezgen3d.hosted_golden_smoke import verify_hosted_golden_smoke_record_file


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Verify hosted-golden-smoke.json schema and required keys.",
    )
    parser.add_argument(
        "record_json",
        type=Path,
        nargs="?",
        default=Path("hosted-golden-smoke.json"),
        help="Path to hosted-golden-smoke.json (default: ./hosted-golden-smoke.json)",
    )
    args = parser.parse_args(argv)

    if not args.record_json.is_file():
        print(f"issue=missing file: {args.record_json}", file=sys.stderr)
        return 1

    issues = verify_hosted_golden_smoke_record_file(args.record_json)
    if issues:
        for issue in issues:
            print(f"issue={issue}", file=sys.stderr)
        return 1
    print("hosted_golden_smoke_record=ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
