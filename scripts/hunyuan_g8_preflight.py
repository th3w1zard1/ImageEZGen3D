from __future__ import annotations

import argparse
import json

from imageezgen3d.hosted_golden_smoke import (
    DEFAULT_SPACE_URL,
    format_hosted_golden_report,
    run_hosted_golden_smoke,
)
from imageezgen3d.hunyuan_g8_preflight import validate_g8_cpu_fallback_status


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "G8 CPU fallback honesty: validate status markdown locally or via live golden smoke."
        )
    )
    parser.add_argument("--json", action="store_true", dest="as_json")
    parser.add_argument(
        "--live",
        action="store_true",
        help="Run hosted golden smoke (includes G8 status checks)",
    )
    parser.add_argument("--space-url", default=DEFAULT_SPACE_URL)
    parser.add_argument("--status-file", type=str, default=None, help="Markdown status file")
    args = parser.parse_args(argv)

    if args.live:
        result = run_hosted_golden_smoke(space_url=args.space_url)
        payload = {
            "ok": result.ok,
            "mode": "live_golden_smoke",
            "run_id": result.run_id,
            "issues": list(result.issues),
        }
        if args.as_json:
            print(json.dumps(payload, indent=2, sort_keys=True))
        else:
            print(format_hosted_golden_report(result))
        return 0 if result.ok else 1

    if args.status_file:
        from pathlib import Path

        status = Path(args.status_file).read_text(encoding="utf-8")
    else:
        parser.error("Provide --live or --status-file")

    issues = validate_g8_cpu_fallback_status(status)
    payload = {"ok": not issues, "mode": "status_file", "issues": issues}
    if args.as_json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        for issue in issues:
            print(f"issue={issue}")
    return 0 if not issues else 1


if __name__ == "__main__":
    raise SystemExit(main())
