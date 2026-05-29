from __future__ import annotations

from pathlib import Path

from .adapters.base import GenerationRequest
from .generation_pipeline import PipelineStageTracker
from .hunyuan_inference import HUNYUAN_ADAPTER, HunyuanMeshResult
from .tencent_hunyuan_forward import (
    ShapeForwardExecutor,
    TextureForwardExecutor,
)
from .tencent_hunyuan_pipeline import (
    TencentPipelineReadinessError,
    TencentStageContext,
    build_tencent_shape_forward_plan,
    ensure_tencent_pipeline_ready,
    run_tencent_shape_stage,
    run_tencent_texture_stage,
)
from .tencent_mesh_convert import simple_mesh_from_obj


class TencentHunyuanInferenceRunner:
    """Tier-C Tencent runner: forward executors assemble `HunyuanMeshResult` when wired."""

    def __init__(
        self,
        *,
        shape_executor: ShapeForwardExecutor | None = None,
        texture_executor: TextureForwardExecutor | None = None,
    ) -> None:
        self._shape_executor = shape_executor
        self._texture_executor = texture_executor

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
        build_tencent_shape_forward_plan(context)

        tracker.mark_shape_running(HUNYUAN_ADAPTER)
        try:
            shape_mesh_path = run_tencent_shape_stage(
                context=context,
                shape_executor=self._shape_executor,
            )
        except NotImplementedError as exc:
            tracker.mark_shape_failed(HUNYUAN_ADAPTER, notes=str(exc))
            raise

        tracker.mark_shape_succeeded_staged(
            HUNYUAN_ADAPTER,
            notes=f"shape mesh at {shape_mesh_path.name}",
        )

        tracker.mark_texture_running(HUNYUAN_ADAPTER)
        try:
            textured_mesh_path = run_tencent_texture_stage(
                context=context,
                shape_mesh_path=shape_mesh_path,
                texture_executor=self._texture_executor,
            )
        except NotImplementedError as exc:
            tracker.mark_texture_failed(HUNYUAN_ADAPTER, notes=str(exc))
            raise

        tracker.mark_texture_succeeded(
            HUNYUAN_ADAPTER,
            notes=f"textured mesh at {textured_mesh_path.name}",
        )
        mesh = simple_mesh_from_obj(textured_mesh_path)
        return HunyuanMeshResult(mesh=mesh, raw_mesh=None)
