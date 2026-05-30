from __future__ import annotations

import argparse
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT / "src") not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT / "src"))

from imageezgen3d.hunyuan_neural_enablement_record import (  # noqa: E402
    verify_neural_enablement_record_file,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Verify neural-enablement-preflight.json schema and gates.",
    )
    parser.add_argument(
        "record_json",
        type=Path,
        nargs="?",
        default=Path("neural-enablement-preflight.json"),
        help="Path to neural-enablement-preflight.json",
    )
    args = parser.parse_args(argv)

    issues = verify_neural_enablement_record_file(args.record_json.resolve())
    if issues:
        for issue in issues:
            print(f"issue={issue}", file=sys.stderr)
        return 1
    print("hunyuan_neural_enablement_record=ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
