from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal

JobStatus = Literal["queued", "running", "succeeded", "failed"]


@dataclass(frozen=True)
class JobRequest:
    """Automation-facing generation request (image path or text prompt)."""

    input_modality: str = "image"
    prompt_text: str | None = None
    image_path: str | None = None
    texture_image_path: str | None = None
    source_mesh_path: str | None = None
    aspect_ratio: str | None = None
    action_id: str | int | None = None
    creative_lab_flow: str | None = None
    creative_lab_stage: str | None = None
    task_type: str | None = None
    topology: str | None = None
    target_polycount: int | None = None
    enable_pbr: bool | None = None
    texture_prompt: str | None = None
    mesh_input_path: str | None = None
    mesh_output_path: str | None = None
    resize_height: float | None = None
    resize_longest_side: float | None = None
    auto_size: bool | None = None
    origin_at: str | None = None
    adapter_name: str | None = None
    quality: str | None = None
    lane: str | None = None
    seed: int | None = None
    project_brief: str | None = None
    starter_flow: str | None = None
    starter_flow_label: str | None = None
    reference_brief: str | None = None
    view_image_paths: dict[str, str] | None = None
    webhook_url: str | None = None
    target_formats: tuple[str, ...] | None = None

    def to_dict(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "input_modality": self.input_modality,
            "prompt_text": self.prompt_text,
            "image_path": self.image_path,
            "texture_image_path": self.texture_image_path,
            "source_mesh_path": self.source_mesh_path,
            "adapter_name": self.adapter_name,
            "quality": self.quality,
            "lane": self.lane,
            "seed": self.seed,
            "project_brief": self.project_brief,
            "starter_flow": self.starter_flow,
            "starter_flow_label": self.starter_flow_label,
            "reference_brief": self.reference_brief,
            "webhook_url": self.webhook_url,
        }
        if self.view_image_paths:
            payload["view_image_paths"] = dict(self.view_image_paths)
        if self.target_formats:
            payload["target_formats"] = list(self.target_formats)
        for key in (
            "aspect_ratio",
            "action_id",
            "creative_lab_flow",
            "creative_lab_stage",
            "task_type",
            "topology",
            "target_polycount",
            "texture_prompt",
            "mesh_input_path",
            "mesh_output_path",
            "origin_at",
        ):
            value = getattr(self, key)
            if value is not None:
                payload[key] = value
        if self.enable_pbr is not None:
            payload["enable_pbr"] = self.enable_pbr
        if self.resize_height is not None:
            payload["resize_height"] = self.resize_height
        if self.resize_longest_side is not None:
            payload["resize_longest_side"] = self.resize_longest_side
        if self.auto_size is not None:
            payload["auto_size"] = self.auto_size
        return payload

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> JobRequest:
        return cls(
            input_modality=str(payload.get("input_modality") or "image"),
            prompt_text=_optional_str(payload.get("prompt_text")),
            image_path=_optional_str(payload.get("image_path")),
            texture_image_path=_optional_str(payload.get("texture_image_path")),
            source_mesh_path=_optional_str(payload.get("source_mesh_path")),
            aspect_ratio=_optional_str(payload.get("aspect_ratio")),
            action_id=payload.get("action_id"),
            creative_lab_flow=_optional_str(payload.get("creative_lab_flow")),
            creative_lab_stage=_optional_str(payload.get("creative_lab_stage")),
            task_type=_optional_str(payload.get("task_type")),
            topology=_optional_str(payload.get("topology")),
            target_polycount=_optional_int(payload.get("target_polycount")),
            enable_pbr=_optional_bool(payload.get("enable_pbr")),
            texture_prompt=_optional_str(payload.get("texture_prompt")),
            mesh_input_path=_optional_str(payload.get("mesh_input_path")),
            mesh_output_path=_optional_str(payload.get("mesh_output_path")),
            resize_height=_optional_float(payload.get("resize_height")),
            resize_longest_side=_optional_float(payload.get("resize_longest_side")),
            auto_size=_optional_bool(payload.get("auto_size")),
            origin_at=_optional_str(payload.get("origin_at")),
            adapter_name=_optional_str(payload.get("adapter_name")),
            quality=_optional_str(payload.get("quality")),
            lane=_optional_str(payload.get("lane")),
            seed=_optional_int(payload.get("seed")),
            project_brief=_optional_str(payload.get("project_brief")),
            starter_flow=_optional_str(payload.get("starter_flow")),
            starter_flow_label=_optional_str(payload.get("starter_flow_label")),
            reference_brief=_optional_str(payload.get("reference_brief")),
            view_image_paths=_optional_view_paths(payload.get("view_image_paths")),
            webhook_url=_optional_str(payload.get("webhook_url")),
            target_formats=_optional_str_tuple(payload.get("target_formats")),
        )


@dataclass
class JobRecord:
    job_id: str
    status: JobStatus
    created_at: str
    updated_at: str
    request: dict[str, Any] = field(default_factory=dict)
    run_id: str | None = None
    error: str | None = None
    webhook_url: str | None = None
    webhook_delivered: bool | None = None
    webhook_error: str | None = None

    def to_dict(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "job_id": self.job_id,
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "request": self.request,
        }
        if self.run_id is not None:
            payload["run_id"] = self.run_id
        if self.error is not None:
            payload["error"] = self.error
        if self.webhook_url is not None:
            payload["webhook_url"] = self.webhook_url
        if self.webhook_delivered is not None:
            payload["webhook_delivered"] = self.webhook_delivered
        if self.webhook_error is not None:
            payload["webhook_error"] = self.webhook_error
        return payload

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> JobRecord:
        return cls(
            job_id=str(payload["job_id"]),
            status=_coerce_status(payload.get("status")),
            created_at=str(payload.get("created_at", "")),
            updated_at=str(payload.get("updated_at", "")),
            request=dict(payload.get("request") or {}),
            run_id=_optional_str(payload.get("run_id")),
            error=_optional_str(payload.get("error")),
            webhook_url=_optional_str(payload.get("webhook_url")),
            webhook_delivered=payload.get("webhook_delivered"),
            webhook_error=_optional_str(payload.get("webhook_error")),
        )


@dataclass(frozen=True)
class JobPollResponse:
    """Poll surface for automation clients (future HTTP handlers wrap this)."""

    job_id: str
    status: JobStatus
    run_id: str | None
    error: str | None
    poll_url: str | None = None
    result_ready: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "job_id": self.job_id,
            "status": self.status,
            "run_id": self.run_id,
            "error": self.error,
            "poll_url": self.poll_url,
            "result_ready": self.result_ready,
        }


def _optional_str(value: object) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _optional_int(value: object) -> int | None:
    if value is None or value == "":
        return None
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        return int(value)
    return int(str(value))


def _optional_bool(value: object) -> bool | None:
    if value is None or value == "":
        return None
    if isinstance(value, bool):
        return value
    normalized = str(value).strip().lower()
    if normalized in ("1", "true", "yes", "on"):
        return True
    if normalized in ("0", "false", "no", "off"):
        return False
    return None


def _optional_float(value: object) -> float | None:
    if value is None or value == "":
        return None
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return float(value)
    return float(str(value))



def _optional_str_tuple(value: object) -> tuple[str, ...] | None:
    if value is None:
        return None
    if isinstance(value, str):
        items = [value]
    elif isinstance(value, (list, tuple)):
        items = list(value)
    else:
        raise ValueError("target_formats must be a list of format names.")
    normalized: list[str] = []
    for item in items:
        text = _optional_str(item)
        if text:
            normalized.append(text)
    return tuple(normalized) or None


def _optional_view_paths(value: object) -> dict[str, str] | None:
    if not isinstance(value, dict):
        return None
    paths: dict[str, str] = {}
    for key, item in value.items():
        text = _optional_str(item)
        if text:
            paths[str(key)] = text
    return paths or None


def _coerce_status(value: object) -> JobStatus:
    normalized = str(value or "queued").strip().lower()
    if normalized in ("queued", "running", "succeeded", "failed"):
        return normalized  # type: ignore[return-value]
    return "queued"
