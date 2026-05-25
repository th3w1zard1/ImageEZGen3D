from __future__ import annotations

from typing import Any, Callable, TypeVar

from .base import AdapterCapabilities, GenerationRequest, GenerationResult

F = TypeVar("F", bound=Callable[..., Any])

# Future hosted inference must run inside @spaces.GPU (see zerogpu-runtime.md).
_DEFAULT_GPU_DURATION_SECONDS = 120


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
    """GPU-isolated Hunyuan inference shell (G4). Not implemented until G3/G5–G7 close."""
    _ = request
    raise NotImplementedError(
        "Hunyuan GPU inference is not wired yet. Complete dependency audit (G3), "
        "resource fit (G5), and hosted E2E (G7) before enablement."
    )


class HunyuanPlaceholderAdapter:
    capabilities = AdapterCapabilities(
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

    def generate(self, request: GenerationRequest) -> GenerationResult:
        if not self.capabilities.configured:
            raise RuntimeError(
                "The Hunyuan ZeroGPU adapter is intentionally disabled. "
                "Complete the admission gates in docs/knowledgebase/hunyuan-admission-gates.md "
                "(and license-audit.md) before enabling this adapter."
            )
        return _run_hunyuan_inference_on_gpu(request)
