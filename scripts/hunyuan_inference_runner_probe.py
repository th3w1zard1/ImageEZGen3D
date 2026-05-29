from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT / "src") not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT / "src"))

from imageezgen3d.hunyuan_inference_runner import (  # noqa: E402
    describe_hunyuan_inference_runner,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Report whether a Hunyuan tier-C inference runner is registered. "
            "Informational only — does not enable the adapter."
        )
    )
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args(argv)

    payload = describe_hunyuan_inference_runner()
    if args.as_json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print("hunyuan_inference_runner_probe_ok=True")
        for key, value in payload.items():
            print(f"{key}={value}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
