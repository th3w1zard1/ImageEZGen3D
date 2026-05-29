from __future__ import annotations

from pathlib import Path
from typing import Any, Callable, Protocol

from .config import HunyuanSettings, load_config
from .tencent_hunyuan_pipeline import (
    TencentShapeForwardPlan,
    TencentTextureForwardPlan,
)

ShapeForwardExecutor = Callable[[TencentShapeForwardPlan, type[Any] | None], Path]
TextureForwardExecutor = Callable[[TencentTextureForwardPlan, type[Any] | None], Path]

_SHAPE_EXECUTOR_NOT_REGISTERED = (
    "Tencent Hunyuan3D shape forward executor is not registered yet."
)
_TEXTURE_EXECUTOR_NOT_REGISTERED = (
    "Tencent Hunyuan3D texture forward executor is not registered yet."
)
_GPU_PIPELINE_CLASS_REQUIRED = (
    "Tencent GPU forward requires an importable upstream pipeline class."
)
_GPU_TORCH_REQUIRED = "Tencent GPU forward requires torch."
_GPU_CUDA_REQUIRED = "Tencent GPU forward requires CUDA."


class TencentForwardExecutor(Protocol):
    """Pluggable upstream forward hook (tests inject; default stops before GPU)."""

    def __call__(self, plan: TencentShapeForwardPlan, pipeline_cls: type[Any] | None) -> Path: ...


def import_tencent_pipeline_class(module_name: str, class_name: str) -> type[Any]:
    import importlib

    module = importlib.import_module(module_name)
    return getattr(module, class_name)


def _torch_cuda_ready() -> tuple[bool, bool]:
    try:
        import torch
    except ImportError:
        return False, False
    return True, bool(torch.cuda.is_available())


def describe_tencent_gpu_forward_readiness(
    settings: HunyuanSettings | None = None,
) -> dict[str, Any]:
    cfg = settings or load_config().hunyuan
    torch_available, cuda_available = _torch_cuda_ready()
    return {
        "gpu_forward_enabled": cfg.gpu_forward,
        "torch_available": torch_available,
        "cuda_available": cuda_available,
        "gpu_forward_ready": cfg.gpu_forward and torch_available and cuda_available,
    }


def _require_gpu_forward_ready(pipeline_cls: type[Any] | None) -> None:
    if pipeline_cls is None:
        raise NotImplementedError(_GPU_PIPELINE_CLASS_REQUIRED)
    torch_available, cuda_available = _torch_cuda_ready()
    if not torch_available:
        raise NotImplementedError(_GPU_TORCH_REQUIRED)
    if not cuda_available:
        raise NotImplementedError(_GPU_CUDA_REQUIRED)


def _first_trimesh_output(output: Any) -> Any:
    if output is None:
        msg = "Tencent shape forward returned no mesh output."
        raise RuntimeError(msg)
    if isinstance(output, list):
        for batch in output:
            if isinstance(batch, list):
                for mesh in batch:
                    if mesh is not None:
                        return mesh
            elif batch is not None:
                return batch
        msg = "Tencent shape forward returned empty mesh batches."
        raise RuntimeError(msg)
    return output


def gpu_shape_forward_executor(
    plan: TencentShapeForwardPlan,
    pipeline_cls: type[Any] | None,
) -> Path:
    """Opt-in GPU shape tower: upstream from_pretrained + __call__."""
    _require_gpu_forward_ready(pipeline_cls)
    assert pipeline_cls is not None

    pipeline = pipeline_cls.from_pretrained(
        str(plan.model_path),
        subfolder=plan.subfolder,
        device=plan.device,
        dtype=plan.dtype,
    )
    mesh = _first_trimesh_output(
        pipeline(str(plan.processed_image), output_type="trimesh"),
    )
    plan.output_mesh.parent.mkdir(parents=True, exist_ok=True)
    mesh.export(str(plan.output_mesh))
    return plan.output_mesh


def gpu_texture_forward_executor(
    plan: TencentTextureForwardPlan,
    pipeline_cls: type[Any] | None,
) -> Path:
    """Opt-in GPU texture tower: upstream paint pipeline __call__."""
    _require_gpu_forward_ready(pipeline_cls)
    assert pipeline_cls is not None
    if not plan.shape_mesh.is_file():
        msg = f"Shape mesh missing at {plan.shape_mesh}"
        raise FileNotFoundError(msg)

    pipeline = pipeline_cls()
    plan.output_mesh.parent.mkdir(parents=True, exist_ok=True)
    pipeline(
        mesh_path=str(plan.shape_mesh),
        image_path=str(plan.processed_image),
        output_mesh_path=str(plan.output_mesh),
    )
    return plan.output_mesh


def default_shape_forward_executor(
    plan: TencentShapeForwardPlan,
    pipeline_cls: type[Any] | None,
) -> Path:
    _ = (plan, pipeline_cls)
    raise NotImplementedError(_SHAPE_EXECUTOR_NOT_REGISTERED)


def default_texture_forward_executor(
    plan: TencentTextureForwardPlan,
    pipeline_cls: type[Any] | None,
) -> Path:
    _ = (plan, pipeline_cls)
    raise NotImplementedError(_TEXTURE_EXECUTOR_NOT_REGISTERED)


def resolve_tencent_forward_executors(
    settings: HunyuanSettings | None = None,
) -> tuple[ShapeForwardExecutor | None, TextureForwardExecutor | None]:
    """Return GPU executors when opt-in env is set; otherwise defer to default stubs."""
    cfg = settings or load_config().hunyuan
    if not cfg.gpu_forward:
        return None, None
    return gpu_shape_forward_executor, gpu_texture_forward_executor


def invoke_tencent_shape_forward(
    plan: TencentShapeForwardPlan,
    pipeline_cls: type[Any] | None,
    *,
    executor: ShapeForwardExecutor = default_shape_forward_executor,
) -> Path:
    return executor(plan, pipeline_cls)


def invoke_tencent_texture_forward(
    plan: TencentTextureForwardPlan,
    pipeline_cls: type[Any] | None,
    *,
    executor: TextureForwardExecutor = default_texture_forward_executor,
) -> Path:
    return executor(plan, pipeline_cls)
