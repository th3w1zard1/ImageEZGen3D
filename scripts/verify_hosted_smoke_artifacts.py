from __future__ import annotations

import argparse
import sys
from pathlib import Path

from imageezgen3d.hosted_golden_smoke import (
    verify_hosted_export_tier_smoke_record_file,
    verify_hosted_golden_smoke_record_file,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Verify hosted-golden-smoke.json and hosted-export-tier-smoke.json "
            "after scheduled smoke --record steps."
        ),
    )
    parser.add_argument(
        "golden_json",
        type=Path,
        nargs="?",
        default=Path("hosted-golden-smoke.json"),
    )
    parser.add_argument(
        "export_tier_json",
        type=Path,
        nargs="?",
        default=Path("hosted-export-tier-smoke.json"),
    )
    args = parser.parse_args(argv)

    exit_code = 0
    for label, path, verify in (
        (
            "hosted_golden_smoke",
            args.golden_json,
            verify_hosted_golden_smoke_record_file,
        ),
        (
            "hosted_export_tier_smoke",
            args.export_tier_json,
            verify_hosted_export_tier_smoke_record_file,
        ),
    ):
        if not path.is_file():
            print(f"issue={label}: missing file: {path}", file=sys.stderr)
            exit_code = 1
            continue
        issues = verify(path)
        if issues:
            for issue in issues:
                print(f"issue={label}: {issue}", file=sys.stderr)
            exit_code = 1
    if exit_code == 0:
        print("hosted_smoke_artifacts=ok")
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
