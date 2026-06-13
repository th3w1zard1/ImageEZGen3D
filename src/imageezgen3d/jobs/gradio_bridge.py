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


def build_retexture_job_request(
    *,
    intake_root: Path,
    source_mesh_path: str,
    texture_image: Image.Image | None,
    prompt_text: str | None = None,
    project_brief: str | None = None,
) -> JobRequest:
    intake_dir = intake_root / uuid.uuid4().hex
    texture_path, _ = stage_gradio_images(intake_dir, texture_image, None)
    if not texture_path:
        raise ValueError(
            "Upload a texture reference image before running Edit Texture."
        )
    return JobRequest(
        input_modality="retexture",
        source_mesh_path=source_mesh_path,
        texture_image_path=texture_path,
        prompt_text=(prompt_text or project_brief or "").strip() or None,
        adapter_name="retexture-demo",
        quality="draft",
        lane="draft",
    )


def build_mesh_op_job_request(
    modality: str,
    mesh_input_path: str,
    *,
    second_mesh_path: str | None = None,
    target_polycount: int | None = None,
) -> JobRequest:
    normalized = modality.strip().lower()
    polycount = target_polycount
    if polycount is None and normalized == "remesh":
        polycount = 30_000
    return JobRequest(
        input_modality=normalized,
        mesh_input_path=mesh_input_path,
        second_mesh_path=second_mesh_path,
        target_polycount=polycount,
    )


def build_animate_job_request(
    source_mesh_path: str,
    *,
    action_id: str = "Walking_man",
) -> JobRequest:
    return JobRequest(
        input_modality="animate",
        source_mesh_path=source_mesh_path,
        action_id=action_id,
        adapter_name="animation-demo",
        quality="draft",
        lane="draft",
        task_type="animations",
    )


def capture_retry_snapshot(
    *,
    starter_flow: str | None,
    project_brief_text: str | None,
    reference_brief_file: str | None,
    adapter_name: str | None,
    quality_name: str | None,
    seed_value: int | None,
    input_modality_name: str | None,
    text_prompt_value: str | None,
    generation_lane_name: str | None,
    queue_as_job_enabled: bool,
) -> dict[str, Any]:
    return {
        "starter_flow": starter_flow,
        "project_brief_text": project_brief_text,
        "reference_brief_file": reference_brief_file,
        "adapter_name": adapter_name,
        "quality_name": quality_name,
        "seed_value": int(seed_value or 0),
        "input_modality_name": input_modality_name,
        "text_prompt_value": text_prompt_value,
        "generation_lane_name": generation_lane_name,
        "queue_as_job_enabled": bool(queue_as_job_enabled),
    }


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
