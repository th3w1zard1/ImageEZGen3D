from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageStat

from ..exporters import SimpleMesh


def prompt_digest(prompt: str) -> bytes:
    return hashlib.sha256((prompt or "").strip().encode("utf-8")).digest()


def fuse_multi_view_color(
    primary_stat: ImageStat.Stat,
    view_images: dict[str, Path],
    *,
    fallback: tuple[float, float, float],
) -> tuple[float, float, float]:
    channels = [list(primary_stat.mean[:3])]
    for path in view_images.values():
        if not path.is_file():
            continue
        view_stat = ImageStat.Stat(Image.open(path).convert("RGB").resize((64, 64)))
        channels.append(list(view_stat.mean[:3]))
    if len(channels) == 1:
        return fallback
    fused = [
        sum(row[index] for row in channels) / len(channels) for index in range(3)
    ]
    return fused[0], fused[1], fused[2]


def procedural_image_from_prompt(
    prompt: str,
    *,
    size: tuple[int, int] = (512, 512),
) -> Image.Image:
    digest = prompt_digest(prompt)
    width, height = size
    image = Image.new("RGB", (width, height))
    draw = ImageDraw.Draw(image)
    hue = digest[0] / 255.0
    base = (
        int(40 + 180 * hue),
        int(50 + 160 * (digest[1] / 255.0)),
        int(60 + 140 * (digest[2] / 255.0)),
    )
    draw.rectangle((0, 0, width, height), fill=base)
    for index in range(6):
        offset = digest[(index + 3) % len(digest)]
        radius = 30 + (offset % 90)
        center = (
            (digest[index] * width) // 255,
            (digest[(index + 5) % len(digest)] * height) // 255,
        )
        color = (
            (base[0] + offset) % 256,
            (base[1] + index * 17) % 256,
            (base[2] + index * 29) % 256,
        )
        draw.ellipse(
            (
                center[0] - radius,
                center[1] - radius,
                center[0] + radius,
                center[1] + radius,
            ),
            fill=color,
        )
    draw.text((16, 16), (prompt or "prompt")[:48], fill=(240, 240, 240))
    return image.filter(ImageFilter.GaussianBlur(radius=0.6))


def image_to_image_transform(
    source: Image.Image,
    prompt: str,
    *,
    size: tuple[int, int] = (512, 512),
) -> Image.Image:
    digest = prompt_digest(prompt)
    base = source.convert("RGB").resize(size, Image.LANCZOS)
    tint = Image.new(
        "RGB",
        size,
        (
            int(80 + digest[0] / 2),
            int(80 + digest[1] / 2),
            int(80 + digest[2] / 2),
        ),
    )
    blended = Image.blend(base, tint, alpha=0.25 + (digest[3] % 40) / 100)
    overlay = procedural_image_from_prompt(prompt, size=size).resize(size)
    return Image.blend(blended, overlay, alpha=0.18)


def depth_relief_mesh(
    image: Image.Image,
    *,
    grid_size: int = 48,
    max_height: float = 0.12,
    invert: bool = False,
) -> SimpleMesh:
    gray = image.convert("L").resize((grid_size, grid_size), Image.LANCZOS)
    pixels = list(gray.getdata())
    vertices: list[tuple[float, float, float]] = []
    for row in range(grid_size):
        for col in range(grid_size):
            value = pixels[row * grid_size + col] / 255.0
            if invert:
                value = 1.0 - value
            z = value * max_height
            x = (col / (grid_size - 1)) - 0.5
            y = (row / (grid_size - 1)) - 0.5
            vertices.append((x, y, z))
    faces: list[tuple[int, int, int]] = []
    for row in range(grid_size - 1):
        for col in range(grid_size - 1):
            top_left = row * grid_size + col
            top_right = top_left + 1
            bottom_left = top_left + grid_size
            bottom_right = bottom_left + 1
            faces.append((top_left, bottom_left, top_right))
            faces.append((top_right, bottom_left, bottom_right))
    mean = sum(pixels) / max(1, len(pixels))
    shade = mean / 255.0
    color = (0.45 + 0.4 * shade, 0.42 + 0.35 * shade, 0.38 + 0.3 * shade, 1.0)
    return SimpleMesh(vertices=tuple(vertices), faces=tuple(faces), color=color)


def humanoid_bone_hierarchy() -> list[dict[str, object]]:
    return [
        {"name": "hips", "parent": None, "head": [0.0, 0.9, 0.0], "tail": [0.0, 1.0, 0.0]},
        {"name": "spine", "parent": "hips", "head": [0.0, 1.0, 0.0], "tail": [0.0, 1.35, 0.0]},
        {"name": "head", "parent": "spine", "head": [0.0, 1.35, 0.0], "tail": [0.0, 1.65, 0.0]},
        {"name": "arm.L", "parent": "spine", "head": [0.0, 1.25, 0.0], "tail": [-0.35, 1.15, 0.0]},
        {"name": "arm.R", "parent": "spine", "head": [0.0, 1.25, 0.0], "tail": [0.35, 1.15, 0.0]},
        {"name": "leg.L", "parent": "hips", "head": [0.0, 0.9, 0.0], "tail": [-0.15, 0.45, 0.0]},
        {"name": "leg.R", "parent": "hips", "head": [0.0, 0.9, 0.0], "tail": [0.15, 0.45, 0.0]},
    ]


def animation_catalog_path() -> Path:
    candidates = [
        Path(__file__).resolve().parents[3] / "docs/reference/meshy/animation-library.json",
        Path.cwd() / "docs/reference/meshy/animation-library.json",
    ]
    for candidate in candidates:
        if candidate.is_file():
            return candidate
    raise FileNotFoundError(
        "Animation catalog not found. Expected docs/reference/meshy/animation-library.json"
    )


def load_animation_catalog() -> dict[str, object]:
    return json.loads(animation_catalog_path().read_text(encoding="utf-8"))


def resolve_animation_entry(action_id: str | int | None) -> dict[str, object]:
    catalog = load_animation_catalog()
    items = catalog.get("result", {}).get("list", [])
    if not isinstance(items, list):
        raise ValueError("Animation catalog is malformed.")
    if action_id is None:
        for item in items:
            if item.get("isDefault"):
                return item
        return items[0]
    target = str(action_id)
    for item in items:
        if str(item.get("id")) == target or str(item.get("key")) == target:
            return item
    raise ValueError(f"Animation action_id '{action_id}' not found in catalog.")
