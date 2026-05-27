from __future__ import annotations

import argparse
import sys
from pathlib import Path

from imageezgen3d.hunyuan_ci_artifact_parity import verify_hunyuan_ci_artifact_files


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Verify hunyuan-admission-audit.json and hunyuan-enablement-preflight.json "
            "agree on g7_readiness and g8_enablement."
        )
    )
    parser.add_argument(
        "audit_json",
        type=Path,
        help="Path to hunyuan-admission-audit.json",
    )
    parser.add_argument(
        "preflight_json",
        type=Path,
        help="Path to hunyuan-enablement-preflight.json",
    )
    args = parser.parse_args(argv)

    issues = verify_hunyuan_ci_artifact_files(args.audit_json, args.preflight_json)
    if issues:
        for issue in issues:
            print(f"issue={issue}", file=sys.stderr)
        return 1
    print("hunyuan_ci_artifact_parity=ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
