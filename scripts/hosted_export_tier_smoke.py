from __future__ import annotations

import argparse
import json
from pathlib import Path

from imageezgen3d.hosted_golden_smoke import (
    DEFAULT_SPACE_URL,
    format_hosted_golden_report,
    run_hosted_golden_smoke,
)

_TIER_CHECKS: tuple[tuple[str, bool, int], ...] = (
    ("draft", False, 42),
    ("balanced", True, 44),
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Hosted export tier smoke: draft + balanced /generate with manifest validation."
        )
    )
    parser.add_argument("--space-url", default=DEFAULT_SPACE_URL)
    parser.add_argument(
        "--record",
        type=Path,
        default=None,
        help="Write combined JSON results to this path",
    )
    args = parser.parse_args(argv)

    results: list[dict[str, object]] = []
    exit_code = 0
    for quality, expect_raw, seed in _TIER_CHECKS:
        result = run_hosted_golden_smoke(
            space_url=args.space_url,
            seed=seed,
            quality=quality,
            validate_manifest=True,
            expect_raw=expect_raw,
        )
        print(format_hosted_golden_report(result))
        print()
        results.append(result.to_dict())
        if not result.ok:
            exit_code = 1

    if args.record is not None:
        args.record.parent.mkdir(parents=True, exist_ok=True)
        args.record.write_text(
            json.dumps({"checks": results}, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

    if exit_code == 0:
        print("OK: hosted export tier smoke passed (draft + balanced)")
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
