from __future__ import annotations

import argparse
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT / "src") not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT / "src"))

from imageezgen3d.hunyuan_gpu_forward_e2e_attestation import (  # noqa: E402
    verify_gpu_forward_e2e_record_file,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Verify hunyuan GPU forward E2E attestation JSON schema and gates.",
    )
    parser.add_argument(
        "record_json",
        type=Path,
        nargs="?",
        default=Path("gpu-forward-e2e.json"),
        help="Path to gpu-forward-e2e.json (default: ./gpu-forward-e2e.json)",
    )
    args = parser.parse_args(argv)

    issues = verify_gpu_forward_e2e_record_file(args.record_json)
    if issues:
        for issue in issues:
            print(f"issue={issue}", file=sys.stderr)
        return 1
    print("gpu_forward_e2e_record=ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
