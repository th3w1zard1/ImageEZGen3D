from __future__ import annotations

import argparse
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT / "src") not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT / "src"))

from imageezgen3d.hunyuan_neural_enablement_preflight_bundle import (  # noqa: E402
    format_neural_enablement_preflight_bundle_report,
    neural_enablement_preflight_bundle_json,
    run_neural_enablement_preflight_bundle,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Run G7 enablement preflight plus configured-adapter inference path "
            "for tier-C neural enablement operators (does not enable the adapter)."
        )
    )
    parser.add_argument(
        "--record-dir",
        type=Path,
        default=Path("."),
        help="Directory for admission, enablement, and G9 workstation JSON records.",
    )
    parser.add_argument(
        "--skip-weight-warm",
        action="store_true",
        help="Probe gates only; do not warm Hub weights before attempt.",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit 1 when neural_enablement_ready is false.",
    )
    parser.add_argument(
        "--live-probe",
        action="store_true",
        help=(
            "Run hosted G7 live probe and write hunyuan-g7-live-probe.json "
            "under --record-dir (network)."
        ),
    )
    parser.add_argument(
        "--space-url",
        default=None,
        help="Space URL for --live-probe (default: IMAGEEZ hosted Space).",
    )
    parser.add_argument(
        "--sample",
        type=Path,
        default=None,
        help="Sample image path for --live-probe.",
    )
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args(argv)

    result = run_neural_enablement_preflight_bundle(
        record_dir=args.record_dir,
        skip_weight_warm=args.skip_weight_warm,
        live_probe=args.live_probe,
        space_url=args.space_url,
        sample_path=args.sample,
    )

    if args.as_json:
        print(neural_enablement_preflight_bundle_json(result), end="")
    else:
        print(format_neural_enablement_preflight_bundle_report(result), end="")

    if args.strict and not result.neural_enablement_ready:
        return 1
    if not result.neural_enablement_preflight_ok:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
