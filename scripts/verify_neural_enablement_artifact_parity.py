from __future__ import annotations

import argparse
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT / "src") not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT / "src"))

from imageezgen3d.hunyuan_neural_enablement_artifact_parity import (  # noqa: E402
    verify_neural_enablement_artifact_files,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Verify neural-enablement-preflight.json parity with "
            "g9-workstation-bundle.json, hunyuan-enablement-preflight.json, "
            "optional hunyuan-g7-live-probe.json, optional "
            "hunyuan-g7-hosted-neural.json, and optional "
            "g9-enablement-evidence.json in a record directory."
        )
    )
    parser.add_argument(
        "--record-dir",
        type=Path,
        default=Path("."),
        help="Directory containing neural and G9 workstation JSON records.",
    )
    args = parser.parse_args(argv)

    issues = verify_neural_enablement_artifact_files(args.record_dir.resolve())
    if issues:
        for issue in issues:
            print(f"issue={issue}", file=sys.stderr)
        return 1
    print("neural_enablement_artifact_parity=ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
