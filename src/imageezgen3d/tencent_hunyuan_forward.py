from __future__ import annotations

from pathlib import Path
from typing import Any, Callable, Protocol

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


class TencentForwardExecutor(Protocol):
    """Pluggable upstream forward hook (tests inject; default stops before GPU)."""

    def __call__(self, plan: TencentShapeForwardPlan, pipeline_cls: type[Any] | None) -> Path: ...


def import_tencent_pipeline_class(module_name: str, class_name: str) -> type[Any]:
    import importlib

    module = importlib.import_module(module_name)
    return getattr(module, class_name)


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
