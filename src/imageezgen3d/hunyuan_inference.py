from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Protocol

from .adapters.base import GenerationRequest, GenerationResult
from .export_tiers import build_export_sidecar
from .exporters import SimpleMesh, export_all, mesh_topology
from .generation_pipeline import PipelineStageTracker
from .mesh_decimation import decimate_mesh

HUNYUAN_ADAPTER = "hunyuan-zerogpu"
_NOT_IMPLEMENTED_MESSAGE = (
    "Hunyuan GPU inference is not wired yet. Complete weight cache, tier-C "
    "dependencies, and hosted E2E (G7) before enablement."
)


@dataclass(frozen=True)
class HunyuanMeshResult:
    mesh: SimpleMesh
    raw_mesh: SimpleMesh | None = None


class HunyuanInferenceBackend(Protocol):
    def run_shape_texture(
        self,
        request: GenerationRequest,
        *,
        tracker: PipelineStageTracker,
    ) -> HunyuanMeshResult: ...


@dataclass
class HunyuanInferenceResult:
    artifacts: dict[str, Path]
    metadata: dict[str, Any] = field(default_factory=dict)
    pipeline_stages: list[dict[str, Any]] = field(default_factory=list)


def finalize_hunyuan_exports(
    mesh: SimpleMesh,
    request: GenerationRequest,
    *,
    raw_mesh: SimpleMesh | None = None,
) -> tuple[dict[str, Path], dict[str, Any]]:
    """Decimate and export Hunyuan mesh artifacts matching the G6 sidecar contract."""
    export_mesh, decimation_meta = decimate_mesh(mesh, request.decimation_target)
    vertex_count, face_count = mesh_topology(export_mesh)
    sidecar = build_export_sidecar(
        quality=request.quality,
        decimation_target=request.decimation_target,
        vertex_count=vertex_count,
        face_count=face_count,
        adapter=HUNYUAN_ADAPTER,
        decimation=decimation_meta,
        raw_exported=raw_mesh is not None,
    )
    paths = export_all(
        export_mesh,
        request.run_dir / "exports",
        stem="hunyuan_mesh",
        export_sidecar=sidecar,
        raw_mesh=raw_mesh,
    )
    metadata = {
        "neural_backend": HUNYUAN_ADAPTER,
        "pipeline_mode": "shape+texture",
        "quality": request.quality,
        "decimation_target": request.decimation_target,
        "face_count": face_count,
        "vertex_count": vertex_count,
        "decimation_applied": decimation_meta.get("decimation_applied", False),
        "raw_exported": raw_mesh is not None,
    }
    return paths, metadata


def run_hunyuan_shape_texture(
    request: GenerationRequest,
    *,
    backend: HunyuanInferenceBackend | None = None,
) -> HunyuanInferenceResult:
    """Shape then texture towers for Hunyuan3D (two-stage neural path)."""
    tracker = PipelineStageTracker()
    tracker.mark_shape_running(HUNYUAN_ADAPTER)
    if backend is not None:
        mesh_result = backend.run_shape_texture(request, tracker=tracker)
        artifacts, export_metadata = finalize_hunyuan_exports(
            mesh_result.mesh,
            request,
            raw_mesh=mesh_result.raw_mesh,
        )
        metadata = {
            **export_metadata,
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
