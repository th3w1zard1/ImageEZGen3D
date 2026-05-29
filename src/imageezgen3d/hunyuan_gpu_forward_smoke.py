from __future__ import annotations

from typing import Any

from .config import HunyuanSettings, load_config
from .hunyuan_tier_c_runtime import evaluate_tier_c_readiness
from .tencent_hunyuan_forward import (
    describe_tencent_gpu_forward_readiness,
    resolve_tencent_forward_executors,
)
from .tencent_hunyuan_pipeline import probe_tencent_pipeline_modules


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
