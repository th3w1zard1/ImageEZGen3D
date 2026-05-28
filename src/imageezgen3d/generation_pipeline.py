from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal

from .export_tiers import DECIMATION_TARGET_BY_QUALITY, resolve_decimation_target

InputModality = Literal["image", "text"]
GenerationLane = Literal["draft", "production"]
StageName = Literal["shape", "texture", "pbr", "export"]
StageStatus = Literal["pending", "running", "succeeded", "skipped", "failed"]

TEXT_STUB_DISCLAIMER = (
    "Text-to-3D preview only — this run uses the text-demo stub adapter and does not "
    "perform neural text-conditioned 3D reconstruction."
)

_STAGE_ORDER: tuple[StageName, ...] = ("shape", "texture", "pbr", "export")


@dataclass(frozen=True)
class GenerationPipelineSpec:
    input_modality: InputModality
    lane: GenerationLane
    prompt_text: str = ""
    quality: str = "draft"
    async_capable: bool = False

    def to_manifest_dict(self) -> dict[str, Any]:
        return {
            "input_modality": self.input_modality,
            "lane": self.lane,
            "prompt_text": self.prompt_text,
            "quality": self.quality,
            "async_capable": self.async_capable,
            "pipeline_stages": initial_pipeline_stages(),
        }


def initial_pipeline_stages() -> list[dict[str, Any]]:
    return [
        {"name": name, "status": "pending", "adapter": None, "notes": ""}
        for name in _STAGE_ORDER
    ]


def resolve_lane_and_quality(
    *,
    lane: str | None,
    quality: str | None,
    default_quality: str = "draft",
) -> tuple[GenerationLane, str]:
    normalized_lane = (lane or "draft").strip().lower()
    if normalized_lane not in ("draft", "production"):
        normalized_lane = "draft"
    lane_value: GenerationLane = (
        "production" if normalized_lane == "production" else "draft"
    )

    explicit_quality = (quality or "").strip().lower()
    if explicit_quality in DECIMATION_TARGET_BY_QUALITY:
        return lane_value, explicit_quality

    if lane_value == "production":
        return lane_value, "balanced"
    return lane_value, default_quality


def build_pipeline_spec(
    *,
    input_modality: str | None,
    lane: str | None,
    quality: str | None,
    prompt_text: str | None,
    default_quality: str = "draft",
) -> GenerationPipelineSpec:
    modality_raw = (input_modality or "image").strip().lower()
    modality: InputModality = "text" if modality_raw == "text" else "image"
    lane_value, quality_value = resolve_lane_and_quality(
        lane=lane,
        quality=quality,
        default_quality=default_quality,
    )
    prompt = (prompt_text or "").strip()
    if modality == "text" and not prompt:
        raise ValueError("Enter a text prompt before generating from text.")
    if modality == "image":
        prompt = prompt  # optional context from brief; stored when non-empty

    return GenerationPipelineSpec(
        input_modality=modality,
        lane=lane_value,
        prompt_text=prompt,
        quality=quality_value,
        async_capable=False,
    )


def decimation_target_for_spec(spec: GenerationPipelineSpec, *, default: int) -> int:
    return resolve_decimation_target(spec.quality, default=default)


@dataclass
class PipelineStageTracker:
    stages: list[dict[str, Any]] = field(default_factory=initial_pipeline_stages)

    def set_stage(
        self,
        name: StageName,
        status: StageStatus,
        *,
        adapter: str | None = None,
        notes: str = "",
    ) -> None:
        for stage in self.stages:
            if stage.get("name") == name:
                stage["status"] = status
                if adapter is not None:
                    stage["adapter"] = adapter
                if notes:
                    stage["notes"] = notes
                return
        raise KeyError(f"Unknown pipeline stage: {name}")

    def mark_shape_running(self, adapter: str) -> None:
        self.set_stage("shape", "running", adapter=adapter)

    def mark_shape_succeeded(self, adapter: str, *, notes: str = "") -> None:
        self.set_stage("shape", "succeeded", adapter=adapter, notes=notes)
        for name in ("texture", "pbr"):
            self.set_stage(
                name,
                "skipped",
                notes="Not executed in this release; reserved for staged adapters.",
            )

    def mark_shape_failed(self, adapter: str, *, notes: str) -> None:
        self.set_stage("shape", "failed", adapter=adapter, notes=notes)

    def mark_export_succeeded(self, *, notes: str = "") -> None:
        self.set_stage("export", "succeeded", notes=notes or "Mesh exports validated.")

    def mark_export_failed(self, *, notes: str) -> None:
        self.set_stage("export", "failed", notes=notes)

    def to_list(self) -> list[dict[str, Any]]:
        return [dict(stage) for stage in self.stages]
