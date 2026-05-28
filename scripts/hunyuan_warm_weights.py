from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT / "src") not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT / "src"))

from imageezgen3d.hunyuan_weights import (  # noqa: E402
    describe_hunyuan_weight_pin,
    ensure_hunyuan_weights,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Warm or verify the pinned Hunyuan Hub snapshot (G2 cache contract). "
            "Does not enable the adapter."
        )
    )
    parser.add_argument("--json", action="store_true", dest="as_json")
    parser.add_argument(
        "--describe-only",
        action="store_true",
        help="Print weight pin metadata without calling snapshot_download.",
    )
    args = parser.parse_args(argv)

    if args.describe_only:
        payload = {
            "hunyuan_warm_weights_ok": True,
            "downloaded": False,
            "weight_pin": describe_hunyuan_weight_pin(),
        }
        if args.as_json:
            print(json.dumps(payload, indent=2, sort_keys=True))
        else:
            print("hunyuan_warm_weights_ok=True")
            print("downloaded=False")
            for key, value in payload["weight_pin"].items():
                print(f"{key}={value}")
        return 0

    try:
        local_root = ensure_hunyuan_weights()
    except Exception as exc:  # noqa: BLE001 — operator CLI surfaces failure
        payload = {
            "hunyuan_warm_weights_ok": False,
            "error": type(exc).__name__,
            "message": str(exc),
        }
        if args.as_json:
            print(json.dumps(payload, indent=2, sort_keys=True))
        else:
            print("hunyuan_warm_weights_ok=False")
            print(f"error={payload['error']}")
            print(f"message={payload['message']}")
        return 1

    payload = {
        "hunyuan_warm_weights_ok": True,
        "downloaded": True,
        "local_root": str(local_root),
        "weight_pin": describe_hunyuan_weight_pin(),
    }
    if args.as_json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print("hunyuan_warm_weights_ok=True")
        print("downloaded=True")
        print(f"local_root={local_root}")
        for key, value in payload["weight_pin"].items():
            print(f"{key}={value}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
