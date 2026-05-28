from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Protocol

from .adapters.base import GenerationRequest, GenerationResult
from .generation_pipeline import PipelineStageTracker

TEXT_NEURAL_ADAPTER = "text-neural"
_NOT_IMPLEMENTED_MESSAGE = (
    "Text neural inference is not wired yet. Complete license audit, model weights, "
    "and hosted E2E before enablement."
)


class TextNeuralInferenceBackend(Protocol):
    def run_text_shape(
        self,
        request: GenerationRequest,
        *,
        tracker: PipelineStageTracker,
    ) -> dict[str, Path]: ...


@dataclass
class TextNeuralInferenceResult:
    artifacts: dict[str, Path]
    metadata: dict[str, Any] = field(default_factory=dict)
    pipeline_stages: list[dict[str, Any]] = field(default_factory=list)


def run_text_neural_shape(
    request: GenerationRequest,
    *,
    backend: TextNeuralInferenceBackend | None = None,
) -> TextNeuralInferenceResult:
    """Text-conditioned shape generation (single-tower neural path)."""
    prompt = (request.prompt_text or "").strip()
    if not prompt:
        raise ValueError("Text neural adapter requires a non-empty prompt.")

    tracker = PipelineStageTracker()
    tracker.mark_shape_running(TEXT_NEURAL_ADAPTER)
    if backend is not None:
        artifacts = backend.run_text_shape(request, tracker=tracker)
        metadata = {
            "neural_backend": TEXT_NEURAL_ADAPTER,
            "pipeline_mode": "text-shape",
            "prompt_text": prompt,
            "adapter_note": (
                "Text-conditioned neural shape inference (mock backend in tests only)."
            ),
        }
        return TextNeuralInferenceResult(
            artifacts=artifacts,
            metadata=metadata,
            pipeline_stages=tracker.to_list(),
        )

    tracker.mark_shape_failed(TEXT_NEURAL_ADAPTER, notes=_NOT_IMPLEMENTED_MESSAGE)
    raise NotImplementedError(_NOT_IMPLEMENTED_MESSAGE)


def to_generation_result(inference: TextNeuralInferenceResult) -> GenerationResult:
    metadata = dict(inference.metadata)
    metadata["pipeline_stages"] = inference.pipeline_stages
    return GenerationResult(
        adapter=TEXT_NEURAL_ADAPTER,
        artifacts=inference.artifacts,
        metadata=metadata,
    )
