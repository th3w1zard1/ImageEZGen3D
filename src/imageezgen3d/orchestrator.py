from __future__ import annotations

import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from PIL import Image

from .adapters import CpuDemoAdapter, HunyuanPlaceholderAdapter
from .adapters.base import GenerationRequest, ModelAdapter
from .config import AppConfig
from .mesh_checks import inspect_artifacts
from .preprocess import save_input_bundle
from .runtime import RuntimeStatus, runtime_status
from .storage import RunStore


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
            "hunyuan-zerogpu": HunyuanPlaceholderAdapter(),
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
        self, adapter_name: str | None
    ) -> tuple[str, ModelAdapter, str | None]:
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
    ) -> dict[str, Any]:
        if primary_image is None:
            raise ValueError("Upload a primary image before generating a 3D draft.")

        run_dir, manifest = self.store.create_run()
        adapter_key, adapter, fallback_reason = self.select_adapter(adapter_name)

        manifest.stage = "preprocessing"
        manifest.parameters = {
            "requested_adapter": adapter_name or self.config.app.adapter,
            "selected_adapter": adapter_key,
            "quality": quality or self.config.generation.quality,
            "seed": seed or self.config.generation.seed,
            "runtime": runtime_status(self.config).__dict__,
        }
        if project_brief and project_brief.strip():
            manifest.parameters["project_brief"] = project_brief.strip()
        if starter_flow:
            manifest.parameters["starter_flow"] = starter_flow
            manifest.parameters["starter_flow_label"] = (
                starter_flow_label or starter_flow
            )
        if fallback_reason:
            manifest.parameters["fallback_reason"] = fallback_reason
        self.store.save_manifest(run_dir, manifest)

        try:
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

            saved_views: dict[str, Path] = {}
            for label, image in (view_images or {}).items():
                if image is None:
                    continue
                view_path = self.store.artifact_path(
                    run_dir, "inputs", f"view_{label}.png"
                )
                image.save(view_path)
                saved_views[label] = view_path
                self.store.record_artifact(manifest, f"view_{label}", view_path)

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
            self.store.save_manifest(run_dir, manifest)
            result = adapter.generate(
                GenerationRequest(
                    run_dir=run_dir,
                    processed_image=processed_path,
                    view_images=saved_views,
                    quality=quality or self.config.generation.quality,
                    seed=seed or self.config.generation.seed,
                )
            )

            for key, path in result.artifacts.items():
                self.store.record_artifact(manifest, key, path)
            health = inspect_artifacts(result.artifacts)
            manifest.mesh_report = health.to_dict()
            manifest.stage = "done"
            manifest.parameters.update(result.metadata)
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
            self.store.save_manifest(run_dir, manifest)
            raise
