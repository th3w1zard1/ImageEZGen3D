from __future__ import annotations

import argparse
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT / "src") not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT / "src"))

from imageezgen3d.hunyuan_neural_enablement_artifact_parity import (  # noqa: E402
    verify_admission_g9_enablement_evidence_bundle_evidence_artifact_parity_fixture_files,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Verify admission-g9-enablement-evidence-bundle-skipped.json "
            "parity with g9-enablement-evidence-skipped.json fixtures."
        )
    )
    parser.add_argument(
        "--fixtures-dir",
        type=Path,
        default=Path("tests/fixtures"),
        help="Directory containing aligned skipped bundle and evidence fixtures",
    )
    args = parser.parse_args(argv)

    issues = (
        verify_admission_g9_enablement_evidence_bundle_evidence_artifact_parity_fixture_files(
            args.fixtures_dir.resolve()
        )
    )
    if issues:
        for issue in issues:
            print(f"issue={issue}", file=sys.stderr)
        return 1
    print("admission_g9_enablement_evidence_bundle_evidence_artifact_parity_fixtures=ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
