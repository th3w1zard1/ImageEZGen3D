from __future__ import annotations

from typing import Any, Mapping

UI_ARTIFACT_PREFIX_KEYS: tuple[str, ...] = (
    "manifest",
    "glb",
    "obj",
    "ply",
    "stl",
)
UI_DELIVERY_FORMAT_ORDER: tuple[str, ...] = ("fbx", "usdz", "3mf")
UI_ARTIFACT_SUFFIX_KEYS: tuple[str, ...] = ("export_sidecar", "raw_glb", "bundle")

# `/generate` returns model + status + preview_extras before download slots (see app.py).
GENERATE_LEADING_OUTPUT_COUNT = 3

UI_ARTIFACT_LABELS: dict[str, str] = {
    "manifest": "Manifest",
    "glb": "GLB",
    "obj": "OBJ",
    "ply": "PLY",
    "stl": "STL",
    "fbx": "FBX",
    "usdz": "USDZ",
    "3mf": "3MF",
    "export_sidecar": "Export sidecar",
    "raw_glb": "RAW GLB",
    "bundle": "All artifacts (ZIP)",
}

# Python identifiers for gr.File bindings (3mf is not a valid bare name).
CREATE_COMPONENT_NAMES: dict[str, str] = {
    "3mf": "threemf_file",
    "export_sidecar": "export_sidecar_file",
    "raw_glb": "raw_glb_file",
    "bundle": "bundle_file",
}

HISTORY_COMPONENT_PREFIX = "history_"
HISTORY_COMPONENT_OVERRIDES: dict[str, str] = {
    "3mf": "history_threemf",
    "export_sidecar": "history_export_sidecar",
    "raw_glb": "history_raw_glb",
    "bundle": "history_bundle",
}


def normalize_export_formats(formats: tuple[str, ...] | list[str] | None) -> tuple[str, ...]:
    if not formats:
        return ()
    return tuple(fmt.strip().lower() for fmt in formats if str(fmt).strip())


def resolve_ui_delivery_keys(config_formats: tuple[str, ...] | list[str] | None) -> tuple[str, ...]:
    normalized = set(normalize_export_formats(config_formats))
    return tuple(key for key in UI_DELIVERY_FORMAT_ORDER if key in normalized)


def resolve_gradio_download_keys(
    config_formats: tuple[str, ...] | list[str] | None,
) -> tuple[str, ...]:
    delivery = resolve_ui_delivery_keys(config_formats)
    return UI_ARTIFACT_PREFIX_KEYS + delivery + UI_ARTIFACT_SUFFIX_KEYS


def resolve_artifact_row_layout(
    config_formats: tuple[str, ...] | list[str] | None,
) -> tuple[tuple[str, ...], ...]:
    delivery = resolve_ui_delivery_keys(config_formats)
    delivery_rows: list[tuple[str, ...]] = []
    for index in range(0, len(delivery), 2):
        delivery_rows.append(delivery[index : index + 2])
    return (
        ("manifest", "glb", "obj"),
        ("ply", "stl"),
        *delivery_rows,
        UI_ARTIFACT_SUFFIX_KEYS,
    )


def create_component_name(key: str) -> str:
    return CREATE_COMPONENT_NAMES.get(key, f"{key}_file")


def history_component_name(key: str) -> str:
    if key in HISTORY_COMPONENT_OVERRIDES:
        return HISTORY_COMPONENT_OVERRIDES[key]
    return f"{HISTORY_COMPONENT_PREFIX}{key}"


def generate_download_index(
    key: str,
    config_formats: tuple[str, ...] | list[str] | None,
) -> int:
    keys = resolve_gradio_download_keys(config_formats)
    if key not in keys:
        raise KeyError(f"Unknown generate download key: {key}")
    return GENERATE_LEADING_OUTPUT_COUNT + keys.index(key)


def generate_output_indices(
    config_formats: tuple[str, ...] | list[str] | None,
) -> dict[str, int]:
    download_keys = resolve_gradio_download_keys(config_formats)
    indices = {
        key: GENERATE_LEADING_OUTPUT_COUNT + offset
        for offset, key in enumerate(download_keys)
    }
    tail_base = GENERATE_LEADING_OUTPUT_COUNT + len(download_keys)
    indices.update(
        {
            "session_state": tail_base,
            "history_run": tail_base + 1,
            "history_compare_run": tail_base + 2,
            "history_notice": tail_base + 3,
            "history_summary": tail_base + 4,
            "create_history_summary": tail_base + 5,
            "assets_gallery": tail_base + 6,
        }
    )
    return indices


def artifact_download_values(
    verified: Mapping[str, Any],
    keys: tuple[str, ...],
    *,
    bundle_path: str | None = None,
) -> tuple[Any, ...]:
    values: list[Any] = []
    for key in keys:
        if key == "bundle":
            values.append(bundle_path)
        else:
            values.append(verified.get(key))
    return tuple(values)


def session_artifact_values(
    state: Mapping[str, Any],
    keys: tuple[str, ...],
) -> tuple[Any, ...]:
    return tuple(state.get(key) for key in keys)


def sync_session_artifact_keys(
    state: dict[str, Any],
    verified: Mapping[str, Any],
    keys: tuple[str, ...],
) -> None:
    for key in keys:
        if key == "bundle":
            continue
        state[key] = verified.get(key)
