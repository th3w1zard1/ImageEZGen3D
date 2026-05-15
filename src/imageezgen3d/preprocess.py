from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from PIL import Image, ImageChops, ImageOps, ImageStat

from .storage import atomic_write_json


@dataclass
class ImageValidationReport:
    width: int
    height: int
    mode: str
    score: int
    issues: list[str] = field(default_factory=list)
    metrics: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "width": self.width,
            "height": self.height,
            "mode": self.mode,
            "score": self.score,
            "issues": self.issues,
            "metrics": self.metrics,
        }


def _edge_variance(image: Image.Image) -> float:
    gray = ImageOps.grayscale(image).resize((128, 128))
    edges = gray.filter(ImageFilterLike.find_edges())
    stat = ImageStat.Stat(edges)
    return float(stat.var[0])


class ImageFilterLike:
    @staticmethod
    def find_edges():
        from PIL import ImageFilter

        return ImageFilter.FIND_EDGES


def validate_image(
    image: Image.Image,
    *,
    minimum_short_side: int = 256,
    maximum_long_side: int = 4096,
    blur_edge_variance_threshold: float = 90.0,
    low_contrast_threshold: float = 18.0,
) -> ImageValidationReport:
    image = ImageOps.exif_transpose(image)
    width, height = image.size
    issues: list[str] = []
    score = 100

    if min(width, height) < minimum_short_side:
        issues.append(
            "Image is small; use at least 512 px on the shortest side for better geometry."
        )
        score -= 25
    if max(width, height) > maximum_long_side:
        issues.append(
            "Image is very large; it will be downscaled for a predictable CPU/ZeroGPU path."
        )
        score -= 5

    aspect = max(width, height) / max(1, min(width, height))
    if aspect > 2.2:
        issues.append(
            "Image is extremely wide/tall; crop around one centered subject before generation."
        )
        score -= 15

    edge_var = _edge_variance(image)
    if edge_var < blur_edge_variance_threshold:
        issues.append(
            "Image may be soft or low-detail; sharper edges usually improve reconstruction."
        )
        score -= 20

    has_alpha = image.mode in ("RGBA", "LA") or (
        image.mode == "P" and "transparency" in image.info
    )
    if not has_alpha:
        issues.append(
            "No alpha channel detected; background removal or a clean plain background is recommended."
        )
        score -= 8

    rgb = image.convert("RGB").resize((64, 64))
    stat = ImageStat.Stat(rgb)
    mean = sum(stat.mean) / 3
    spread = sum(stat.stddev) / 3
    if mean < 35 or mean > 225:
        issues.append("Exposure is extreme; avoid very dark or blown-out subjects.")
        score -= 10
    if spread < low_contrast_threshold:
        issues.append(
            "Low contrast or featureless material detected; matte textured inputs work best."
        )
        score -= 12

    return ImageValidationReport(
        width=width,
        height=height,
        mode=image.mode,
        score=max(0, min(100, score)),
        issues=issues,
        metrics={
            "edge_variance": round(edge_var, 3),
            "mean_luma": round(mean, 3),
            "contrast": round(spread, 3),
            "has_alpha": has_alpha,
        },
    )


def normalize_image(image: Image.Image, size: int = 768) -> Image.Image:
    image = ImageOps.exif_transpose(image)
    if image.mode not in ("RGBA", "RGB"):
        image = image.convert("RGBA")
    if image.mode == "RGBA":
        background = Image.new("RGBA", image.size, (245, 247, 250, 255))
        image = Image.alpha_composite(background, image).convert("RGB")
    else:
        image = image.convert("RGB")

    image.thumbnail((size, size), Image.Resampling.LANCZOS)
    canvas = Image.new("RGB", (size, size), (245, 247, 250))
    offset = ((size - image.width) // 2, (size - image.height) // 2)
    canvas.paste(image, offset)
    return canvas


def save_input_bundle(
    image: Image.Image,
    input_path: Path,
    processed_path: Path,
    report_path: Path,
    *,
    target_size: int = 768,
    minimum_short_side: int = 256,
    maximum_long_side: int = 4096,
    blur_edge_variance_threshold: float = 90.0,
    low_contrast_threshold: float = 18.0,
) -> ImageValidationReport:
    input_path.parent.mkdir(parents=True, exist_ok=True)
    processed_path.parent.mkdir(parents=True, exist_ok=True)
    report = validate_image(
        image,
        minimum_short_side=minimum_short_side,
        maximum_long_side=maximum_long_side,
        blur_edge_variance_threshold=blur_edge_variance_threshold,
        low_contrast_threshold=low_contrast_threshold,
    )
    original = ImageOps.exif_transpose(image)
    original.save(input_path)
    normalize_image(original, size=target_size).save(processed_path)
    atomic_write_json(report_path, report.to_dict())
    return report
