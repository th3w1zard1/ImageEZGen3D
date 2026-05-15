from __future__ import annotations

from pathlib import Path
from typing import Any

from PIL import Image

from .adapters import CpuDemoAdapter, HunyuanPlaceholderAdapter
from .adapters.base import GenerationRequest, ModelAdapter
from .config import AppConfig
from .mesh_checks import inspect_artifacts
from .preprocess import save_input_bundle
from .runtime import runtime_status, zero_gpu_runtime_available
from .storage import RunStore


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
        return ["auto", *sorted(self.adapters)]

    def select_adapter(
        self, adapter_name: str | None
    ) -> tuple[str, ModelAdapter, str | None]:
        requested = adapter_name or self.config.app.adapter
        if requested != "auto":
            adapter = self.adapters.get(requested)
            if adapter is None:
                raise ValueError(
                    f"Unknown adapter '{requested}'. Available: {', '.join(self.adapter_choices())}"
                )
            return requested, adapter, None

        status = runtime_status(self.config)
        if self.config.runtime.mode == "cpu" or self.config.runtime.force_cpu:
            fallback_reason = status.reason
        elif self.config.runtime.prefer_zerogpu and zero_gpu_runtime_available(
            self.config
        ):
            zerogpu_adapter = self.adapters.get(self.config.app.zerogpu_adapter)
            if zerogpu_adapter and zerogpu_adapter.capabilities.configured:
                return self.config.app.zerogpu_adapter, zerogpu_adapter, None
            fallback_reason = "ZeroGPU runtime is present, but the configured ZeroGPU model adapter is not enabled yet."
        else:
            fallback_reason = status.reason

        if not self.config.runtime.fallback_to_cpu:
            raise RuntimeError(
                f"ZeroGPU could not be used and CPU fallback is disabled: {fallback_reason}"
            )
        cpu_adapter = self.adapters[self.config.app.cpu_adapter]
        return self.config.app.cpu_adapter, cpu_adapter, fallback_reason

    def generate(
        self,
        primary_image: Image.Image | None,
        view_images: dict[str, Image.Image | None] | None = None,
        adapter_name: str | None = None,
        quality: str | None = None,
        seed: int | None = None,
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
            return payload
        except Exception as exc:
            manifest.stage = "failed"
            manifest.errors.append(str(exc))
            self.store.save_manifest(run_dir, manifest)
            raise
