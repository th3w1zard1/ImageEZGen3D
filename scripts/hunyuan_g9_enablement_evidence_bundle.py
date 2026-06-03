from __future__ import annotations

import argparse
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT / "src") not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT / "src"))

from imageezgen3d.hunyuan_g9_enablement_evidence_bundle import (  # noqa: E402
    format_g9_enablement_evidence_bundle_report,
    g9_enablement_evidence_bundle_json,
    run_g9_enablement_evidence_bundle,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Run neural enablement capstone and record g9-enablement-evidence.json "
            "for enablement PR reviewers (does not enable the adapter)."
        )
    )
    parser.add_argument(
        "--record-dir",
        type=Path,
        default=Path("."),
        help="Directory for enablement JSON records.",
    )
    parser.add_argument(
        "--skip-weight-warm",
        action="store_true",
        help="Probe gates only; do not warm Hub weights before attempt.",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help=(
            "Exit 1 when g9_enablement_evidence_ready is false or parity_ok is false."
        ),
    )
    parser.add_argument(
        "--require-hosted-neural",
        action="store_true",
        help="Require hunyuan-g7-hosted-neural.json ok=true in --record-dir.",
    )
    parser.add_argument(
        "--live-probe",
        action="store_true",
        help="Run hosted G7 live probe under --record-dir (network).",
    )
    parser.add_argument(
        "--space-url",
        default=None,
        help="Space URL for --live-probe or --hosted-neural.",
    )
    parser.add_argument(
        "--sample",
        type=Path,
        default=None,
        help="Sample image path for --live-probe.",
    )
    parser.add_argument(
        "--hosted-neural",
        action="store_true",
        help=(
            "Record hunyuan-g7-hosted-neural.json from status markdown "
            "(requires --status-file or --status-text)."
        ),
    )
    parser.add_argument(
        "--status-file",
        type=Path,
        default=None,
        help="Generation status markdown for --hosted-neural.",
    )
    parser.add_argument(
        "--status-text",
        default=None,
        help="Generation status markdown inline for --hosted-neural.",
    )
    parser.add_argument(
        "--hosted-sample",
        default=None,
        help="Sample label or path for --hosted-neural record.",
    )
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args(argv)

    if args.hosted_neural and args.status_file is None and args.status_text is None:
        parser.error("--hosted-neural requires --status-file or --status-text")
    if args.status_file is not None and args.status_text is not None:
        parser.error("use only one of --status-file or --status-text")

    result = run_g9_enablement_evidence_bundle(
        record_dir=args.record_dir,
        skip_weight_warm=args.skip_weight_warm,
        live_probe=args.live_probe,
        space_url=args.space_url,
        sample_path=args.sample,
        hosted_neural=args.hosted_neural,
        hosted_neural_status_file=args.status_file,
        hosted_neural_status_text=args.status_text,
        hosted_neural_sample=args.hosted_sample,
        hosted_neural_space_url=args.space_url,
        require_hosted_neural=args.require_hosted_neural,
    )

    if args.as_json:
        print(g9_enablement_evidence_bundle_json(result), end="")
    else:
        print(format_g9_enablement_evidence_bundle_report(result), end="")

    if args.strict and not result.g9_enablement_evidence_ready:
        return 1
    if args.strict and not result.parity_ok:
        return 1
    if not result.g9_enablement_preflight_ok:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
