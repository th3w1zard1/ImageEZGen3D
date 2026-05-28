from __future__ import annotations

from dataclasses import replace
from typing import TYPE_CHECKING, Any, Callable, TypeVar

from .base import AdapterCapabilities, GenerationRequest, GenerationResult
from ..text_neural_inference import run_text_neural_shape, to_generation_result

if TYPE_CHECKING:
    from ..config import AppConfig

F = TypeVar("F", bound=Callable[..., Any])

_DEFAULT_GPU_DURATION_SECONDS = 120

_BASE_CAPABILITIES = AdapterCapabilities(
    name="text-neural",
    cpu_safe=False,
    zerogpu_ready=True,
    configured=False,
    supports_multi_view=False,
    outputs=("glb", "obj"),
    notes=(
        "Text-to-3D neural placeholder. Enable only after license audit and "
        "admission review for the chosen model stack."
    ),
)


def _spaces_gpu_decorator(duration: int = _DEFAULT_GPU_DURATION_SECONDS) -> Callable[[F], F]:
    try:
        import spaces  # type: ignore[import-untyped]
    except ImportError:
        return lambda function: function

    gpu_factory = getattr(spaces, "GPU", None)
    if gpu_factory is None:
        return lambda function: function
    return gpu_factory(duration=duration)


@_spaces_gpu_decorator(duration=_DEFAULT_GPU_DURATION_SECONDS)
def _run_text_neural_inference_on_gpu(request: GenerationRequest) -> GenerationResult:
    return to_generation_result(run_text_neural_shape(request))


def resolve_text_neural_configured(*, config: AppConfig | None = None) -> bool:
    if config is not None:
        return config.text_neural.configured
    from ..config import load_config

    return load_config().text_neural.configured


class TextNeuralPlaceholderAdapter:
    def __init__(self, *, configured: bool | None = None) -> None:
        flag = (
            resolve_text_neural_configured()
            if configured is None
            else configured
        )
        self.capabilities = replace(_BASE_CAPABILITIES, configured=flag)

    def generate(self, request: GenerationRequest) -> GenerationResult:
        if not self.capabilities.configured:
            raise RuntimeError(
                "The text-neural adapter is intentionally disabled. "
                "Complete license-audit.md and adapter admission review before enabling."
            )
        return _run_text_neural_inference_on_gpu(request)
