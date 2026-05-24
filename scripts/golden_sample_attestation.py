from __future__ import annotations

import argparse
import sys
from pathlib import Path

from imageezgen3d.golden_sample import (
    attestation_json,
    format_attestation_report,
    run_golden_sample_attestation,
    write_attestation_record,
)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run Block golden-sample generation attestation (local CPU demo)."
    )
    parser.add_argument(
        "--sample",
        type=Path,
        default=None,
        help="Path to sample image (default: assets/examples/teal_block.png)",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="Output directory for run artifacts (default: outputs)",
    )
    parser.add_argument("--json", action="store_true", dest="as_json")
    parser.add_argument(
        "--record",
        type=Path,
        default=None,
        help="Write attestation JSON to this path (in addition to stdout when --json)",
    )
    args = parser.parse_args()

    attestation = run_golden_sample_attestation(
        sample_path=args.sample,
        output_dir=args.output_dir,
    )
    if args.record is not None:
        write_attestation_record(args.record, attestation)
    if args.as_json:
        print(attestation_json(attestation), end="")
    elif args.record is None:
        print(format_attestation_report(attestation))

    if not attestation.ok:
        sys.exit(1)


if __name__ == "__main__":
    main()
