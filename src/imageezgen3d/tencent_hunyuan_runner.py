from __future__ import annotations

from pathlib import Path

from .adapters.base import GenerationRequest
from .generation_pipeline import PipelineStageTracker
from .hunyuan_inference import HUNYUAN_ADAPTER, HunyuanMeshResult

_TENCENT_INTEGRATION_NOTE = (
    "Tencent Hunyuan3D shape+texture pipeline is not integrated yet."
)


class TencentHunyuanInferenceRunner:
    """Tier-C Tencent runner shell: validates weights, stops before neural inference."""

    def run_shape_texture(
        self,
        request: GenerationRequest,
        *,
        tracker: PipelineStageTracker,
        weight_root: Path,
        shape_checkpoint: Path,
    ) -> HunyuanMeshResult:
        if not shape_checkpoint.is_file():
            message = (
                f"Hunyuan shape checkpoint missing at {shape_checkpoint} "
                f"(weight root {weight_root})"
            )
            tracker.mark_shape_failed(HUNYUAN_ADAPTER, notes=message)
            raise FileNotFoundError(message)

        tracker.mark_shape_running(HUNYUAN_ADAPTER)
        message = (
            f"{_TENCENT_INTEGRATION_NOTE} Checkpoint verified at {shape_checkpoint}."
        )
        tracker.mark_shape_failed(HUNYUAN_ADAPTER, notes=message)
        raise NotImplementedError(message)
