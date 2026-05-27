from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

_REPO_ROOT = Path(__file__).resolve().parents[2]
HUNYUAN_SAMPLE_MANIFEST = (
    _REPO_ROOT / "tests" / "fixtures" / "hunyuan-zerogpu-manifest.sample.json"
)

_REQUIRED_PARAMETER_KEYS = (
    "requested_adapter",
    "selected_adapter",
    "quality",
    "decimation_target",
    "seed",
    "runtime",
)
_REQUIRED_ARTIFACT_KEYS = ("manifest", "glb", "obj", "export_sidecar")
_HUNYUAN_ADAPTER = "hunyuan-zerogpu"


def validate_hunyuan_manifest_parity(payload: Mapping[str, Any]) -> list[str]:
    """Validate a Hunyuan run manifest matches the cpu-demo trust contract shape."""
    issues: list[str] = []

    stage = payload.get("stage")
    if stage != "done":
        issues.append(f"Expected stage done, got {stage!r}")

    adapter = str(payload.get("adapter") or "")
    if adapter != _HUNYUAN_ADAPTER:
        issues.append(f"Expected adapter {_HUNYUAN_ADAPTER!r}, got {adapter!r}")

    parameters = payload.get("parameters")
    if not isinstance(parameters, dict):
        issues.append("Manifest missing parameters object")
        parameters = {}

    for key in _REQUIRED_PARAMETER_KEYS:
        if key not in parameters:
            issues.append(f"Manifest parameters missing {key!r}")

    selected = str(parameters.get("selected_adapter") or "")
    if selected != _HUNYUAN_ADAPTER:
        issues.append(
            f"Expected selected_adapter {_HUNYUAN_ADAPTER!r}, got {selected!r}"
        )

    if parameters.get("fallback_reason"):
        issues.append("Hunyuan sample manifest must not record cpu fallback_reason")
    if parameters.get("preview_disclaimer"):
        issues.append("Hunyuan sample manifest must not record preview_disclaimer")

    runtime = parameters.get("runtime")
    if runtime is not None and not isinstance(runtime, dict):
        issues.append("Manifest parameters.runtime must be an object")

    artifacts = payload.get("artifacts")
    if not isinstance(artifacts, dict):
        issues.append("Manifest missing artifacts object")
        artifacts = {}

    for key in _REQUIRED_ARTIFACT_KEYS:
        if key not in artifacts:
            issues.append(f"Manifest artifacts missing {key!r}")

    return issues


def load_hunyuan_sample_manifest() -> dict[str, Any]:
    if not HUNYUAN_SAMPLE_MANIFEST.is_file():
        msg = f"Hunyuan sample manifest missing: {HUNYUAN_SAMPLE_MANIFEST}"
        raise FileNotFoundError(msg)
    return json.loads(HUNYUAN_SAMPLE_MANIFEST.read_text(encoding="utf-8"))
