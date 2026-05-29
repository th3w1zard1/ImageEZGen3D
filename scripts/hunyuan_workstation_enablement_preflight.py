from __future__ import annotations

import argparse
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT / "src") not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT / "src"))

from imageezgen3d.hunyuan_workstation_enablement_preflight import (  # noqa: E402
    enablement_preflight_json,
    format_workstation_enablement_preflight_report,
    run_workstation_enablement_preflight,
    workstation_enablement_preflight_exit_code,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Run workstation bundle plus evidence preflight for tier-C enablement "
            "readiness (does not enable the adapter or claim G7 hosted PASS)."
        )
    )
    parser.add_argument(
        "--record-dir",
        type=Path,
        default=Path("."),
        help="Directory for gpu-forward-e2e.json (default: current directory).",
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
        help="Exit 1 when enablement_workstation_ready is false.",
    )
    args = parser.parse_args(argv)

    result = run_workstation_enablement_preflight(
        record_dir=args.record_dir,
        skip_weight_warm=args.skip_weight_warm,
    )

    if args.as_json:
        print(enablement_preflight_json(result), end="")
    else:
        print(format_workstation_enablement_preflight_report(result), end="")

    if args.strict and not result.enablement_workstation_ready:
        return 1
    return workstation_enablement_preflight_exit_code(result)


if __name__ == "__main__":
    raise SystemExit(main())
