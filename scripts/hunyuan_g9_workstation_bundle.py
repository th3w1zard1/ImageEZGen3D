from __future__ import annotations

import argparse
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT / "src") not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT / "src"))

from imageezgen3d.hunyuan_g9_workstation_bundle import (  # noqa: E402
    format_g9_workstation_bundle_report,
    g9_workstation_bundle_json,
    run_g9_workstation_bundle,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Run Hunyuan preflight bundle plus workstation enablement record "
            "for G9 operator readiness (does not enable the adapter)."
        )
    )
    parser.add_argument(
        "--record-dir",
        type=Path,
        default=Path("."),
        help="Directory for admission, enablement, and workstation JSON records.",
    )
    parser.add_argument("--json", action="store_true", dest="as_json")
    parser.add_argument(
        "--skip-weight-warm",
        action="store_true",
        help="Probe gates only; do not warm Hub weights before attempt.",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit 1 when g9_workstation_bundle_ok or workstation_evidence_ready is false.",
    )
    args = parser.parse_args(argv)

    result = run_g9_workstation_bundle(
        record_dir=args.record_dir,
        skip_weight_warm=args.skip_weight_warm,
    )

    if args.as_json:
        print(g9_workstation_bundle_json(result), end="")
    else:
        print(format_g9_workstation_bundle_report(result), end="")

    if args.strict and (
        not result.g9_workstation_bundle_ok or not result.workstation_evidence_ready
    ):
        return 1
    if not result.g9_workstation_bundle_ok:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
