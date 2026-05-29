from __future__ import annotations

import argparse
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT / "src") not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT / "src"))

from imageezgen3d.hunyuan_g9_preflight_bundle import (  # noqa: E402
    format_g9_preflight_bundle_report,
    run_g9_preflight_bundle,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Run G9 workstation bundle, record verify, and artifact parity "
            "(does not enable the adapter)."
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
        help="Exit 1 when workstation_evidence_ready is false.",
    )
    args = parser.parse_args(argv)

    result = run_g9_preflight_bundle(
        record_dir=args.record_dir,
        skip_weight_warm=args.skip_weight_warm,
    )
    print(format_g9_preflight_bundle_report(result), end="")

    if args.strict and not result.workstation_evidence_ready:
        return 1
    if not result.g9_preflight_bundle_ok:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
