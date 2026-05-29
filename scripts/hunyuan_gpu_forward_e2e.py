from __future__ import annotations

import argparse
import json
import sys
import tempfile
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT / "src") not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT / "src"))

from imageezgen3d.hunyuan_gpu_forward_smoke import (  # noqa: E402
    DEFAULT_GPU_FORWARD_E2E_SAMPLE,
    attempt_gpu_forward_workstation_e2e,
    format_gpu_forward_e2e_report,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Attempt Hunyuan GPU forward E2E via weight-verified Tencent runner. "
            "Skips honestly when workstation gates fail; does not enable the adapter."
        )
    )
    parser.add_argument(
        "--sample",
        type=Path,
        default=DEFAULT_GPU_FORWARD_E2E_SAMPLE,
        help="Sample image for the E2E attempt (default: Block/teal_block.png).",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="Run directory for artifacts (default: temp dir under outputs/).",
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
        help="Exit 1 when attempt_status is failed (workstation was ready).",
    )
    args = parser.parse_args(argv)

    run_dir = args.output_dir
    temp_dir: tempfile.TemporaryDirectory[str] | None = None
    if run_dir is None:
        temp_dir = tempfile.TemporaryDirectory(prefix="hunyuan-gpu-forward-e2e-")
        run_dir = Path(temp_dir.name)

    report = attempt_gpu_forward_workstation_e2e(
        sample_path=args.sample,
        run_dir=run_dir,
        skip_weight_warm=args.skip_weight_warm,
    )

    if args.as_json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(format_gpu_forward_e2e_report(report), end="")

    if args.strict and report["attempt_status"] == "failed":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
