from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Protocol


@dataclass(frozen=True)
class AdapterCapabilities:
    name: str
    cpu_safe: bool
    zerogpu_ready: bool
    configured: bool
    supports_multi_view: bool
    outputs: tuple[str, ...]
    notes: str


@dataclass(frozen=True)
class GenerationRequest:
    run_dir: Path
    processed_image: Path | None
    view_images: dict[str, Path]
    quality: str
    seed: int
    decimation_target: int = 500_000
    input_modality: str = "image"
    lane: str = "draft"
    prompt_text: str = ""
    export_formats: tuple[str, ...] | None = None
    source_mesh_path: Path | None = None
    aspect_ratio: str | None = None
    action_id: str | int | None = None
    creative_lab_flow: str | None = None
    creative_lab_stage: str | None = None


@dataclass
class GenerationResult:
    adapter: str
    artifacts: dict[str, Path] = field(default_factory=dict)
    metadata: dict[str, object] = field(default_factory=dict)


class ModelAdapter(Protocol):
    capabilities: AdapterCapabilities

    def generate(self, request: GenerationRequest) -> GenerationResult:
        raise NotImplementedError
