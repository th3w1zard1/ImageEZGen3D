from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT / "src") not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT / "src"))

from imageezgen3d.hunyuan_configured_inference import (  # noqa: E402
    describe_configured_adapter_inference_path,
    format_configured_adapter_inference_report,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Report configured Hunyuan adapter inference path readiness. "
            "Informational only — does not enable the adapter on Space."
        )
    )
    parser.add_argument("--json", action="store_true", dest="as_json")
    parser.add_argument(
        "--skip-weight-warm",
        action="store_true",
        help="Skip Hub weight warm when evaluating tier-C gates.",
    )
    args = parser.parse_args(argv)

    report = describe_configured_adapter_inference_path(
        skip_weight_warm=args.skip_weight_warm,
    )
    if args.as_json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(format_configured_adapter_inference_report(report))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
