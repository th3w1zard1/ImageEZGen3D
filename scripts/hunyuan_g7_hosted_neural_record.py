from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT / "src") not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT / "src"))

from imageezgen3d.hunyuan_g7_hosted_neural_record import (  # noqa: E402
    DEFAULT_G7_HOSTED_NEURAL_RECORD,
    attestation_from_status_markdown,
    write_g7_hosted_neural_record,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Record hunyuan-g7-hosted-neural.json from hosted /generate status markdown "
            "(post-enablement G7 evidence)."
        )
    )
    parser.add_argument(
        "--status-file",
        type=Path,
        help="Read generation status markdown from this file.",
    )
    parser.add_argument(
        "--status-text",
        help="Generation status markdown inline (alternative to --status-file).",
    )
    parser.add_argument(
        "--record",
        type=Path,
        default=DEFAULT_G7_HOSTED_NEURAL_RECORD,
        help="Output JSON record path.",
    )
    parser.add_argument("--sample", help="Sample image label or path used for the run.")
    parser.add_argument("--space-url", help="Hosted Space URL used for the run.")
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args(argv)

    if args.status_file is None and args.status_text is None:
        parser.error("one of --status-file or --status-text is required")
    if args.status_file is not None and args.status_text is not None:
        parser.error("use only one of --status-file or --status-text")

    if args.status_file is not None:
        status_markdown = args.status_file.read_text(encoding="utf-8")
    else:
        status_markdown = args.status_text or ""

    attestation = attestation_from_status_markdown(
        status_markdown,
        sample=args.sample,
        space_url=args.space_url,
    )
    write_g7_hosted_neural_record(args.record, attestation)

    if args.as_json:
        print(json.dumps(attestation.to_dict(), indent=2, sort_keys=True))
    else:
        print(f"g7_hosted_neural_record_ok={attestation.ok}")
        print(f"g7_status_valid={attestation.g7_status_valid}")
        print(f"run_id={attestation.run_id}")
        print(f"record={args.record.resolve()}")
        for issue in attestation.issues:
            print(f"issue={issue}")

    return 0 if attestation.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
