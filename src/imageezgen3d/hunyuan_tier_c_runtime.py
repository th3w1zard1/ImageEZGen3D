from __future__ import annotations

from pathlib import Path
from typing import Any, Callable

from .config import HunyuanSettings, load_config
from .hunyuan_runtime import probe_hunyuan_runtime
from .hunyuan_weights import (
    describe_hunyuan_weight_pin,
    ensure_hunyuan_weights,
    resolve_shape_checkpoint,
)


class TierCReadinessError(RuntimeError):
    """Tier B/C deps or weight cache are not ready for Hunyuan inference wiring."""

    def __init__(self, message: str, *, report: dict[str, Any]) -> None:
        super().__init__(message)
        self.report = report


def evaluate_tier_c_readiness(
    *,
    settings: HunyuanSettings | None = None,
    skip_weight_warm: bool = False,
    probe_runner: Callable[[], dict[str, Any]] = probe_hunyuan_runtime,
    ensure_weights: Callable[..., Path] = ensure_hunyuan_weights,
) -> dict[str, Any]:
    """Summarize tier B/C imports and optional weight cache readiness."""
    cfg = settings or load_config().hunyuan
    runtime = probe_runner()
    missing_tier_b = [
        label
        for label, entry in runtime["tier_b"].items()
        if not entry.get("available")
    ]
    missing_tier_c = [
        label
        for label, entry in runtime["tier_c"].items()
        if not entry.get("available")
    ]
    report: dict[str, Any] = {
        "tier_b_ready": runtime["tier_b_available"],
        "tier_c_ready": runtime["tier_c_available"],
        "missing_tier_b": missing_tier_b,
        "missing_tier_c": missing_tier_c,
        "weight_pin": describe_hunyuan_weight_pin(cfg),
        "weights_verified": False,
        "weight_root": "",
        "shape_checkpoint": "",
        "inference_wired": False,
    }
    if skip_weight_warm or not runtime["tier_b_available"] or not runtime["tier_c_available"]:
        return report

    try:
        weight_root = ensure_weights(settings=cfg)
        shape_checkpoint = resolve_shape_checkpoint(weight_root)
    except Exception as exc:  # noqa: BLE001 — readiness report captures warm failures
        report["weight_error"] = f"{type(exc).__name__}: {exc}"
        return report

    report["weights_verified"] = True
    report["weight_root"] = str(weight_root)
    report["shape_checkpoint"] = str(shape_checkpoint)
    return report


def prepare_tier_c_runtime(
    *,
    settings: HunyuanSettings | None = None,
    probe_runner: Callable[[], dict[str, Any]] = probe_hunyuan_runtime,
    ensure_weights: Callable[..., Path] = ensure_hunyuan_weights,
) -> dict[str, Any]:
    """Ensure weights and tier B/C imports before tier-C inference wiring."""
    report = evaluate_tier_c_readiness(
        settings=settings,
        skip_weight_warm=False,
        probe_runner=probe_runner,
        ensure_weights=ensure_weights,
    )
    if not report["tier_b_ready"]:
        missing = ", ".join(report["missing_tier_b"]) or "unknown"
        message = f"Missing tier B modules: {missing}"
        raise TierCReadinessError(message, report=report)
    if not report["tier_c_ready"]:
        missing = ", ".join(report["missing_tier_c"]) or "unknown"
        message = f"Missing tier C modules: {missing}"
        raise TierCReadinessError(message, report=report)
    if not report.get("weights_verified"):
        weight_error = report.get("weight_error", "weight cache not verified")
        message = f"Hunyuan weight cache is not ready: {weight_error}"
        raise TierCReadinessError(message, report=report)
    if not report["inference_wired"]:
        message = (
            "Tier-C dependencies satisfied; Hunyuan inference runner is not wired yet."
        )
        raise NotImplementedError(message)
    return report


def format_tier_c_readiness_report(report: dict[str, Any]) -> str:
    lines = [
        "hunyuan_tier_c_readiness_ok=True",
        f"tier_b_ready={report['tier_b_ready']}",
        f"tier_c_ready={report['tier_c_ready']}",
        f"weights_verified={report.get('weights_verified', False)}",
        f"inference_wired={report.get('inference_wired', False)}",
    ]
    if report.get("weight_root"):
        lines.append(f"weight_root={report['weight_root']}")
    if report.get("shape_checkpoint"):
        lines.append(f"shape_checkpoint={report['shape_checkpoint']}")
    if report.get("weight_error"):
        lines.append(f"weight_error={report['weight_error']}")
    if report.get("missing_tier_b"):
        lines.append(f"missing_tier_b={','.join(report['missing_tier_b'])}")
    if report.get("missing_tier_c"):
        lines.append(f"missing_tier_c={','.join(report['missing_tier_c'])}")
    return "\n".join(lines) + "\n"
