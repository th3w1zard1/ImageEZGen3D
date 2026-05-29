from __future__ import annotations

from pathlib import Path
from typing import Protocol

from .adapters.base import GenerationRequest
from .config import HunyuanSettings, load_config
from .generation_pipeline import PipelineStageTracker
from .hunyuan_inference import HunyuanMeshResult

_UNWIRED_RUNNER_NOTE = (
    "No Hunyuan inference runner is registered. Tier-C Tencent wiring remains future work."
)


class HunyuanInferenceRunner(Protocol):
    """Tier-C neural shape+texture runner (Tencent Hunyuan3D integration seam)."""

    def run_shape_texture(
        self,
        request: GenerationRequest,
        *,
        tracker: PipelineStageTracker,
        weight_root: Path,
        shape_checkpoint: Path,
    ) -> HunyuanMeshResult: ...


def resolve_hunyuan_inference_runner(
    settings: HunyuanSettings | None = None,
) -> HunyuanInferenceRunner | None:
    """Return a wired runner when tier-C inference is implemented; default is unwired."""
    _ = settings or load_config().hunyuan
    return None


def describe_hunyuan_inference_runner(
    settings: HunyuanSettings | None = None,
) -> dict[str, str | bool]:
    runner = resolve_hunyuan_inference_runner(settings)
    return {
        "inference_wired": runner is not None,
        "runner_id": type(runner).__name__ if runner is not None else "",
        "note": _UNWIRED_RUNNER_NOTE if runner is None else "Inference runner registered.",
    }
