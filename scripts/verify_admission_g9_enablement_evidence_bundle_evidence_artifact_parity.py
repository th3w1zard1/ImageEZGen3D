from __future__ import annotations

import argparse
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT / "src") not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT / "src"))

from imageezgen3d.hunyuan_neural_enablement_artifact_parity import (  # noqa: E402
    verify_admission_g9_enablement_evidence_bundle_evidence_artifact_parity_files,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Verify admission-g9-enablement-evidence-bundle.json nested evidence "
            "parity with g9-enablement-evidence.json in a record directory."
        )
    )
    parser.add_argument(
        "--record-dir",
        type=Path,
        default=Path("."),
        help="Directory containing both bundle and G9 evidence JSON records.",
    )
    args = parser.parse_args(argv)

    issues = verify_admission_g9_enablement_evidence_bundle_evidence_artifact_parity_files(
        args.record_dir
    )
    if issues:
        for issue in issues:
            print(f"issue={issue}", file=sys.stderr)
        return 1
    print("admission_g9_enablement_evidence_bundle_evidence_artifact_parity=ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
