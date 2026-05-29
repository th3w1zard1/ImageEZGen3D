from __future__ import annotations

from typing import Any

from .config import HunyuanSettings, load_config
from .hunyuan_gpu_forward_smoke import evaluate_gpu_forward_workstation_readiness
from .hunyuan_inference_runner import describe_hunyuan_inference_runner


def describe_configured_adapter_inference_path(
    *,
    settings: HunyuanSettings | None = None,
    skip_weight_warm: bool = False,
) -> dict[str, Any]:
    """Report configured-adapter inference seam without executing GPU forward."""
    cfg = settings or load_config().hunyuan
    runner = describe_hunyuan_inference_runner(cfg)
    gpu_workstation = evaluate_gpu_forward_workstation_readiness(
        settings=cfg,
        skip_weight_warm=skip_weight_warm,
    )

    if cfg.dev_backend:
        backend_kind = "dev_preview"
    elif cfg.weight_backend:
        backend_kind = "weight_verified"
    else:
        backend_kind = "none"

    neural_forward_eligible = (
        cfg.configured
        and cfg.weight_backend
        and not cfg.dev_backend
        and bool(runner["inference_wired"])
        and cfg.gpu_forward
    )
    neural_forward_ready = neural_forward_eligible and bool(
        gpu_workstation["workstation_ready"]
    )

    if not cfg.configured:
        expected_outcome = "adapter_disabled"
    elif cfg.dev_backend:
        expected_outcome = "dev_preview_mesh"
    elif not cfg.weight_backend:
        expected_outcome = "not_implemented"
    elif not runner["inference_wired"]:
        expected_outcome = "not_implemented"
    elif not cfg.gpu_forward:
        expected_outcome = "not_implemented"
    elif neural_forward_ready:
        expected_outcome = "neural_forward_attempt"
    else:
        expected_outcome = "not_implemented"

    return {
        "adapter_configured": cfg.configured,
        "backend_kind": backend_kind,
        "weight_backend": cfg.weight_backend,
        "dev_backend": cfg.dev_backend,
        "gpu_forward": cfg.gpu_forward,
        "inference_runner": runner,
        "gpu_workstation": gpu_workstation,
        "neural_forward_eligible": neural_forward_eligible,
        "neural_forward_ready": neural_forward_ready,
        "expected_outcome": expected_outcome,
        "entrypoint": (
            "HunyuanPlaceholderAdapter.generate → "
            "_run_hunyuan_inference_on_gpu → run_hunyuan_shape_texture"
        ),
    }


def format_configured_adapter_inference_report(report: dict[str, Any]) -> str:
    lines = [
        "hunyuan_configured_inference_probe_ok=True",
        f"adapter_configured={report['adapter_configured']}",
        f"backend_kind={report['backend_kind']}",
        f"neural_forward_eligible={report['neural_forward_eligible']}",
        f"neural_forward_ready={report['neural_forward_ready']}",
        f"expected_outcome={report['expected_outcome']}",
        f"workstation_ready={report['gpu_workstation']['workstation_ready']}",
        f"blockers={report['gpu_workstation']['blockers']}",
    ]
    return "\n".join(lines)
