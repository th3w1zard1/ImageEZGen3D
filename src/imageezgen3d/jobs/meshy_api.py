from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal

from ..credits import estimate_credits, informational_balance_starting
from .models import JobPollResponse, JobRequest, JobStatus

MeshyTaskStatus = Literal["PENDING", "IN_PROGRESS", "SUCCEEDED", "FAILED", "CANCELED"]

_STATUS_TO_MESHY: dict[JobStatus, MeshyTaskStatus] = {
    "queued": "PENDING",
    "running": "IN_PROGRESS",
    "succeeded": "SUCCEEDED",
    "failed": "FAILED",
}

_MESHY_RESOURCE_NAMES: dict[str, str] = {
    "text-to-3d": "text-to-3d",
    "image-to-3d": "image-to-3d",
    "multi-image-to-3d": "multi-image-to-3d",
    "retexture": "retexture",
    "text-to-image": "text-to-image",
    "image-to-image": "image-to-image",
    "rigging": "rigging",
    "animations": "animations",
    "remesh": "remesh",
    "convert": "convert",
    "resize": "resize",
    "analyze-printability": "analyze-printability",
    "repair-printability": "repair-printability",
}

_SYNTHETIC_BALANCE = informational_balance_starting()


@dataclass(frozen=True)
class MeshyRouteMatch:
    action: Literal["create", "retrieve", "stream", "balance"]
    task_kind: str | None = None
    task_id: str | None = None


def meshy_status(status: JobStatus) -> MeshyTaskStatus:
    return _STATUS_TO_MESHY.get(status, "PENDING")


def meshy_balance_payload() -> dict[str, Any]:
    return {
        "balance": _SYNTHETIC_BALANCE,
        "currency": "credits",
        "note": "Synthetic informational balance for local Meshy-shaped API parity.",
    }


def match_meshy_route(segments: list[str], method: str) -> MeshyRouteMatch | None:
    if method == "GET" and segments == ["openapi", "v1", "balance"]:
        return MeshyRouteMatch(action="balance")

    if (
        method == "POST"
        and len(segments) == 3
        and segments[0] == "openapi"
        and segments[1] in ("v1", "v2")
    ):
        resource = segments[2]
        if resource in _MESHY_RESOURCE_NAMES:
            return MeshyRouteMatch(action="create", task_kind=_MESHY_RESOURCE_NAMES[resource])
        return None

    if (
        method == "POST"
        and len(segments) == 5
        and segments[0] == "openapi"
        and segments[1] == "creative-lab"
        and segments[3] == "v1"
        and segments[4] in ("prototype", "build")
    ):
        flow = segments[2]
        return MeshyRouteMatch(
            action="create",
            task_kind=f"creative-lab:{flow}:{segments[4]}",
        )

    if (
        method == "POST"
        and len(segments) == 4
        and segments[0] == "openapi"
        and segments[1] == "v1"
        and segments[2] == "print"
        and segments[3] == "multi-color"
    ):
        return MeshyRouteMatch(action="create", task_kind="print-multi-color")

    if (
        method == "GET"
        and len(segments) == 5
        and segments[0] == "openapi"
        and segments[1] == "v1"
        and segments[2] == "print"
        and segments[3] == "multi-color"
    ):
        return MeshyRouteMatch(
            action="retrieve",
            task_kind="print-multi-color",
            task_id=segments[4],
        )

    if (
        method == "GET"
        and len(segments) == 6
        and segments[0] == "openapi"
        and segments[1] == "v1"
        and segments[2] == "print"
        and segments[3] == "multi-color"
        and segments[5] == "stream"
    ):
        return MeshyRouteMatch(
            action="stream",
            task_kind="print-multi-color",
            task_id=segments[4],
        )

    if (
        method == "GET"
        and len(segments) == 4
        and segments[0] == "openapi"
        and segments[1] == "v1"
        and segments[2] in _MESHY_RESOURCE_NAMES
    ):
        return MeshyRouteMatch(
            action="retrieve",
            task_kind=_MESHY_RESOURCE_NAMES[segments[2]],
            task_id=segments[3],
        )

    if (
        method == "GET"
        and len(segments) == 5
        and segments[0] == "openapi"
        and segments[1] == "v1"
        and segments[2] in _MESHY_RESOURCE_NAMES
        and segments[4] == "stream"
    ):
        return MeshyRouteMatch(
            action="stream",
            task_kind=_MESHY_RESOURCE_NAMES[segments[2]],
            task_id=segments[3],
        )

    return None


def job_request_from_meshy(task_kind: str, payload: dict[str, Any]) -> JobRequest:
    if task_kind.startswith("creative-lab:"):
        _, flow, stage = task_kind.split(":", 2)
        return JobRequest(
            input_modality="creative-lab",
            prompt_text=_optional_str(payload.get("prompt")),
            image_path=_resolve_local_asset(payload, "image_url", "image_path"),
            creative_lab_flow=flow,
            creative_lab_stage=stage,
            task_type=task_kind,
        )

    if task_kind == "text-to-3d":
        mode = str(payload.get("mode") or "preview").strip().lower()
        lane = "preview" if mode == "preview" else "refine"
        return JobRequest(
            input_modality="text",
            prompt_text=_optional_str(payload.get("prompt")),
            lane=lane,
            topology=_optional_str(payload.get("topology")),
            target_polycount=_optional_int(payload.get("target_polycount")),
            enable_pbr=_optional_bool(payload.get("enable_pbr")),
            task_type=task_kind,
        )

    if task_kind == "image-to-3d":
        texture_prompt = _optional_str(payload.get("texture_prompt"))
        texture_image = _resolve_local_asset(
            payload, "texture_image_url", "texture_image_path"
        )
        return JobRequest(
            input_modality="image",
            image_path=_resolve_local_asset(payload, "image_url", "image_path"),
            prompt_text=texture_prompt,
            texture_image_path=texture_image,
            lane="refine" if payload.get("enable_pbr") else "preview",
            topology=_optional_str(payload.get("topology")),
            target_polycount=_optional_int(payload.get("target_polycount")),
            enable_pbr=_optional_bool(payload.get("enable_pbr")),
            task_type=task_kind,
        )

    if task_kind == "multi-image-to-3d":
        texture_prompt = _optional_str(payload.get("texture_prompt"))
        texture_image = _resolve_local_asset(
            payload, "texture_image_url", "texture_image_path"
        )
        view_paths = _resolve_image_urls(payload)
        primary_path = _resolve_local_asset(payload, "image_url", "image_path")
        if not primary_path and view_paths:
            primary_path = next(iter(view_paths.values()))
        if not primary_path and not view_paths:
            raise ValueError(
                "multi-image-to-3d requires image_urls or a local image_path/image_url."
            )
        return JobRequest(
            input_modality="multi-image-to-3d",
            image_path=primary_path,
            view_image_paths=view_paths or None,
            prompt_text=texture_prompt,
            texture_image_path=texture_image,
            lane="refine" if payload.get("enable_pbr") else "preview",
            topology=_optional_str(payload.get("topology")),
            target_polycount=_optional_int(payload.get("target_polycount")),
            enable_pbr=_optional_bool(payload.get("enable_pbr")),
            task_type=task_kind,
        )

    if task_kind == "retexture":
        return JobRequest(
            input_modality="retexture",
            texture_image_path=_resolve_local_asset(
                payload, "texture_image_url", "texture_image_path"
            ),
            source_mesh_path=_resolve_local_asset(payload, "model_url", "source_mesh_path"),
            prompt_text=_optional_str(payload.get("text_style_prompt")),
            task_type=task_kind,
        )

    if task_kind == "text-to-image":
        return JobRequest(
            input_modality="text-to-image",
            prompt_text=_optional_str(payload.get("prompt")),
            aspect_ratio=_optional_str(payload.get("aspect_ratio")),
            task_type=task_kind,
        )

    if task_kind == "image-to-image":
        return JobRequest(
            input_modality="image-to-image",
            image_path=_resolve_local_asset(payload, "image_url", "image_path"),
            prompt_text=_optional_str(payload.get("prompt")),
            aspect_ratio=_optional_str(payload.get("aspect_ratio")),
            task_type=task_kind,
        )

    if task_kind == "rigging":
        return JobRequest(
            input_modality="rig",
            source_mesh_path=_resolve_local_asset(payload, "model_url", "source_mesh_path"),
            task_type=task_kind,
        )

    if task_kind == "animations":
        return JobRequest(
            input_modality="animate",
            action_id=payload.get("action_id"),
            source_mesh_path=_resolve_local_asset(payload, "model_url", "source_mesh_path"),
            task_type=task_kind,
        )

    if task_kind == "remesh":
        return JobRequest(
            input_modality="remesh",
            mesh_input_path=_resolve_mesh_input(payload),
            topology=_optional_str(payload.get("topology")),
            target_polycount=_optional_int(payload.get("target_polycount")),
            task_type=task_kind,
        )

    if task_kind == "convert":
        output_format = _optional_str(payload.get("format")) or _optional_str(
            payload.get("output_format")
        )
        return JobRequest(
            input_modality="convert",
            mesh_input_path=_resolve_mesh_input(payload),
            mesh_output_path=output_format or "glb",
            task_type=task_kind,
        )

    if task_kind == "resize":
        return JobRequest(
            input_modality="resize",
            mesh_input_path=_resolve_mesh_input(payload),
            resize_height=_optional_float(payload.get("height")),
            resize_longest_side=_optional_float(payload.get("longest_side")),
            auto_size=_optional_bool(payload.get("auto_size")),
            origin_at=_optional_str(payload.get("origin_at")),
            task_type=task_kind,
        )

    if task_kind == "analyze-printability":
        return JobRequest(
            input_modality="print-analyze",
            mesh_input_path=_resolve_mesh_input(payload),
            task_type=task_kind,
        )

    if task_kind == "repair-printability":
        return JobRequest(
            input_modality="print-repair",
            mesh_input_path=_resolve_mesh_input(payload),
            task_type=task_kind,
        )

    if task_kind == "print-multi-color":
        from ..mesh_ops.multi_color_print import validate_max_colors, validate_max_depth

        mesh_input = _resolve_mesh_input(payload)
        if not mesh_input:
            raise ValueError("Either model_url or input_task_id must be provided.")
        return JobRequest(
            input_modality="print-multi-color",
            mesh_input_path=mesh_input,
            max_colors=validate_max_colors(_optional_int(payload.get("max_colors"))),
            max_depth=validate_max_depth(_optional_int(payload.get("max_depth"))),
            task_type=task_kind,
        )

    raise ValueError(f"Unsupported Meshy task kind: {task_kind}")


def meshy_task_payload(
    *,
    task_kind: str,
    task_id: str,
    poll: JobPollResponse,
    manifest: dict[str, Any] | None = None,
) -> dict[str, Any]:
    status = meshy_status(poll.status)
    payload: dict[str, Any] = {
        "id": task_id,
        "task_id": task_id,
        "type": task_kind,
        "status": status,
        "progress": _progress_for_status(status),
    }
    if poll.error:
        payload["task_error"] = {"message": poll.error}
    credits = _consumed_credits(payload["status"], manifest, task_kind)
    payload["consumed_credits"] = credits
    if manifest is not None and status == "SUCCEEDED":
        payload.update(_meshy_result_fields(manifest))
    return payload


def meshy_webhook_payload(
    *,
    task_kind: str,
    job_id: str,
    status: JobStatus,
    run_id: str | None,
    error: str | None,
    result: dict[str, Any] | None,
) -> dict[str, Any]:
    meshy_status_value = meshy_status(status)
    body: dict[str, Any] = {
        "id": job_id,
        "task_id": job_id,
        "type": task_kind,
        "status": meshy_status_value,
        "progress": _progress_for_status(meshy_status_value),
        "job_id": job_id,
        "run_id": run_id,
        "error": error,
    }
    if status == "succeeded" and result:
        body["result"] = result
        body.update(_meshy_result_fields(result))
    return body


def _consumed_credits(
    status: MeshyTaskStatus,
    manifest: dict[str, Any] | None,
    task_kind: str,
) -> int:
    if status == "FAILED":
        return 0
    parameters: dict[str, Any] = {}
    if isinstance(manifest, dict):
        raw = manifest.get("parameters")
        if isinstance(raw, dict):
            parameters = raw
    if parameters.get("consumed_credits") is not None:
        return int(parameters["consumed_credits"])
    return estimate_credits({**parameters, "task_type": task_kind}).consumed_credits


def _meshy_result_fields(manifest: dict[str, Any]) -> dict[str, Any]:
    artifacts = manifest.get("artifacts", {})
    if not isinstance(artifacts, dict):
        artifacts = {}
    model_urls: dict[str, str] = {}
    for key in ("glb", "obj", "stl", "fbx", "usdz", "3mf", "png", "image", "prototype"):
        value = artifacts.get(key)
        if isinstance(value, str) and value:
            model_urls[key] = value
    fields: dict[str, Any] = {}
    if model_urls:
        fields["model_urls"] = model_urls
    parameters = manifest.get("parameters", {})
    if isinstance(parameters, dict):
        for key in ("task_type", "action_id", "creative_lab_flow", "creative_lab_stage"):
            if parameters.get(key) is not None:
                fields[key] = parameters[key]
        mesh_report = manifest.get("mesh_report")
        if isinstance(mesh_report, dict):
            fields["mesh_report"] = mesh_report
        mesh_op = parameters.get("mesh_op_report")
        if isinstance(mesh_op, dict):
            fields["mesh_op_report"] = mesh_op
    return fields


def _progress_for_status(status: MeshyTaskStatus) -> int:
    if status == "PENDING":
        return 0
    if status == "IN_PROGRESS":
        return 50
    if status == "SUCCEEDED":
        return 100
    return 0


def _resolve_local_asset(
    payload: dict[str, Any],
    url_key: str,
    path_key: str,
) -> str | None:
    direct = _optional_str(payload.get(path_key))
    if direct:
        return direct
    url_value = _optional_str(payload.get(url_key))
    if url_value and not url_value.startswith(("http://", "https://")):
        return url_value
    return None


def _resolve_mesh_input(payload: dict[str, Any]) -> str | None:
    direct = _resolve_local_asset(payload, "model_url", "mesh_input_path")
    if direct:
        return direct
    return _optional_str(payload.get("input_task_id"))


def _resolve_image_urls(payload: dict[str, Any]) -> dict[str, str]:
    raw_urls = payload.get("image_urls")
    if not isinstance(raw_urls, list):
        return {}
    labels = ("front", "back", "left", "right")
    view_paths: dict[str, str] = {}
    for index, item in enumerate(raw_urls[:4]):
        path = _resolve_url_item(item)
        if not path:
            continue
        label = labels[index] if index < len(labels) else f"view_{index}"
        view_paths[label] = path
    return view_paths


def _resolve_url_item(value: object) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    if not text:
        return None
    if text.startswith(("http://", "https://", "data:")):
        return None
    return text


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
