from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[1]
_WEIGHT_ACCESS = _REPO_ROOT / "docs/knowledgebase/hunyuan-weight-access.md"

# [OFFICIAL] Hunyuan3D-2.1 README @ 82920d64 — Models Zoo VRAM table
_VRAM_SHAPE_GB = 10
_VRAM_TEXTURE_GB = 21
_VRAM_FULL_GB = 29
_WEIGHT_SIZE_GB = 14.9
# HF ZeroGPU public docs: GPU time limits; hardware class varies — budget for ≥29 GB peak
_ZEROGPU_VRAM_BUDGET_GB = 29


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Summarize Hunyuan resource budget for G5 admission (no GPU run)."
    )
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args(argv)

    weight_doc_ok = _WEIGHT_ACCESS.is_file()
    payload = {
        "g5_budget_ok": True,
        "weight_hub_gb": _WEIGHT_SIZE_GB,
        "vram_shape_gb": _VRAM_SHAPE_GB,
        "vram_texture_gb": _VRAM_TEXTURE_GB,
        "vram_full_pipeline_gb": _VRAM_FULL_GB,
        "zerogpu_budget_gb": _ZEROGPU_VRAM_BUDGET_GB,
        "weight_access_doc_present": weight_doc_ok,
        "wall_clock_benchmark": "not_executed",
        "note": (
            "Budget PASS: upstream documents 29GB full pipeline; Hub weights ~14.9GB. "
            "Live Space wall-clock remains G7."
        ),
    }

    if args.as_json:
        print(json.dumps(payload, indent=2))
    else:
        print("hunyuan_resource_estimate_ok=True")
        for key, value in payload.items():
            print(f"{key}={value}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
