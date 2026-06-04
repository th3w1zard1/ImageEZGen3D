from __future__ import annotations

import argparse
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT / "src") not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT / "src"))

from imageezgen3d.hunyuan_neural_enablement_preflight_bundle import (  # noqa: E402
    verify_neural_enablement_preflight_bundle_files,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Verify neural-enablement-preflight.json and record-dir artifact "
            "parity after the neural capstone."
        )
    )
    parser.add_argument(
        "--record-dir",
        type=Path,
        default=Path("."),
        help="Directory containing neural capstone JSON records.",
    )
    args = parser.parse_args(argv)

    issues = verify_neural_enablement_preflight_bundle_files(args.record_dir)
    if issues:
        for issue in issues:
            print(f"issue={issue}", file=sys.stderr)
        return 1
    print("neural_enablement_preflight_bundle_verify=ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
