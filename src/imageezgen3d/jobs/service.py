from __future__ import annotations

import json
import time
from concurrent.futures import Future, ThreadPoolExecutor
from pathlib import Path
from typing import Any

from PIL import Image

from ..config import AppConfig, load_config
from ..delivery_exports import resolve_target_export_formats
from ..orchestrator import ImageEZOrchestrator
from ..storage import atomic_write_json
from .models import JobPollResponse, JobRequest, JobRecord, JobStatus
from .store import JobStore
from .webhooks import deliver_webhook


class JobService:
    """In-process async job queue with poll surface for automation clients."""

    def __init__(
        self,
        config: AppConfig | None = None,
        *,
        max_workers: int = 1,
    ) -> None:
        self.config = config or load_config()
        self.orchestrator = ImageEZOrchestrator(self.config)
        self.run_store = self.orchestrator.store
        jobs_root = self.config.app.output_dir / "jobs"
        self.job_store = JobStore(jobs_root)
        self._executor = ThreadPoolExecutor(max_workers=max(1, max_workers))
        self._futures: dict[str, Future[None]] = {}

    def submit(self, request: JobRequest) -> str:
        resolve_target_export_formats(
            request.target_formats,
            self.config.exports.formats,
        )
        modality = (request.input_modality or "image").strip().lower()
        if modality == "retexture":
            if not request.texture_image_path and not request.image_path:
                raise ValueError(
                    "Retexture jobs require texture_image_path or image_path."
                )
            if request.source_mesh_path:
                mesh_path = Path(request.source_mesh_path)
                if not mesh_path.is_file():
                    raise FileNotFoundError(f"Source mesh not found: {mesh_path}")
        elif modality == "text-to-image":
            if not (request.prompt_text or request.project_brief):
                raise ValueError("text-to-image jobs require prompt_text.")
        elif modality == "image-to-image":
            if not request.image_path:
                raise ValueError("image-to-image jobs require image_path.")
        elif modality in ("rig", "animate"):
            if request.source_mesh_path:
                mesh_path = Path(request.source_mesh_path)
                if not mesh_path.is_file():
                    raise FileNotFoundError(f"Source mesh not found: {mesh_path}")
        elif modality == "creative-lab":
            if request.image_path:
                image_path = Path(request.image_path)
                if not image_path.is_file():
                    raise FileNotFoundError(f"Image not found: {image_path}")
        record = self.job_store.create(request=request.to_dict())
        future = self._executor.submit(self._execute_job, record.job_id)
        self._futures[record.job_id] = future
        return record.job_id

    def poll(self, job_id: str, *, poll_url_template: str | None = None) -> JobPollResponse:
        record = self.job_store.load(job_id)
        poll_url = None
        if poll_url_template:
            poll_url = poll_url_template.format(job_id=job_id)
        return JobPollResponse(
            job_id=record.job_id,
            status=record.status,
            run_id=record.run_id,
            error=record.error,
            poll_url=poll_url,
            result_ready=record.status == "succeeded",
        )

    def get_result(self, job_id: str) -> dict[str, Any]:
        record = self.job_store.load(job_id)
        if record.status != "succeeded" or not record.run_id:
            raise RuntimeError(
                f"Job {job_id} is not ready (status={record.status!r})."
            )
        return self.run_store.read_manifest(record.run_id)

    def get_generation_payload(self, job_id: str) -> dict[str, Any]:
        """Return orchestrator-shaped payload for UI clients after job success."""
        manifest = self.get_result(job_id)
        parameters = manifest.get("parameters", {})
        if not isinstance(parameters, dict):
            parameters = {}
        artifacts = manifest.get("artifacts", {})
        if not isinstance(artifacts, dict):
            artifacts = {}
        payload = dict(manifest)
        payload["adapter"] = str(
            parameters.get("selected_adapter")
            or parameters.get("requested_adapter")
            or "unknown"
        )
        payload["artifacts"] = {
            key: self.run_store.artifact_value(path)
            for key, path in artifacts.items()
            if self.run_store.artifact_value(path) is not None
        }
        return payload

    def wait_for(
        self,
        job_id: str,
        *,
        timeout_seconds: float = 120.0,
        poll_interval_seconds: float = 0.05,
    ) -> JobPollResponse:
        deadline = time.monotonic() + timeout_seconds
        while time.monotonic() < deadline:
            response = self.poll(job_id)
            if response.status in ("succeeded", "failed"):
                return response
            time.sleep(poll_interval_seconds)
        raise TimeoutError(f"Job {job_id} did not finish within {timeout_seconds}s")

    def shutdown(self, *, wait: bool = True) -> None:
        self._executor.shutdown(wait=wait, cancel_futures=not wait)

    def _execute_job(self, job_id: str) -> None:
        record = self.job_store.load(job_id)
        request = JobRequest.from_dict(record.request)
        self.job_store.update_status(job_id, "running")
        try:
            result = self._run_generation(request)
            run_id = str(result.get("run_id") or "")
            self._mark_run_async_capable(run_id, job_id)
            webhook_delivered, webhook_error = self._deliver_webhook(
                record,
                status="succeeded",
                run_id=run_id or None,
                error=None,
                result=result,
            )
            self.job_store.update_status(
                job_id,
                "succeeded",
                run_id=run_id or None,
                webhook_delivered=webhook_delivered,
                webhook_error=webhook_error,
            )
        except Exception as exc:
            webhook_delivered, webhook_error = self._deliver_webhook(
                record,
                status="failed",
                run_id=None,
                error=str(exc),
                result={"job_id": job_id, "error": str(exc)},
            )
            self.job_store.update_status(
                job_id,
                "failed",
                error=str(exc),
                webhook_delivered=webhook_delivered,
                webhook_error=webhook_error,
            )

    def _run_generation(self, request: JobRequest) -> dict[str, Any]:
        modality = (request.input_modality or "image").strip().lower()
        primary_image: Image.Image | None = None
        source_mesh_path: Path | None = None
        prompt_text = request.prompt_text or request.project_brief
        if modality == "image":
            if not request.image_path:
                raise ValueError("image_path is required for image modality jobs.")
            image_path = Path(request.image_path)
            if not image_path.is_file():
                raise FileNotFoundError(f"Image not found: {image_path}")
            primary_image = Image.open(image_path)
        elif modality == "retexture":
            texture_path_str = request.texture_image_path or request.image_path
            if not texture_path_str:
                raise ValueError(
                    "texture_image_path or image_path is required for retexture jobs."
                )
            texture_path = Path(texture_path_str)
            if not texture_path.is_file():
                raise FileNotFoundError(f"Texture image not found: {texture_path}")
            primary_image = Image.open(texture_path)
            if request.source_mesh_path:
                source_mesh_path = Path(request.source_mesh_path)
                if not source_mesh_path.is_file():
                    raise FileNotFoundError(
                        f"Source mesh not found: {source_mesh_path}"
                    )
        elif modality == "image-to-image":
            if not request.image_path:
                raise ValueError("image_path is required for image-to-image jobs.")
            image_path = Path(request.image_path)
            if not image_path.is_file():
                raise FileNotFoundError(f"Image not found: {image_path}")
            primary_image = Image.open(image_path)
        elif modality == "creative-lab":
            if request.image_path:
                image_path = Path(request.image_path)
                if not image_path.is_file():
                    raise FileNotFoundError(f"Image not found: {image_path}")
                primary_image = Image.open(image_path)
        elif modality in ("rig", "animate"):
            if request.source_mesh_path:
                source_mesh_path = Path(request.source_mesh_path)
                if not source_mesh_path.is_file():
                    raise FileNotFoundError(
                        f"Source mesh not found: {source_mesh_path}"
                    )
        elif modality == "text-to-image":
            if not prompt_text:
                raise ValueError("prompt_text is required for text-to-image jobs.")
        view_images: dict[str, Image.Image] = {}
        if request.view_image_paths:
            for label, path_str in request.view_image_paths.items():
                view_path = Path(path_str)
                if view_path.is_file():
                    view_images[label] = Image.open(view_path)
        return self.orchestrator.generate(
            primary_image,
            view_images=view_images or None,
            adapter_name=request.adapter_name,
            quality=request.quality,
            seed=request.seed,
            project_brief=request.project_brief,
            starter_flow=request.starter_flow,
            starter_flow_label=request.starter_flow_label,
            reference_brief=request.reference_brief,
            input_modality=modality,
            prompt_text=prompt_text,
            lane=request.lane,
            target_formats=request.target_formats,
            source_mesh_path=source_mesh_path,
            aspect_ratio=request.aspect_ratio,
            action_id=request.action_id,
            creative_lab_flow=request.creative_lab_flow,
            creative_lab_stage=request.creative_lab_stage,
        )

    def _mark_run_async_capable(self, run_id: str, job_id: str) -> None:
        if not run_id:
            return
        manifest_path = self.run_store.root / run_id / "manifest.json"
        if not manifest_path.exists():
            return
        payload = json.loads(manifest_path.read_text(encoding="utf-8"))
        parameters = payload.setdefault("parameters", {})
        generation = parameters.setdefault("generation", {})
        generation["async_capable"] = True
        parameters["job_id"] = job_id
        atomic_write_json(manifest_path, payload)

    def _deliver_webhook(
        self,
        record: JobRecord,
        *,
        status: JobStatus,
        run_id: str | None,
        error: str | None,
        result: dict[str, Any],
    ) -> tuple[bool | None, str | None]:
        if not record.webhook_url:
            return None, None
        body = {
            "job_id": record.job_id,
            "status": status,
            "run_id": run_id,
            "error": error,
            "result": result if status == "succeeded" else None,
        }
        delivered, webhook_error = deliver_webhook(record.webhook_url, body)
        return delivered, webhook_error
