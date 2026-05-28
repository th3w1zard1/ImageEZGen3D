from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from imageezgen3d.jobs import JobService, load_batch_requests, run_batch  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run ImageEZGen3D generation jobs from a JSONL batch file.",
    )
    parser.add_argument(
        "--input",
        required=True,
        help="Path to JSONL file (one job request object per line).",
    )
    parser.add_argument(
        "--no-wait",
        action="store_true",
        help="Submit jobs and return poll handles without waiting.",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=120.0,
        help="Seconds to wait per job when waiting (default: 120).",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print machine-readable JSON summary to stdout.",
    )
    args = parser.parse_args()

    requests = load_batch_requests(args.input)
    if not requests:
        print("No job requests found in input file.", file=sys.stderr)
        return 1

    service = JobService(max_workers=1)
    try:
        summaries = run_batch(
            service,
            requests,
            wait=not args.no_wait,
            timeout_seconds=args.timeout,
        )
    finally:
        service.shutdown(wait=True)

    if args.json:
        print(json.dumps(summaries, indent=2))
    else:
        for item in summaries:
            print(
                f"{item['job_id']}\t{item['status']}\trun={item.get('run_id') or '-'}"
            )
    failed = sum(1 for item in summaries if item.get("status") == "failed")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
