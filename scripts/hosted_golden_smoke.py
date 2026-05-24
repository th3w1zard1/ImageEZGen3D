from __future__ import annotations

import argparse
from pathlib import Path

from imageezgen3d.hosted_golden_smoke import (
    DEFAULT_SPACE_URL,
    format_hosted_golden_report,
    hosted_golden_json,
    run_hosted_golden_smoke,
    write_hosted_golden_record,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Hosted Space golden smoke: Block /generate with export-budget checks."
        )
    )
    parser.add_argument("--space-url", default=DEFAULT_SPACE_URL)
    parser.add_argument(
        "--sample",
        type=Path,
        default=None,
        help="Path to sample image (default: assets/examples/teal_block.png)",
    )
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--quality", default="draft")
    parser.add_argument("--adapter", default="auto")
    parser.add_argument("--json", action="store_true", dest="as_json")
    parser.add_argument(
        "--record",
        type=Path,
        default=None,
        help="Write result JSON to this path",
    )
    args = parser.parse_args(argv)

    result = run_hosted_golden_smoke(
        space_url=args.space_url,
        sample_path=args.sample,
        seed=args.seed,
        quality=args.quality,
        adapter=args.adapter,
    )
    if args.record is not None:
        write_hosted_golden_record(args.record, result)
    if args.as_json:
        print(hosted_golden_json(result), end="")
    elif args.record is None:
        print(format_hosted_golden_report(result))

    return 0 if result.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
