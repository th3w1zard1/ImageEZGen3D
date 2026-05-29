from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT / "src") not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT / "src"))

from imageezgen3d.hunyuan_workstation_evidence_preflight import (  # noqa: E402
    evaluate_workstation_evidence_preflight,
    format_workstation_evidence_preflight_report,
    workstation_evidence_preflight_exit_code,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Preflight optional local gpu-forward-e2e.json workstation evidence "
            "(does not enable the adapter or claim G7 hosted PASS)."
        )
    )
    parser.add_argument(
        "record_json",
        type=Path,
        nargs="?",
        default=Path("gpu-forward-e2e.json"),
        help="Path to gpu-forward-e2e.json (default: ./gpu-forward-e2e.json)",
    )
    parser.add_argument("--json", action="store_true", dest="as_json")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit 1 when record is present but workstation_evidence_ok is false.",
    )
    args = parser.parse_args(argv)

    result = evaluate_workstation_evidence_preflight(args.record_json)
    if args.as_json:
        print(json.dumps(result.to_dict(), indent=2, sort_keys=True))
    else:
        print(format_workstation_evidence_preflight_report(result), end="")

    if args.strict and result.record_present and not result.workstation_evidence_ok:
        return 1
    return workstation_evidence_preflight_exit_code(result)


if __name__ == "__main__":
    raise SystemExit(main())
