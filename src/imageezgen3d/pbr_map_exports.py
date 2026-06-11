from __future__ import annotations

import base64
import io
from pathlib import Path
from typing import Mapping

from PIL import Image

from .export_tiers import PBR_MAP_SLOTS

REFERENCE_PBR_NOTES = (
    "Reference PBR map pack exported from input-derived base color with neutral "
    "normal and default metallic-roughness factors; not a neural bake."
)

PBR_MANIFEST_KEYS: dict[str, str] = {
    "base_color": "pbr_base_color",
    "normal": "pbr_normal",
    "metallic_roughness": "pbr_metallic_roughness",
    "ao": "pbr_ao",
}

PBR_MAP_FILENAMES: dict[str, str] = {
    "base_color": "base_color.png",
    "normal": "normal.png",
    "metallic_roughness": "metallic_roughness.png",
    "ao": "ao.png",
}

DEFAULT_MAP_SIZE = 512


def resolve_base_color_image(
    mesh_color: tuple[float, float, float, float],
    *,
    b64_image: str | None = None,
    size: int = DEFAULT_MAP_SIZE,
) -> Image.Image:
    if b64_image:
        raw = base64.b64decode(b64_image)
        with Image.open(io.BytesIO(raw)) as image:
            rgb = image.convert("RGB")
            if rgb.size != (size, size):
                rgb = rgb.resize((size, size), Image.LANCZOS)
            return rgb.copy()

    red, green, blue, _alpha = mesh_color
    return Image.new(
        "RGB",
        (size, size),
        (
            int(max(0.0, min(1.0, red)) * 255),
            int(max(0.0, min(1.0, green)) * 255),
            int(max(0.0, min(1.0, blue)) * 255),
        ),
    )


def write_reference_pbr_maps(
    export_dir: Path,
    *,
    base_color_image: Image.Image,
    size: int = DEFAULT_MAP_SIZE,
) -> tuple[dict[str, Path], dict[str, str]]:
    """Write reference PBR map PNGs under export_dir/pbr/."""
    maps_dir = export_dir / "pbr"
    maps_dir.mkdir(parents=True, exist_ok=True)
    run_root = export_dir.parent

    base_color = base_color_image.convert("RGB")
    if base_color.size != (size, size):
        base_color = base_color.resize((size, size), Image.LANCZOS)
    normal = Image.new("RGB", (size, size), (128, 128, 255))
    metallic_roughness = Image.new("RGB", (size, size), (0, 180, 0))
    ao = Image.new("L", (size, size), 255)

    written: dict[str, Path] = {}
    for slot, filename in PBR_MAP_FILENAMES.items():
        path = maps_dir / filename
        if slot == "base_color":
            base_color.save(path, format="PNG")
        elif slot == "normal":
            normal.save(path, format="PNG")
        elif slot == "metallic_roughness":
            metallic_roughness.save(path, format="PNG")
        else:
            ao.save(path, format="PNG")
        written[slot] = path

    sidecar_paths = {
        slot: str(path.relative_to(run_root)) for slot, path in written.items()
    }
    return written, sidecar_paths


def pbr_manifest_artifacts(written: Mapping[str, Path]) -> dict[str, Path]:
    artifacts: dict[str, Path] = {}
    for slot in PBR_MAP_SLOTS:
        path = written.get(slot)
        if path is None:
            continue
        artifacts[PBR_MANIFEST_KEYS[slot]] = path
    return artifacts
