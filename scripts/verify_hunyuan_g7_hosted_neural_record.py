from __future__ import annotations

import argparse
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT / "src") not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT / "src"))

from imageezgen3d.hunyuan_g7_hosted_neural_record import (  # noqa: E402
    DEFAULT_G7_HOSTED_NEURAL_RECORD,
    verify_g7_hosted_neural_record_file,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Verify hunyuan-g7-hosted-neural.json post-enablement G7 evidence.",
    )
    parser.add_argument(
        "record_json",
        type=Path,
        nargs="?",
        default=DEFAULT_G7_HOSTED_NEURAL_RECORD,
        help="Path to hunyuan-g7-hosted-neural.json",
    )
    args = parser.parse_args(argv)

    issues = verify_g7_hosted_neural_record_file(args.record_json.resolve())
    if issues:
        for issue in issues:
            print(f"issue={issue}", file=sys.stderr)
        return 1
    print("hunyuan_g7_hosted_neural_record=ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
