from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT / "src") not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT / "src"))

from imageezgen3d.tencent_hunyuan_pipeline import (  # noqa: E402
    format_tencent_pipeline_report,
    probe_tencent_pipeline_modules,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Probe Tencent Hunyuan3D shape+texture upstream module imports. "
            "Informational only — does not enable the adapter."
        )
    )
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args(argv)

    report = probe_tencent_pipeline_modules()
    if args.as_json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(format_tencent_pipeline_report(report), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
