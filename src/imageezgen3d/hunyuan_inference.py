from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Protocol

from .adapters.base import GenerationRequest, GenerationResult
from .export_tiers import build_export_sidecar
from .exporters import SimpleMesh, export_all, mesh_topology
from .config import load_config
from .generation_pipeline import PipelineStageTracker
from .generation_pipeline import lane_exports_reference_pbr_maps
from .mesh_decimation import decimate_mesh
from .pbr_map_exports import (
    REFERENCE_PBR_NOTES,
    pbr_manifest_artifacts,
    resolve_base_color_image,
    write_reference_pbr_maps,
)

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
    export_dir = request.run_dir / "exports"
    pbr_written: dict[str, Path] = {}
    pbr_sidecar_paths: dict[str, str] | None = None
    pbr_available = False
    if lane_exports_reference_pbr_maps(request.lane):
        base_color_image = resolve_base_color_image(
            export_mesh.color,
            b64_image=export_mesh.b64_image,
        )
        pbr_written, pbr_sidecar_paths = write_reference_pbr_maps(
            export_dir,
            base_color_image=base_color_image,
        )
        pbr_available = True
    sidecar = build_export_sidecar(
        quality=request.quality,
        decimation_target=request.decimation_target,
        vertex_count=vertex_count,
        face_count=face_count,
        adapter=HUNYUAN_ADAPTER,
        decimation=decimation_meta,
        raw_exported=raw_mesh is not None,
        pbr_available=pbr_available,
        pbr_map_paths=pbr_sidecar_paths,
        pbr_notes=REFERENCE_PBR_NOTES if pbr_available else None,
    )
    paths = export_all(
        export_mesh,
        export_dir,
        stem="hunyuan_mesh",
        export_sidecar=sidecar,
        raw_mesh=raw_mesh,
        formats=request.export_formats or load_config().exports.formats,
    )
    paths.update(pbr_manifest_artifacts(pbr_written))
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


def resolve_default_hunyuan_backend(
    backend: HunyuanInferenceBackend | None,
) -> HunyuanInferenceBackend | None:
    if backend is not None:
        return backend
    from .hunyuan_backend import resolve_hunyuan_backend_from_config

    config = load_config()
    return resolve_hunyuan_backend_from_config(config.hunyuan)


def run_hunyuan_shape_texture(
    request: GenerationRequest,
    *,
    backend: HunyuanInferenceBackend | None = None,
) -> HunyuanInferenceResult:
    """Shape then texture towers for Hunyuan3D (two-stage neural path)."""
    from .hunyuan_backend import (
        DevPreviewHunyuanBackend,
        WeightVerifiedHunyuanBackend,
        adapter_note_for_backend,
    )

    tracker = PipelineStageTracker()
    tracker.mark_shape_running(HUNYUAN_ADAPTER)
    resolved_backend = resolve_default_hunyuan_backend(backend)
    if resolved_backend is not None:
        mesh_result = resolved_backend.run_shape_texture(request, tracker=tracker)
        artifacts, export_metadata = finalize_hunyuan_exports(
            mesh_result.mesh,
            request,
            raw_mesh=mesh_result.raw_mesh,
        )
        config = load_config()
        adapter_note = adapter_note_for_backend(
            resolved_backend,
            settings=config.hunyuan,
        )
        metadata = {
            **export_metadata,
            "adapter_note": adapter_note,
        }
        if isinstance(resolved_backend, DevPreviewHunyuanBackend):
            metadata["dev_preview"] = True
            metadata["preview_disclaimer"] = adapter_note
        if isinstance(resolved_backend, WeightVerifiedHunyuanBackend):
            metadata["weight_backend"] = True
            from .hunyuan_inference_runner import resolve_hunyuan_inference_runner

            runner = resolve_hunyuan_inference_runner(config.hunyuan)
            if config.hunyuan.gpu_forward and runner is not None:
                metadata["neural_forward"] = True
            else:
                metadata["tier_c_shell"] = True
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
