from __future__ import annotations

from typing import Any, Mapping

DECIMATION_TARGET_BY_QUALITY: dict[str, int] = {
    "draft": 25_000,
    "balanced": 150_000,
    "high": 500_000,
}

PBR_MAP_SLOTS = ("base_color", "normal", "metallic_roughness", "ao")


def resolve_decimation_target(quality: str | None, *, default: int = 500_000) -> int:
    normalized = (quality or "draft").strip().lower()
    return DECIMATION_TARGET_BY_QUALITY.get(normalized, default)


def build_pbr_delivery_block(
    *,
    adapter: str,
    pbr_available: bool = False,
    map_paths: Mapping[str, str | None] | None = None,
    workflow: str = "metallic-roughness",
) -> dict[str, Any]:
    """Khronos-style PBR delivery metadata for export sidecars."""
    maps: dict[str, str | None] = {slot: None for slot in PBR_MAP_SLOTS}
    if map_paths:
        for slot in PBR_MAP_SLOTS:
            value = map_paths.get(slot)
            maps[slot] = str(value) if value else None
    if pbr_available and not any(maps.values()):
        pbr_available = False
    notes = (
        "Separate PBR texture maps are present and referenced below."
        if pbr_available
        else (
            "Factor-only materials embedded in GLB; separate map files not exported "
            f"for adapter {adapter!r}."
        )
    )
    return {
        "workflow": workflow,
        "pbr_available": pbr_available,
        "material_model": "metallic-roughness",
        "maps": maps,
        "notes": notes,
    }


def build_export_sidecar(
    *,
    quality: str,
    decimation_target: int,
    vertex_count: int,
    face_count: int,
    adapter: str,
    decimation: Mapping[str, Any] | None = None,
    raw_exported: bool = False,
    pbr_available: bool = False,
    pbr_map_paths: Mapping[str, str | None] | None = None,
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "export_tier": quality,
        "decimation_target_faces": decimation_target,
        "mesh_topology": {
            "vertex_count": vertex_count,
            "face_count": face_count,
        },
        "within_decimation_budget": face_count <= decimation_target,
        "raw_exported": raw_exported,
        "adapter": adapter,
        "notes": (
            "Sidecar records export intent and measured topology. "
            "Tier exports may be decimated; RAW GLB preserves pre-decimation mesh when present."
        ),
        "pbr_delivery": build_pbr_delivery_block(
            adapter=adapter,
            pbr_available=pbr_available,
            map_paths=pbr_map_paths,
        ),
    }
    if decimation:
        payload["decimation"] = dict(decimation)
    return payload


def apply_pbr_stage_from_sidecar(
    tracker: Any,
    sidecar: Mapping[str, Any],
    *,
    adapter: str,
) -> None:
    """Update pipeline pbr stage from export sidecar pbr_delivery block."""
    delivery = sidecar.get("pbr_delivery")
    if not isinstance(delivery, dict):
        tracker.set_stage(
            "pbr",
            "skipped",
            notes="Export sidecar missing pbr_delivery block.",
        )
        return
    if delivery.get("pbr_available") is True:
        tracker.set_stage(
            "pbr",
            "succeeded",
            adapter=adapter,
            notes=str(delivery.get("notes") or "PBR map pack exported."),
        )
        return
    tracker.set_stage(
        "pbr",
        "skipped",
        notes=str(
            delivery.get("notes")
            or "Separate PBR maps not available for this adapter."
        ),
    )


def decimation_target_from_parameters(parameters: Mapping[str, Any]) -> int | None:
    value = parameters.get("decimation_target")
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        return int(value)
    return None
