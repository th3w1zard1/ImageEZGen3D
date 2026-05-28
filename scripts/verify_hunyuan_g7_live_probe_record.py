from __future__ import annotations

import argparse
import sys
from pathlib import Path

from imageezgen3d.hunyuan_g7_preflight import verify_hunyuan_g7_live_probe_record_file


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Verify hunyuan-g7-live-probe.json from scheduled smoke --live-probe.",
    )
    parser.add_argument(
        "record_json",
        type=Path,
        nargs="?",
        default=Path("hunyuan-g7-live-probe.json"),
    )
    args = parser.parse_args(argv)

    if not args.record_json.is_file():
        print(f"issue=missing file: {args.record_json}", file=sys.stderr)
        return 1

    issues = verify_hunyuan_g7_live_probe_record_file(args.record_json)
    if issues:
        for issue in issues:
            print(f"issue={issue}", file=sys.stderr)
        return 1
    print("hunyuan_g7_live_probe_record=ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
