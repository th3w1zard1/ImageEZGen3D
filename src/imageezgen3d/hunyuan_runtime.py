from __future__ import annotations

import importlib
import importlib.util
from typing import Any

from .hunyuan_weights import describe_hunyuan_weight_pin

# Tier B mirrors pyproject optional extra `hunyuan-audit` (G3).
TIER_B_MODULES: tuple[tuple[str, str], ...] = (
    ("transformers", "transformers"),
    ("diffusers", "diffusers"),
    ("accelerate", "accelerate"),
    ("huggingface_hub", "huggingface_hub"),
    ("safetensors", "safetensors"),
    ("einops", "einops"),
    ("omegaconf", "omegaconf"),
    ("yaml", "yaml"),
    ("tqdm", "tqdm"),
    ("pydantic", "pydantic"),
)

# Tier C highlights from requirements/hunyuan-pins.txt (full Hunyuan stack).
TIER_C_MODULES: tuple[tuple[str, str], ...] = (
    ("open3d", "open3d"),
    ("pymeshlab", "pymeshlab"),
    ("cupy", "cupy"),
    ("bpy", "bpy"),
    ("deepspeed", "deepspeed"),
    ("basicsr", "basicsr"),
    ("realesrgan", "realesrgan"),
    ("rembg", "rembg"),
)


def probe_import(module_name: str) -> dict[str, Any]:
    """Return import availability for one module without raising."""
    spec = importlib.util.find_spec(module_name)
    if spec is None:
        return {
            "available": False,
            "error": "ModuleNotFoundError",
            "message": f"No module named '{module_name}'",
        }
    try:
        module = importlib.import_module(module_name)
    except Exception as exc:  # noqa: BLE001 — probe must capture all import failures
        return {
            "available": False,
            "error": type(exc).__name__,
            "message": str(exc),
        }
    version = getattr(module, "__version__", "")
    payload: dict[str, Any] = {"available": True}
    if version:
        payload["version"] = str(version)
    return payload


def probe_hunyuan_runtime() -> dict[str, Any]:
    """Probe tier B/C import surface and weight pin metadata (no adapter enablement)."""
    tier_b = {label: probe_import(module) for label, module in TIER_B_MODULES}
    tier_c = {label: probe_import(module) for label, module in TIER_C_MODULES}
    return {
        "tier_b": tier_b,
        "tier_c": tier_c,
        "tier_b_available": all(entry["available"] for entry in tier_b.values()),
        "tier_c_available": all(entry["available"] for entry in tier_c.values()),
        "weight_pin": describe_hunyuan_weight_pin(),
    }


def format_hunyuan_runtime_report(report: dict[str, Any]) -> str:
    lines = [
        "hunyuan_runtime_probe_ok=True",
        f"tier_b_available={report['tier_b_available']}",
        f"tier_c_available={report['tier_c_available']}",
        f"weight_repo={report['weight_pin']['repo_id']}",
        f"weight_revision={report['weight_pin']['revision']}",
    ]
    for tier_name in ("tier_b", "tier_c"):
        for label, entry in report[tier_name].items():
            if entry.get("available"):
                version = entry.get("version", "")
                suffix = f" version={version}" if version else ""
                lines.append(f"{tier_name}.{label}=available{suffix}")
            else:
                error = entry.get("error", "unknown")
                lines.append(f"{tier_name}.{label}=missing error={error}")
    return "\n".join(lines) + "\n"
