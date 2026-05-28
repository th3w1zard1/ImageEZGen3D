from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from imageezgen3d.jobs import JobService  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Poll an ImageEZGen3D async job by id.",
    )
    parser.add_argument("--job-id", required=True, help="Job id returned from submit.")
    parser.add_argument(
        "--wait",
        action="store_true",
        help="Block until the job reaches a terminal status.",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=120.0,
        help="Seconds to wait when --wait is set (default: 120).",
    )
    parser.add_argument(
        "--result",
        action="store_true",
        help="Print manifest JSON when the job succeeded.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print poll payload as JSON.",
    )
    args = parser.parse_args()

    service = JobService(max_workers=1)
    try:
        if args.wait:
            poll = service.wait_for(args.job_id, timeout_seconds=args.timeout)
        else:
            poll = service.poll(args.job_id)
        payload: dict[str, object] = poll.to_dict()
        if args.result and poll.status == "succeeded":
            payload["manifest"] = service.get_result(args.job_id)
        if args.json:
            print(json.dumps(payload, indent=2))
        else:
            print(
                f"{payload['job_id']}\t{payload['status']}\trun={payload.get('run_id') or '-'}"
            )
        if poll.status == "failed":
            return 1
        return 0
    finally:
        service.shutdown(wait=False)


if __name__ == "__main__":
    raise SystemExit(main())
