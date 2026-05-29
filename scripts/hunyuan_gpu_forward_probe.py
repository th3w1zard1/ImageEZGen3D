from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT / "src") not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT / "src"))

from imageezgen3d.hunyuan_gpu_forward_smoke import (  # noqa: E402
    evaluate_gpu_forward_workstation_readiness,
    format_gpu_forward_workstation_report,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Probe Hunyuan GPU forward workstation readiness (tier-C, pipeline, CUDA). "
            "Informational only — does not run neural inference or enable the adapter."
        )
    )
    parser.add_argument("--json", action="store_true", dest="as_json")
    parser.add_argument(
        "--skip-weight-warm",
        action="store_true",
        help="Probe imports and gates only; do not warm Hub weights.",
    )
    args = parser.parse_args(argv)

    report = evaluate_gpu_forward_workstation_readiness(
        skip_weight_warm=args.skip_weight_warm,
    )
    if args.as_json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(format_gpu_forward_workstation_report(report), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
