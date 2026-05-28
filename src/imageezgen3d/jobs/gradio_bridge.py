from __future__ import annotations

import uuid
from pathlib import Path
from typing import Any

from PIL import Image

from .models import JobRequest
from .service import JobService


def stage_gradio_images(
    intake_dir: Path,
    primary_image: Image.Image | None,
    view_images: dict[str, Image.Image | None] | None,
) -> tuple[str | None, dict[str, str]]:
    intake_dir.mkdir(parents=True, exist_ok=True)
    primary_path: str | None = None
    if primary_image is not None:
        path = intake_dir / "primary.png"
        primary_image.save(path)
        primary_path = str(path)
    staged_views: dict[str, str] = {}
    for label, image in (view_images or {}).items():
        if image is None:
            continue
        path = intake_dir / f"view_{label}.png"
        image.save(path)
        staged_views[label] = str(path)
    return primary_path, staged_views


def build_job_request_from_gradio(
    *,
    intake_root: Path,
    primary_image: Image.Image | None,
    view_images: dict[str, Image.Image | None] | None,
    adapter_name: str | None,
    quality_name: str | None,
    seed_value: int | None,
    project_brief_text: str | None,
    starter_flow: str | None,
    starter_flow_label: str | None,
    reference_brief_file: str | None,
    input_modality_name: str | None,
    text_prompt_value: str | None,
    generation_lane_name: str | None,
) -> JobRequest:
    intake_dir = intake_root / uuid.uuid4().hex
    image_path, view_paths = stage_gradio_images(
        intake_dir,
        primary_image,
        view_images,
    )
    return JobRequest(
        input_modality=str(input_modality_name or "image"),
        prompt_text=text_prompt_value,
        image_path=image_path,
        adapter_name=adapter_name,
        quality=quality_name,
        lane=generation_lane_name,
        seed=seed_value,
        project_brief=project_brief_text,
        starter_flow=starter_flow,
        starter_flow_label=starter_flow_label,
        reference_brief=reference_brief_file,
        view_image_paths=view_paths or None,
    )


def run_via_job_queue(
    service: JobService,
    request: JobRequest,
    *,
    timeout_seconds: float = 300.0,
) -> dict[str, Any]:
    job_id = service.submit(request)
    poll = service.wait_for(job_id, timeout_seconds=timeout_seconds)
    if poll.status != "succeeded":
        raise RuntimeError(poll.error or f"Background job {job_id} failed.")
    return service.get_generation_payload(job_id)
