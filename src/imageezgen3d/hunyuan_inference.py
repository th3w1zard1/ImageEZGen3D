from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Protocol

from .adapters.base import GenerationRequest, GenerationResult
from .generation_pipeline import PipelineStageTracker

HUNYUAN_ADAPTER = "hunyuan-zerogpu"
_NOT_IMPLEMENTED_MESSAGE = (
    "Hunyuan GPU inference is not wired yet. Complete weight cache, tier-C "
    "dependencies, and hosted E2E (G7) before enablement."
)


class HunyuanInferenceBackend(Protocol):
    def run_shape_texture(
        self,
        request: GenerationRequest,
        *,
        tracker: PipelineStageTracker,
    ) -> dict[str, Path]: ...


@dataclass
class HunyuanInferenceResult:
    artifacts: dict[str, Path]
    metadata: dict[str, Any] = field(default_factory=dict)
    pipeline_stages: list[dict[str, Any]] = field(default_factory=list)


def run_hunyuan_shape_texture(
    request: GenerationRequest,
    *,
    backend: HunyuanInferenceBackend | None = None,
) -> HunyuanInferenceResult:
    """Shape then texture towers for Hunyuan3D (two-stage neural path)."""
    tracker = PipelineStageTracker()
    tracker.mark_shape_running(HUNYUAN_ADAPTER)
    if backend is not None:
        artifacts = backend.run_shape_texture(request, tracker=tracker)
        metadata = {
            "neural_backend": HUNYUAN_ADAPTER,
            "pipeline_mode": "shape+texture",
            "adapter_note": (
                "Hunyuan shape+texture inference (mock backend in tests only)."
            ),
        }
        return HunyuanInferenceResult(
            artifacts=artifacts,
            metadata=metadata,
            pipeline_stages=tracker.to_list(),
        )

    tracker.mark_shape_failed(HUNYUAN_ADAPTER, notes=_NOT_IMPLEMENTED_MESSAGE)
    raise NotImplementedError(_NOT_IMPLEMENTED_MESSAGE)


def to_generation_result(inference: HunyuanInferenceResult) -> GenerationResult:
    metadata = dict(inference.metadata)
    metadata["pipeline_stages"] = inference.pipeline_stages
    return GenerationResult(
        adapter=HUNYUAN_ADAPTER,
        artifacts=inference.artifacts,
        metadata=metadata,
    )
