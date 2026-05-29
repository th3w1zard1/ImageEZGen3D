from __future__ import annotations

import base64
import io
from pathlib import Path

from PIL import Image, ImageStat

from .adapters.base import GenerationRequest
from .exporters import SimpleMesh, make_box_mesh
from .generation_pipeline import PipelineStageTracker
from .config import HunyuanSettings
from .hunyuan_inference import HUNYUAN_ADAPTER, HunyuanInferenceBackend, HunyuanMeshResult
from .hunyuan_inference_runner import resolve_hunyuan_inference_runner
from .hunyuan_tier_c_runtime import TierCReadinessError, prepare_tier_c_runtime
from .mesh_decimation import subdivide_mesh

_DEV_PREVIEW_NOTE = (
    "Dev preview mesh derived from input image colors; not Hunyuan3D neural inference."
)
_NEURAL_SHELL_NOTE = (
    "Hunyuan weights and tier-C deps verified; inference runner is not wired yet."
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
    """Warm weights, verify tier B/C imports, then stop before inference wiring."""

    def __init__(
        self,
        *,
        settings: HunyuanSettings | None = None,
        prepare_runtime=prepare_tier_c_runtime,
    ) -> None:
        self._settings = settings
        self._prepare_runtime = prepare_runtime

    def run_shape_texture(
        self,
        request: GenerationRequest,
        *,
        tracker: PipelineStageTracker,
    ) -> HunyuanMeshResult:
        try:
            report = self._prepare_runtime(settings=self._settings)
        except TierCReadinessError as exc:
            tracker.mark_shape_failed(HUNYUAN_ADAPTER, notes=str(exc))
            raise NotImplementedError(str(exc)) from exc
        except NotImplementedError as exc:
            tracker.mark_shape_failed(HUNYUAN_ADAPTER, notes=str(exc))
            raise

        runner = resolve_hunyuan_inference_runner(self._settings)
        if runner is None:
            message = "Hunyuan inference runner is not wired yet."
            tracker.mark_shape_failed(HUNYUAN_ADAPTER, notes=message)
            raise NotImplementedError(message)

        return runner.run_shape_texture(
            request,
            tracker=tracker,
            weight_root=Path(report["weight_root"]),
            shape_checkpoint=Path(report["shape_checkpoint"]),
        )


def resolve_hunyuan_dev_backend(*, dev_enabled: bool) -> HunyuanInferenceBackend | None:
    if not dev_enabled:
        return None
    return DevPreviewHunyuanBackend()


def resolve_hunyuan_weight_backend(
    *,
    weight_enabled: bool,
    settings: HunyuanSettings | None = None,
) -> HunyuanInferenceBackend | None:
    if not weight_enabled:
        return None
    return WeightVerifiedHunyuanBackend(settings=settings)


def resolve_hunyuan_backend_from_config(
    settings: HunyuanSettings,
) -> HunyuanInferenceBackend | None:
    if settings.dev_backend:
        return DevPreviewHunyuanBackend()
    if settings.weight_backend:
        return WeightVerifiedHunyuanBackend(settings=settings)
    return None


def adapter_note_for_backend(backend: HunyuanInferenceBackend) -> str:
    if isinstance(backend, DevPreviewHunyuanBackend):
        return _DEV_PREVIEW_NOTE
    if isinstance(backend, WeightVerifiedHunyuanBackend):
        return _NEURAL_SHELL_NOTE
    return "Hunyuan shape+texture inference backend."
