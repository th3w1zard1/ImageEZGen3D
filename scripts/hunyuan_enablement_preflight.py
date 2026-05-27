from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from imageezgen3d.hunyuan_enablement_preflight import (
    EnablementPreflightResult,
    enablement_preflight_exit_code,
    evaluate_enablement_preflight,
    format_enablement_preflight_report,
)


def write_enablement_preflight_record(
    path: Path, result: EnablementPreflightResult
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(result.to_dict(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Unified Hunyuan enablement preflight: G1–G9 admission + G7 readiness."
        )
    )
    parser.add_argument("--json", action="store_true", dest="as_json")
    parser.add_argument(
        "--record",
        type=Path,
        default=None,
        help="Write JSON snapshot to this path",
    )
    args = parser.parse_args(argv)

    result = evaluate_enablement_preflight()
    if args.record is not None:
        write_enablement_preflight_record(args.record, result)
    if args.as_json:
        print(json.dumps(result.to_dict(), indent=2, sort_keys=True))
    elif args.record is None:
        print(format_enablement_preflight_report(result), end="")

    return enablement_preflight_exit_code(result)


if __name__ == "__main__":
    raise SystemExit(main())
