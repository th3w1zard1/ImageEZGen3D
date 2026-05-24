from __future__ import annotations

from typing import Any, Mapping

DECIMATION_TARGET_BY_QUALITY: dict[str, int] = {
    "draft": 25_000,
    "balanced": 150_000,
    "high": 500_000,
}


def resolve_decimation_target(quality: str | None, *, default: int = 500_000) -> int:
    normalized = (quality or "draft").strip().lower()
    return DECIMATION_TARGET_BY_QUALITY.get(normalized, default)


def build_export_sidecar(
    *,
    quality: str,
    decimation_target: int,
    vertex_count: int,
    face_count: int,
    adapter: str,
) -> dict[str, Any]:
    return {
        "export_tier": quality,
        "decimation_target_faces": decimation_target,
        "mesh_topology": {
            "vertex_count": vertex_count,
            "face_count": face_count,
        },
        "within_decimation_budget": face_count <= decimation_target,
        "adapter": adapter,
        "notes": (
            "Sidecar records export intent and measured topology. "
            "Neural backends should apply decimation_target at export time."
        ),
    }


def decimation_target_from_parameters(parameters: Mapping[str, Any]) -> int | None:
    value = parameters.get("decimation_target")
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        return int(value)
    return None
