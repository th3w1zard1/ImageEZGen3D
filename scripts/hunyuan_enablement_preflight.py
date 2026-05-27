from __future__ import annotations

import argparse
import json
import sys

from imageezgen3d.hunyuan_enablement_preflight import (
    enablement_preflight_exit_code,
    evaluate_enablement_preflight,
    format_enablement_preflight_report,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Unified Hunyuan enablement preflight: G1–G9 admission + G7 readiness."
        )
    )
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args(argv)

    result = evaluate_enablement_preflight()
    if args.as_json:
        print(json.dumps(result.to_dict(), indent=2, sort_keys=True))
    else:
        print(format_enablement_preflight_report(result), end="")

    return enablement_preflight_exit_code(result)


if __name__ == "__main__":
    raise SystemExit(main())
