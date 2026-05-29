from __future__ import annotations

from typing import Any, Callable

from .hunyuan_runtime import probe_import

# [OFFICIAL] Tencent-Hunyuan/Hunyuan3D-2.1 @ 82920d64 (G1/G3 pin)
TENCENT_UPSTREAM_COMMIT = "82920d643c0dc2f7bfd7255f45f62d386edfe60c"

SHAPE_PIPELINE_MODULES: tuple[tuple[str, str], ...] = (
    ("hy3dshape_pipelines", "hy3dshape.hy3dshape.pipelines"),
)

TEXTURE_PIPELINE_MODULES: tuple[tuple[str, str], ...] = (
    ("texture_gen_pipeline", "hy3dpaint.textureGenPipeline"),
    ("hunyuan_paint_pbr", "hy3dpaint.hunyuanpaintpbr.pipeline"),
)

_SHAPE_NOT_WIRED = (
    "Tencent Hunyuan3D shape tower entrypoints are present but not wired yet."
)
_TEXTURE_NOT_WIRED = (
    "Tencent Hunyuan3D texture tower entrypoints are present but not wired yet."
)


class TencentPipelineReadinessError(RuntimeError):
    """Upstream Tencent pipeline modules are not importable in this environment."""

    def __init__(self, message: str, *, report: dict[str, Any]) -> None:
        super().__init__(message)
        self.report = report


def probe_tencent_module(module_name: str) -> dict[str, Any]:
    """Probe upstream module import without raising when optional deps are missing."""
    try:
        return probe_import(module_name)
    except Exception as exc:  # noqa: BLE001 — partial upstream installs must not crash probes
        return {
            "available": False,
            "error": type(exc).__name__,
            "message": str(exc),
        }


def probe_tencent_pipeline_modules(
    *,
    probe_runner: Callable[[str], dict[str, Any]] = probe_tencent_module,
) -> dict[str, Any]:
    shape = {label: probe_runner(module) for label, module in SHAPE_PIPELINE_MODULES}
    texture = {label: probe_runner(module) for label, module in TEXTURE_PIPELINE_MODULES}
    missing_shape = [label for label, entry in shape.items() if not entry.get("available")]
    missing_texture = [label for label, entry in texture.items() if not entry.get("available")]
    shape_ready = not missing_shape
    texture_ready = not missing_texture
    return {
        "upstream_commit": TENCENT_UPSTREAM_COMMIT,
        "shape": shape,
        "texture": texture,
        "missing_shape": missing_shape,
        "missing_texture": missing_texture,
        "shape_ready": shape_ready,
        "texture_ready": texture_ready,
        "pipeline_ready": shape_ready and texture_ready,
    }


def ensure_tencent_pipeline_ready(
    *,
    probe_runner: Callable[[str], dict[str, Any]] = probe_tencent_module,
) -> dict[str, Any]:
    report = probe_tencent_pipeline_modules(probe_runner=probe_runner)
    if not report["shape_ready"]:
        missing = ", ".join(report["missing_shape"]) or "unknown"
        message = f"Missing Tencent shape pipeline modules: {missing}"
        raise TencentPipelineReadinessError(message, report=report)
    if not report["texture_ready"]:
        missing = ", ".join(report["missing_texture"]) or "unknown"
        message = f"Missing Tencent texture pipeline modules: {missing}"
        raise TencentPipelineReadinessError(message, report=report)
    return report


def run_tencent_shape_stage(
    *,
    probe_runner: Callable[[str], dict[str, Any]] = probe_tencent_module,
) -> None:
    ensure_tencent_pipeline_ready(probe_runner=probe_runner)
    raise NotImplementedError(_SHAPE_NOT_WIRED)


def run_tencent_texture_stage(
    *,
    probe_runner: Callable[[str], dict[str, Any]] = probe_tencent_module,
) -> None:
    ensure_tencent_pipeline_ready(probe_runner=probe_runner)
    raise NotImplementedError(_TEXTURE_NOT_WIRED)


def format_tencent_pipeline_report(report: dict[str, Any]) -> str:
    lines = [
        "hunyuan_tencent_pipeline_probe_ok=True",
        f"upstream_commit={report['upstream_commit']}",
        f"shape_ready={report['shape_ready']}",
        f"texture_ready={report['texture_ready']}",
        f"pipeline_ready={report['pipeline_ready']}",
    ]
    if report.get("missing_shape"):
        lines.append(f"missing_shape={','.join(report['missing_shape'])}")
    if report.get("missing_texture"):
        lines.append(f"missing_texture={','.join(report['missing_texture'])}")
    return "\n".join(lines) + "\n"
