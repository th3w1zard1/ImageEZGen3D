from __future__ import annotations

import json
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from PIL import Image

from .adapters import CpuDemoAdapter, HunyuanPlaceholderAdapter, TextDemoAdapter, TextNeuralPlaceholderAdapter
from .adapters.base import GenerationRequest, ModelAdapter
from .config import AppConfig
from .delivery_exports import resolve_target_export_formats
from .export_tiers import apply_pbr_stage_from_sidecar
from .generation_pipeline import (
    PipelineStageTracker,
    TEXT_STUB_DISCLAIMER,
    build_pipeline_spec,
    decimation_target_for_spec,
)
from .mesh_checks import inspect_artifacts
from .preprocess import save_input_bundle
from .runtime import RuntimeStatus, runtime_status
from .storage import RunStore

PREVIEW_FALLBACK_DISCLAIMER = (
    "Preview mesh only — this run uses the CPU demo adapter and does not perform "
    "neural 3D reconstruction."
)

TEXT_NEURAL_FALLBACK_REASON = (
    "Neural text-to-3D adapter is not enabled; using text-demo stub."
)


@dataclass(frozen=True)
class AdapterResolution:
    requested: str
    selected: str | None
    runtime: RuntimeStatus
    zerogpu_runnable: bool
    message: str
    fallback_reason: str | None = None


class ImageEZOrchestrator:
    def __init__(self, config: AppConfig) -> None:
        self.config = config
        self.store = RunStore(
            config.app.output_dir, retention_runs=config.storage.retention_runs
        )
        self.adapters: dict[str, ModelAdapter] = {
            "cpu-demo": CpuDemoAdapter(),
            "text-demo": TextDemoAdapter(),
            "text-neural": TextNeuralPlaceholderAdapter(
                configured=config.text_neural.configured
            ),
            "hunyuan-zerogpu": HunyuanPlaceholderAdapter(
                configured=config.hunyuan.configured
            ),
        }

    def adapter_choices(self) -> list[str]:
        configured = [
            name
            for name, adapter in self.adapters.items()
            if adapter.capabilities.configured
        ]
        return ["auto", *sorted(configured)]

    def resolve_adapter(self, adapter_name: str | None) -> AdapterResolution:
        requested = adapter_name or self.config.app.adapter
        status = runtime_status(self.config)
        zerogpu_adapter = self.adapters.get(self.config.app.zerogpu_adapter)
        zerogpu_runnable = bool(
            status.zerogpu_runtime_available
            and zerogpu_adapter is not None
            and zerogpu_adapter.capabilities.configured
        )

        if requested != "auto":
            adapter = self.adapters.get(requested)
            if adapter is None:
                return AdapterResolution(
                    requested=requested,
                    selected=None,
                    runtime=status,
                    zerogpu_runnable=zerogpu_runnable,
                    message=(
                        f"Unknown adapter '{requested}'. Available: {', '.join(self.adapter_choices())}"
                    ),
                )
            if not adapter.capabilities.configured:
                return AdapterResolution(
                    requested=requested,
                    selected=None,
                    runtime=status,
                    zerogpu_runnable=zerogpu_runnable,
                    message=(
                        f"Adapter '{requested}' is not enabled yet. Choose one of: {', '.join(self.adapter_choices())}"
                    ),
                )
            return AdapterResolution(
                requested=requested,
                selected=requested,
                runtime=status,
                zerogpu_runnable=zerogpu_runnable,
                message=f"Using requested backend '{requested}'.",
            )

        if self.config.runtime.mode == "cpu" or self.config.runtime.force_cpu:
            return AdapterResolution(
                requested=requested,
                selected=self.config.app.cpu_adapter,
                runtime=status,
                zerogpu_runnable=zerogpu_runnable,
                message=status.reason,
                fallback_reason=status.reason,
            )

        if self.config.runtime.prefer_zerogpu and status.zerogpu_runtime_available:
            if zerogpu_runnable:
                return AdapterResolution(
                    requested=requested,
                    selected=self.config.app.zerogpu_adapter,
                    runtime=status,
                    zerogpu_runnable=True,
                    message=status.reason,
                )
            fallback_reason = "ZeroGPU runtime is present, but the configured ZeroGPU model adapter is not enabled yet."
            if self.config.runtime.fallback_to_cpu:
                return AdapterResolution(
                    requested=requested,
                    selected=self.config.app.cpu_adapter,
                    runtime=status,
                    zerogpu_runnable=False,
                    message=fallback_reason,
                    fallback_reason=fallback_reason,
                )
            return AdapterResolution(
                requested=requested,
                selected=None,
                runtime=status,
                zerogpu_runnable=False,
                message=(
                    f"ZeroGPU could not be used and CPU fallback is disabled: {fallback_reason}"
                ),
            )

        if self.config.runtime.fallback_to_cpu:
            return AdapterResolution(
                requested=requested,
                selected=self.config.app.cpu_adapter,
                runtime=status,
                zerogpu_runnable=zerogpu_runnable,
                message=status.reason,
                fallback_reason=status.reason,
            )

        return AdapterResolution(
            requested=requested,
            selected=None,
            runtime=status,
            zerogpu_runnable=zerogpu_runnable,
            message=(
                f"ZeroGPU could not be used and CPU fallback is disabled: {status.reason}"
            ),
        )

    def select_adapter(
        self, adapter_name: str | None, *, input_modality: str = "image"
    ) -> tuple[str, ModelAdapter, str | None]:
        if input_modality == "text":
            requested = (adapter_name or "auto").strip().lower()
            neural = self.adapters.get("text-neural")
            stub = self.adapters.get("text-demo")
            if stub is None or not stub.capabilities.configured:
                raise ValueError(
                    "Text-to-3D is not available. The text-demo adapter is not configured."
                )

            if requested == "text-neural":
                if neural is None or not neural.capabilities.configured:
                    raise ValueError(
                        "Adapter 'text-neural' is not enabled yet. "
                        f"Choose one of: {', '.join(self.adapter_choices())}"
                    )
                return "text-neural", neural, None

            if requested == "text-demo":
                return "text-demo", stub, None

            if requested not in ("auto", "", "none"):
                raise ValueError(
                    f"Adapter '{adapter_name}' does not support text-to-3D. "
                    "Use auto, text-demo, or text-neural."
                )

            if neural is not None and neural.capabilities.configured:
                return "text-neural", neural, None
            return "text-demo", stub, TEXT_NEURAL_FALLBACK_REASON

        resolution = self.resolve_adapter(adapter_name)
        if resolution.selected is None:
            if resolution.requested != "auto":
                raise ValueError(resolution.message)
            raise RuntimeError(resolution.message)

        adapter = self.adapters[resolution.selected]
        return resolution.selected, adapter, resolution.fallback_reason

    def generate(
        self,
        primary_image: Image.Image | None,
        view_images: dict[str, Image.Image | None] | None = None,
        adapter_name: str | None = None,
        quality: str | None = None,
        seed: int | None = None,
        project_brief: str | None = None,
        starter_flow: str | None = None,
        starter_flow_label: str | None = None,
        reference_brief: str | Path | None = None,
        *,
        input_modality: str | None = None,
        prompt_text: str | None = None,
        lane: str | None = None,
        target_formats: tuple[str, ...] | list[str] | None = None,
    ) -> dict[str, Any]:
        pipeline_spec = build_pipeline_spec(
            input_modality=input_modality,
            lane=lane,
            quality=quality,
            prompt_text=prompt_text or project_brief,
            default_quality=self.config.generation.quality,
        )
        if pipeline_spec.input_modality == "image" and primary_image is None:
            raise ValueError("Upload a primary image before generating a 3D draft.")

        run_dir, manifest = self.store.create_run()
        adapter_key, adapter, fallback_reason = self.select_adapter(
            adapter_name,
            input_modality=pipeline_spec.input_modality,
        )

        quality_value = pipeline_spec.quality
        decimation_target = decimation_target_for_spec(
            pipeline_spec,
            default=self.config.generation.decimation_target,
        )
        export_formats = resolve_target_export_formats(
            target_formats,
            self.config.exports.formats,
        )
        stage_tracker = PipelineStageTracker()
        manifest.stage = "preprocessing"
        manifest.parameters = {
            "requested_adapter": adapter_name or self.config.app.adapter,
            "selected_adapter": adapter_key,
            "quality": quality_value,
            "lane": pipeline_spec.lane,
            "input_modality": pipeline_spec.input_modality,
            "decimation_target": decimation_target,
            "seed": seed or self.config.generation.seed,
            "runtime": runtime_status(self.config).__dict__,
            "generation": pipeline_spec.to_manifest_dict(),
            "export_formats": list(export_formats),
        }
        if target_formats:
            manifest.parameters["target_formats"] = [
                str(fmt).strip().lower()
                for fmt in target_formats
                if str(fmt).strip()
            ]
        manifest.parameters["generation"]["pipeline_stages"] = (
            stage_tracker.to_list()
        )
        if pipeline_spec.prompt_text:
            manifest.parameters["prompt_text"] = pipeline_spec.prompt_text
        if project_brief and project_brief.strip():
            manifest.parameters["project_brief"] = project_brief.strip()
        if starter_flow:
            manifest.parameters["starter_flow"] = starter_flow
            manifest.parameters["starter_flow_label"] = (
                starter_flow_label or starter_flow
            )
        if fallback_reason:
            manifest.parameters["fallback_reason"] = fallback_reason
        if fallback_reason and adapter_key == self.config.app.cpu_adapter:
            manifest.parameters["preview_disclaimer"] = PREVIEW_FALLBACK_DISCLAIMER
        if adapter_key == "text-demo":
            manifest.parameters["preview_disclaimer"] = TEXT_STUB_DISCLAIMER
            if fallback_reason:
                manifest.parameters["fallback_reason"] = fallback_reason
        self.store.save_manifest(run_dir, manifest)

        try:
            processed_path: Path | None = None
            saved_views: dict[str, Path] = {}

            if pipeline_spec.input_modality == "image":
                assert primary_image is not None
                input_path = self.store.artifact_path(run_dir, "inputs", "primary.png")
                processed_path = self.store.artifact_path(
                    run_dir, "processed", "primary_normalized.png"
                )
                report_path = self.store.artifact_path(
                    run_dir, "reports", "input_validation.json"
                )
                report = save_input_bundle(
                    primary_image,
                    input_path,
                    processed_path,
                    report_path,
                    target_size=self.config.preprocessing.target_size,
                    minimum_short_side=self.config.preprocessing.minimum_short_side,
                    maximum_long_side=self.config.preprocessing.maximum_long_side,
                    blur_edge_variance_threshold=self.config.preprocessing.blur_edge_variance_threshold,
                    low_contrast_threshold=self.config.preprocessing.low_contrast_threshold,
                )
                manifest.validation = report.to_dict()
                self.store.record_artifact(manifest, "original", input_path)
                self.store.record_artifact(manifest, "processed", processed_path)
                self.store.record_artifact(manifest, "validation", report_path)

                for label, image in (view_images or {}).items():
                    if image is None:
                        continue
                    view_path = self.store.artifact_path(
                        run_dir, "inputs", f"view_{label}.png"
                    )
                    image.save(view_path)
                    saved_views[label] = view_path
                    self.store.record_artifact(manifest, f"view_{label}", view_path)
            else:
                prompt_path = self.store.artifact_path(run_dir, "inputs", "prompt.txt")
                prompt_path.write_text(pipeline_spec.prompt_text + "\n", encoding="utf-8")
                self.store.record_artifact(manifest, "prompt", prompt_path)
                manifest.validation = {
                    "input_modality": "text",
                    "prompt_length": len(pipeline_spec.prompt_text),
                    "score": 100,
                    "messages": [],
                }

            if reference_brief:
                source_brief = Path(reference_brief)
                if source_brief.exists() and source_brief.is_file():
                    suffix = source_brief.suffix or ".txt"
                    brief_path = self.store.artifact_path(
                        run_dir, "inputs", f"reference_brief{suffix}"
                    )
                    shutil.copyfile(source_brief, brief_path)
                    self.store.record_artifact(manifest, "reference_brief", brief_path)
                    manifest.parameters["reference_brief_name"] = source_brief.name

            manifest.stage = "generating"
            stage_tracker.mark_shape_running(adapter_key)
            manifest.parameters["generation"]["pipeline_stages"] = (
                stage_tracker.to_list()
            )
            self.store.save_manifest(run_dir, manifest)
            result = adapter.generate(
                GenerationRequest(
                    run_dir=run_dir,
                    processed_image=processed_path,
                    view_images=saved_views,
                    quality=quality_value,
                    seed=seed or self.config.generation.seed,
                    decimation_target=decimation_target,
                    input_modality=pipeline_spec.input_modality,
                    lane=pipeline_spec.lane,
                    prompt_text=pipeline_spec.prompt_text,
                    export_formats=export_formats,
                )
            )

            reported_stages = result.metadata.get("pipeline_stages")
            if isinstance(reported_stages, list) and reported_stages:
                stage_tracker.apply_stage_snapshot(reported_stages)
            else:
                stage_tracker.mark_shape_succeeded(
                    adapter_key,
                    notes=str(result.metadata.get("adapter_note", "")),
                )
            for key, path in result.artifacts.items():
                self.store.record_artifact(manifest, key, path)
            health = inspect_artifacts(result.artifacts)
            manifest.mesh_report = health.to_dict()
            sidecar_path = result.artifacts.get("export_sidecar")
            if sidecar_path is not None and Path(sidecar_path).is_file():
                sidecar_payload = json.loads(
                    Path(sidecar_path).read_text(encoding="utf-8")
                )
                apply_pbr_stage_from_sidecar(
                    stage_tracker,
                    sidecar_payload,
                    adapter=result.adapter,
                )
            else:
                stage_tracker.set_stage(
                    "pbr",
                    "skipped",
                    notes="Export sidecar missing; PBR delivery unknown.",
                )
            if health.status == "ok":
                stage_tracker.mark_export_succeeded()
            else:
                stage_tracker.mark_export_failed(notes="Mesh validation reported issues.")
            manifest.stage = "done"
            manifest.parameters.update(result.metadata)
            manifest.parameters["generation"]["pipeline_stages"] = (
                stage_tracker.to_list()
            )
            manifest.parameters["generation"]["quality"] = quality_value
            manifest.parameters["generation"]["lane"] = pipeline_spec.lane
            manifest_path = self.store.save_manifest(run_dir, manifest)
            self.store.record_artifact(manifest, "manifest", manifest_path)
            self.store.save_manifest(run_dir, manifest)
            payload = manifest.to_dict()
            payload["adapter"] = result.adapter
            payload["artifacts"] = {
                key: self.store.artifact_value(path)
                for key, path in payload["artifacts"].items()
                if self.store.artifact_value(path) is not None
            }
            return payload
        except Exception as exc:
            manifest.stage = "failed"
            manifest.errors.append(str(exc))
            if "generation" in manifest.parameters:
                tracker = PipelineStageTracker(
                    stages=manifest.parameters["generation"].get(
                        "pipeline_stages", []
                    )
                )
                tracker.mark_shape_failed(
                    manifest.parameters.get("selected_adapter", "unknown"),
                    notes=str(exc),
                )
                manifest.parameters["generation"]["pipeline_stages"] = (
                    tracker.to_list()
                )
            self.store.save_manifest(run_dir, manifest)
            raise
