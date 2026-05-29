from __future__ import annotations

from pathlib import Path
from typing import Any

from .adapters.base import GenerationRequest
from .config import HunyuanSettings, load_config
from .exporters import mesh_topology
from .generation_pipeline import PipelineStageTracker
from .hunyuan_backend import WeightVerifiedHunyuanBackend
from .hunyuan_tier_c_runtime import evaluate_tier_c_readiness
from .tencent_hunyuan_forward import (
    describe_tencent_gpu_forward_readiness,
    resolve_tencent_forward_executors,
)
from .tencent_hunyuan_pipeline import probe_tencent_pipeline_modules

DEFAULT_GPU_FORWARD_E2E_SAMPLE = Path("assets/examples/teal_block.png")


def evaluate_gpu_forward_workstation_readiness(
    *,
    settings: HunyuanSettings | None = None,
    skip_weight_warm: bool = False,
) -> dict[str, Any]:
    """Merge tier-C, Tencent pipeline, and GPU forward gates for workstation smoke."""
    cfg = settings or load_config().hunyuan
    tier_c = evaluate_tier_c_readiness(
        settings=cfg,
        skip_weight_warm=skip_weight_warm,
    )
    pipeline = probe_tencent_pipeline_modules()
    gpu_forward = describe_tencent_gpu_forward_readiness(cfg)
    shape_executor, texture_executor = resolve_tencent_forward_executors(cfg)

    blockers: list[str] = []
    if not cfg.gpu_forward:
        blockers.append("gpu_forward_disabled")
    if not tier_c["tier_b_ready"]:
        blockers.append("tier_b")
    if not tier_c["tier_c_ready"]:
        blockers.append("tier_c")
    if not tier_c.get("inference_wired"):
        blockers.append("inference_runner")
    if not skip_weight_warm and not tier_c.get("weights_verified"):
        blockers.append("weights")
    if not pipeline["pipeline_ready"]:
        blockers.append("tencent_pipeline")
    if not gpu_forward["torch_available"]:
        blockers.append("torch")
    if not gpu_forward["cuda_available"]:
        blockers.append("cuda")

    return {
        "gpu_forward_enabled": cfg.gpu_forward,
        "gpu_executors_registered": (
            shape_executor is not None and texture_executor is not None
        ),
        "tier_c": tier_c,
        "tencent_pipeline_ready": pipeline["pipeline_ready"],
        "tencent_bindings_ready": pipeline["bindings_ready"],
        "gpu_forward": gpu_forward,
        "blockers": blockers,
        "workstation_ready": not blockers,
    }


def format_gpu_forward_workstation_report(report: dict[str, Any]) -> str:
    lines = [
        "hunyuan_gpu_forward_probe_ok=True",
        f"workstation_ready={report['workstation_ready']}",
        f"gpu_forward_enabled={report['gpu_forward_enabled']}",
        f"gpu_executors_registered={report['gpu_executors_registered']}",
        f"tencent_pipeline_ready={report['tencent_pipeline_ready']}",
        f"tencent_bindings_ready={report['tencent_bindings_ready']}",
        f"tier_b_ready={report['tier_c']['tier_b_ready']}",
        f"tier_c_ready={report['tier_c']['tier_c_ready']}",
        f"weights_verified={report['tier_c'].get('weights_verified', False)}",
        f"inference_wired={report['tier_c'].get('inference_wired', False)}",
        f"torch_available={report['gpu_forward']['torch_available']}",
        f"cuda_available={report['gpu_forward']['cuda_available']}",
    ]
    if report.get("blockers"):
        lines.append(f"blockers={','.join(report['blockers'])}")
    if report["tier_c"].get("weight_root"):
        lines.append(f"weight_root={report['tier_c']['weight_root']}")
    return "\n".join(lines) + "\n"


def attempt_gpu_forward_workstation_e2e(
    *,
    sample_path: Path | None = None,
    run_dir: Path | None = None,
    settings: HunyuanSettings | None = None,
    skip_weight_warm: bool = False,
) -> dict[str, Any]:
    """Run weight-verified Tencent GPU forward when workstation gates pass."""
    cfg = settings or load_config().hunyuan
    readiness = evaluate_gpu_forward_workstation_readiness(
        settings=cfg,
        skip_weight_warm=skip_weight_warm,
    )
    report: dict[str, Any] = {
        "readiness": readiness,
        "attempt_status": "skipped",
        "skip_reason": None,
        "error": None,
        "pipeline_stages": [],
        "mesh_vertices": None,
        "mesh_faces": None,
        "sample_path": None,
        "run_dir": None,
    }

    if not readiness["workstation_ready"]:
        report["skip_reason"] = "workstation_not_ready"
        return report
    if not cfg.weight_backend:
        report["skip_reason"] = "weight_backend_disabled"
        return report

    sample = sample_path or DEFAULT_GPU_FORWARD_E2E_SAMPLE
    report["sample_path"] = str(sample)
    if not sample.is_file():
        report["skip_reason"] = "sample_missing"
        report["error"] = f"Sample image not found: {sample}"
        return report
    if run_dir is None:
        report["skip_reason"] = "run_dir_required"
        report["error"] = "run_dir is required for GPU forward E2E attempts."
        return report

    report["run_dir"] = str(run_dir)
    tracker = PipelineStageTracker()
    backend = WeightVerifiedHunyuanBackend(settings=cfg)
    request = GenerationRequest(
        run_dir=run_dir,
        processed_image=sample,
        view_images={},
        quality="draft",
        seed=1,
        decimation_target=25_000,
    )

    try:
        mesh_result = backend.run_shape_texture(request, tracker=tracker)
    except NotImplementedError as exc:
        report["attempt_status"] = "not_implemented"
        report["error"] = str(exc)
        report["pipeline_stages"] = list(tracker.stages)
        return report
    except Exception as exc:
        report["attempt_status"] = "failed"
        report["error"] = str(exc)
        report["pipeline_stages"] = list(tracker.stages)
        return report

    vertices, faces = mesh_topology(mesh_result.mesh)
    report["attempt_status"] = "succeeded"
    report["mesh_vertices"] = vertices
    report["mesh_faces"] = faces
    report["pipeline_stages"] = list(tracker.stages)
    return report


def format_gpu_forward_e2e_report(report: dict[str, Any]) -> str:
    readiness = report["readiness"]
    lines = [
        "hunyuan_gpu_forward_e2e_ok=True",
        f"attempt_status={report['attempt_status']}",
        f"workstation_ready={readiness['workstation_ready']}",
    ]
    if report.get("skip_reason"):
        lines.append(f"skip_reason={report['skip_reason']}")
    if report.get("error"):
        lines.append(f"error={report['error']}")
    if report.get("mesh_vertices") is not None:
        lines.append(f"mesh_vertices={report['mesh_vertices']}")
        lines.append(f"mesh_faces={report['mesh_faces']}")
    if readiness.get("blockers"):
        lines.append(f"blockers={','.join(readiness['blockers'])}")
    return "\n".join(lines) + "\n"
