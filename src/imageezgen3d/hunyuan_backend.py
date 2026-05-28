from __future__ import annotations

import base64
import io
from pathlib import Path

from PIL import Image, ImageStat

from .adapters.base import GenerationRequest
from .exporters import SimpleMesh, make_box_mesh
from .generation_pipeline import PipelineStageTracker
from .hunyuan_inference import HUNYUAN_ADAPTER, HunyuanInferenceBackend, HunyuanMeshResult
from .hunyuan_weights import ensure_hunyuan_weights
from .mesh_decimation import subdivide_mesh

_DEV_PREVIEW_NOTE = (
    "Dev preview mesh derived from input image colors; not Hunyuan3D neural inference."
)
_NEURAL_SHELL_NOTE = (
    "Hunyuan weights verified; tier-C inference runtime is not wired yet."
)
_SUBDIVIDE_LEVELS_BY_QUALITY: dict[str, int] = {
    "draft": 0,
    "balanced": 7,
    "high": 8,
}


def _mesh_from_processed_image(request: GenerationRequest) -> HunyuanMeshResult:
    if request.processed_image is None:
        raise ValueError("Hunyuan backend requires a processed input image.")
    image_path = Path(request.processed_image)
    if not image_path.is_file():
        raise FileNotFoundError(f"Processed image not found: {image_path}")

    image = Image.open(image_path).convert("RGB")
    stat = ImageStat.Stat(image.resize((64, 64)))
    red, green, blue = [channel / 255 for channel in stat.mean]
    width, height = image.size
    aspect = max(0.55, min(1.8, width / max(1, height)))
    quality_height = {"draft": 0.85, "balanced": 1.0, "high": 1.15}.get(
        request.quality, 0.9
    )
    thumb = image.resize((512, 512), Image.LANCZOS)
    buffer = io.BytesIO()
    thumb.save(buffer, format="JPEG", quality=85)
    b64_image = base64.b64encode(buffer.getvalue()).decode("utf-8")
    mesh: SimpleMesh = make_box_mesh(
        width=aspect,
        depth=0.72,
        height=quality_height,
        color=(red, green, blue, 1.0),
        b64_image=b64_image,
    )
    subdivide_levels = _SUBDIVIDE_LEVELS_BY_QUALITY.get(request.quality, 0)
    raw_mesh = subdivide_mesh(mesh, subdivide_levels) if subdivide_levels > 0 else None
    return HunyuanMeshResult(mesh=mesh, raw_mesh=raw_mesh)


class DevPreviewHunyuanBackend:
    """Local dev stand-in: image-colored preview mesh with staged tracker updates."""

    def run_shape_texture(
        self,
        request: GenerationRequest,
        *,
        tracker: PipelineStageTracker,
    ) -> HunyuanMeshResult:
        mesh_result = _mesh_from_processed_image(request)
        tracker.mark_shape_succeeded_staged(HUNYUAN_ADAPTER, notes="dev preview shape")
        tracker.mark_texture_running(HUNYUAN_ADAPTER)
        tracker.mark_texture_succeeded(HUNYUAN_ADAPTER, notes="dev preview texture")
        return mesh_result


class WeightVerifiedHunyuanBackend:
    """Warm the pinned weight cache, then stop before tier-C runtime integration."""

    def __init__(
        self,
        *,
        ensure_weights=ensure_hunyuan_weights,
        settings=None,
    ) -> None:
        self._ensure_weights = ensure_weights
        self._settings = settings

    def run_shape_texture(
        self,
        request: GenerationRequest,
        *,
        tracker: PipelineStageTracker,
    ) -> HunyuanMeshResult:
        weight_root = self._ensure_weights(settings=self._settings)
        message = (
            "Hunyuan tier-C inference runtime is not wired yet. "
            f"Weights verified at {weight_root}."
        )
        tracker.mark_shape_failed(HUNYUAN_ADAPTER, notes=message)
        raise NotImplementedError(message)


def resolve_hunyuan_dev_backend(*, dev_enabled: bool) -> HunyuanInferenceBackend | None:
    if not dev_enabled:
        return None
    return DevPreviewHunyuanBackend()


def adapter_note_for_backend(backend: HunyuanInferenceBackend) -> str:
    if isinstance(backend, DevPreviewHunyuanBackend):
        return _DEV_PREVIEW_NOTE
    if isinstance(backend, WeightVerifiedHunyuanBackend):
        return _NEURAL_SHELL_NOTE
    return "Hunyuan shape+texture inference backend."
