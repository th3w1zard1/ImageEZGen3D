from __future__ import annotations

import argparse
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT / "src") not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT / "src"))

from imageezgen3d.hunyuan_admission_g9_enablement_evidence_bundle_record import (  # noqa: E402
    verify_admission_g9_enablement_evidence_bundle_fixture_files,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Verify admission-g9-enablement-evidence-bundle fixture JSON files.",
    )
    parser.add_argument(
        "--fixtures-dir",
        type=Path,
        default=Path("tests/fixtures"),
        help="Directory containing admission-g9-enablement-evidence-bundle-*.json fixtures",
    )
    args = parser.parse_args(argv)

    issues = verify_admission_g9_enablement_evidence_bundle_fixture_files(
        args.fixtures_dir.resolve()
    )
    if issues:
        for issue in issues:
            print(f"issue={issue}", file=sys.stderr)
        return 1
    print("admission_g9_enablement_evidence_bundle_record_fixtures=ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
