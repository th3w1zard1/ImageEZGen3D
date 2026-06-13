from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from ..mesh_ops.booleans import boolean_mesh
from ..mesh_ops.convert import convert_mesh, supported_convert_formats
from ..mesh_ops.multi_color_print import multi_color_print
from ..mesh_ops.printability import analyze_printability, repair_printability
from ..mesh_ops.remesh import remesh_mesh
from ..mesh_ops.resize import resize_mesh
from ..mesh_ops.uv import unwrap_uv
from ..credits import apply_credit_estimate_to_parameters
from ..storage import RunStore
from .models import JobRequest

BOOLEAN_MODALITIES = frozenset(
    {"boolean-union", "boolean-difference", "boolean-intersection"}
)
_BOOLEAN_OPERATION_BY_MODALITY = {
    "boolean-union": "union",
    "boolean-difference": "difference",
    "boolean-intersection": "intersection",
}


def run_mesh_op_job(store: RunStore, request: JobRequest) -> dict[str, Any]:
    modality = (request.input_modality or "").strip().lower()
    input_path = _require_mesh_input(request)
    run_dir, manifest = store.create_run()
    export_dir = run_dir / "exports"
    export_dir.mkdir(parents=True, exist_ok=True)
    manifest.stage = "generating"
    manifest.parameters = {
        "input_modality": modality,
        "task_type": request.task_type or modality,
        "mesh_input_path": str(input_path),
    }
    if modality in BOOLEAN_MODALITIES:
        second_path = _require_second_mesh(request)
        manifest.parameters["second_mesh_path"] = str(second_path)
    store.save_manifest(run_dir, manifest)

    report: dict[str, Any]
    output_path: Path
    artifact_key = "glb"

    if modality == "remesh":
        output_path = export_dir / "remeshed.glb"
        remesh_report = remesh_mesh(
            input_path,
            output_path,
            target_polycount=request.target_polycount or 30_000,
            topology=request.topology or "triangle",
        )
        report = remesh_report.to_dict()
    elif modality == "convert":
        output_format = (request.mesh_output_path or "glb").strip().lower().lstrip(".")
        if output_format not in supported_convert_formats():
            raise ValueError(
                f"Unsupported convert format {output_format!r}. "
                f"Choose one of: {', '.join(supported_convert_formats())}"
            )
        output_path = export_dir / f"converted.{output_format}"
        convert_report = convert_mesh(input_path, output_path)
        report = convert_report.to_dict()
        artifact_key = output_format
    elif modality == "resize":
        output_path = export_dir / "resized.glb"
        resize_report = resize_mesh(
            input_path,
            output_path,
            resize_height=request.resize_height,
            resize_longest_side=request.resize_longest_side,
            auto_size=bool(request.auto_size),
            origin_at=request.origin_at or "bottom",
        )
        report = resize_report.to_dict()
    elif modality == "print-analyze":
        analysis = analyze_printability(input_path)
        report = analysis.to_dict()
        output_path = export_dir / "printability_analysis.json"
        output_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
        artifact_key = "analysis"
    elif modality == "print-repair":
        output_path = export_dir / "repaired.glb"
        repair_report = repair_printability(input_path, output_path)
        report = repair_report.to_dict()
    elif modality == "print-multi-color":
        output_path = export_dir / "multi_color.3mf"
        print_report = multi_color_print(
            input_path,
            output_path,
            max_colors=request.max_colors,
            max_depth=request.max_depth,
        )
        report = print_report.to_dict()
        artifact_key = "3mf"
    elif modality == "unwrap-uv":
        output_path = export_dir / "unwrapped.glb"
        unwrap_report = unwrap_uv(input_path, output_path)
        report = unwrap_report.to_dict()
    elif modality in BOOLEAN_MODALITIES:
        second_path = _require_second_mesh(request)
        operation = _BOOLEAN_OPERATION_BY_MODALITY[modality]
        output_path = export_dir / f"boolean_{operation}.glb"
        boolean_report = boolean_mesh(
            input_path,
            second_path,
            output_path,
            operation=operation,
        )
        report = boolean_report.to_dict()
    else:
        raise ValueError(f"Unsupported mesh operation modality: {modality}")

    manifest.stage = "done"
    manifest.parameters["mesh_op_report"] = report
    apply_credit_estimate_to_parameters(manifest.parameters)
    if artifact_key != "analysis":
        store.record_artifact(manifest, artifact_key, output_path)
    else:
        store.record_artifact(manifest, artifact_key, output_path)
    manifest_path = store.save_manifest(run_dir, manifest)
    store.record_artifact(manifest, "manifest", manifest_path)
    store.save_manifest(run_dir, manifest)
    payload = manifest.to_dict()
    payload["artifacts"] = {
        key: store.artifact_value(path)
        for key, path in payload["artifacts"].items()
        if store.artifact_value(path) is not None
    }
    payload["run_id"] = run_dir.name
    return payload


def _require_second_mesh(request: JobRequest) -> Path:
    path_str = request.second_mesh_path
    if not path_str:
        raise ValueError(
            "second_mesh_path is required for boolean mesh operation jobs."
        )
    path = Path(path_str)
    if not path.is_file():
        raise FileNotFoundError(f"Second mesh input not found: {path}")
    return path


def _require_mesh_input(request: JobRequest) -> Path:
    path_str = request.mesh_input_path or request.source_mesh_path
    if not path_str:
        raise ValueError("mesh_input_path or model_url is required for mesh operation jobs.")
    path = Path(path_str)
    if not path.is_file():
        raise FileNotFoundError(f"Mesh input not found: {path}")
    return path
