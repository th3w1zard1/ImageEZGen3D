from __future__ import annotations

from pathlib import Path

from .adapters.base import GenerationRequest
from .generation_pipeline import PipelineStageTracker
from .hunyuan_inference import HUNYUAN_ADAPTER, HunyuanMeshResult
from .tencent_hunyuan_pipeline import (
    TencentPipelineReadinessError,
    TencentStageContext,
    ensure_tencent_pipeline_ready,
    run_tencent_shape_stage,
    run_tencent_texture_stage,
)


class TencentHunyuanInferenceRunner:
    """Tier-C Tencent runner: validates weights, resolves pipeline bindings, stops before forward."""

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

        try:
            ensure_tencent_pipeline_ready()
        except TencentPipelineReadinessError as exc:
            tracker.mark_shape_failed(HUNYUAN_ADAPTER, notes=str(exc))
            raise NotImplementedError(str(exc)) from exc

        context = TencentStageContext(
            run_dir=Path(request.run_dir),
            processed_image=Path(request.processed_image),
            weight_root=weight_root,
            shape_checkpoint=shape_checkpoint,
        )

        tracker.mark_shape_running(HUNYUAN_ADAPTER)
        try:
            run_tencent_shape_stage(context=context)
        except NotImplementedError as exc:
            tracker.mark_shape_failed(HUNYUAN_ADAPTER, notes=str(exc))
            raise

        tracker.mark_texture_running(HUNYUAN_ADAPTER)
        try:
            run_tencent_texture_stage(context=context)
        except NotImplementedError as exc:
            tracker.mark_texture_failed(HUNYUAN_ADAPTER, notes=str(exc))
            raise

        message = "Tencent Hunyuan3D texture stage completed without mesh output."
        tracker.mark_texture_failed(HUNYUAN_ADAPTER, notes=message)
        raise NotImplementedError(message)
