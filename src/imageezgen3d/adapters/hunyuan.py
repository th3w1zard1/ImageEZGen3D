from __future__ import annotations

from dataclasses import replace
from typing import TYPE_CHECKING, Any, Callable, TypeVar

from .base import AdapterCapabilities, GenerationRequest, GenerationResult
from ..hunyuan_inference import run_hunyuan_shape_texture, to_generation_result

if TYPE_CHECKING:
    from ..config import AppConfig

F = TypeVar("F", bound=Callable[..., Any])

# Future hosted inference must run inside @spaces.GPU (see zerogpu-runtime.md).
_DEFAULT_GPU_DURATION_SECONDS = 120

_BASE_CAPABILITIES = AdapterCapabilities(
    name="hunyuan-zerogpu",
    cpu_safe=False,
    zerogpu_ready=True,
    configured=False,
    supports_multi_view=True,
    outputs=("glb", "obj"),
    notes=(
        "ZeroGPU-first placeholder. GPU path uses @spaces.GPU scaffold; "
        "enable only after admission gates G1–G8 close."
    ),
)


def _spaces_gpu_decorator(duration: int = _DEFAULT_GPU_DURATION_SECONDS) -> Callable[[F], F]:
    """Apply Hugging Face @spaces.GPU when the `spaces` package is available."""
    try:
        import spaces  # type: ignore[import-untyped]
    except ImportError:
        return lambda function: function

    gpu_factory = getattr(spaces, "GPU", None)
    if gpu_factory is None:
        return lambda function: function
    return gpu_factory(duration=duration)


@_spaces_gpu_decorator(duration=_DEFAULT_GPU_DURATION_SECONDS)
def _run_hunyuan_inference_on_gpu(request: GenerationRequest) -> GenerationResult:
    """GPU-isolated Hunyuan inference (G4). Delegates to hunyuan_inference module."""
    return to_generation_result(run_hunyuan_shape_texture(request))


def resolve_hunyuan_configured(*, config: AppConfig | None = None) -> bool:
    """Configured flag from AppConfig (env/pyproject), matching orchestrator wiring."""
    if config is not None:
        return config.hunyuan.configured
    from ..config import load_config

    return load_config().hunyuan.configured


class HunyuanPlaceholderAdapter:
    def __init__(self, *, configured: bool | None = None) -> None:
        flag = resolve_hunyuan_configured() if configured is None else configured
        self.capabilities = replace(_BASE_CAPABILITIES, configured=flag)

    def generate(self, request: GenerationRequest) -> GenerationResult:
        if not self.capabilities.configured:
            raise RuntimeError(
                "The Hunyuan ZeroGPU adapter is intentionally disabled. "
                "Complete the admission gates in docs/knowledgebase/hunyuan-admission-gates.md "
                "(and license-audit.md) before enabling this adapter."
            )
        return _run_hunyuan_inference_on_gpu(request)
