from __future__ import annotations

import argparse
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT / "src") not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT / "src"))

from imageezgen3d.hunyuan_gpu_forward_workstation_bundle import (  # noqa: E402
    verify_gpu_forward_e2e_fixture_files,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Verify gpu-forward-e2e attestation fixture JSON files.",
    )
    parser.add_argument(
        "fixtures_dir",
        type=Path,
        nargs="?",
        default=Path("tests/fixtures"),
        help="Directory containing gpu-forward-e2e-*.json fixtures",
    )
    args = parser.parse_args(argv)

    issues = verify_gpu_forward_e2e_fixture_files(args.fixtures_dir.resolve())
    if issues:
        for issue in issues:
            print(f"issue={issue}", file=sys.stderr)
        return 1
    print("gpu_forward_e2e_fixtures=ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
