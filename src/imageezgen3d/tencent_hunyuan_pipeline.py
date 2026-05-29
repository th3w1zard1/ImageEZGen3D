from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
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

SHAPE_PIPELINE_CLASS = "Hunyuan3DDiTPipeline"
TEXTURE_PIPELINE_CLASS = "Hunyuan3DPaintPipeline"

_SHAPE_FORWARD_NOT_WIRED = (
    "Tencent Hunyuan3D shape pipeline class is resolved but forward pass is not wired yet."
)
_TEXTURE_FORWARD_NOT_WIRED = (
    "Tencent Hunyuan3D texture pipeline class is resolved but forward pass is not wired yet."
)


@dataclass(frozen=True)
class TencentStageContext:
    """Inputs required to invoke upstream Tencent shape+texture towers."""

    run_dir: Path
    processed_image: Path
    weight_root: Path
    shape_checkpoint: Path


class TencentPipelineReadinessError(RuntimeError):
    """Upstream Tencent pipeline modules or bindings are not ready."""

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


def resolve_tencent_symbol(
    module_name: str,
    attr_name: str,
    *,
    probe_runner: Callable[[str], dict[str, Any]] = probe_tencent_module,
) -> dict[str, Any]:
    """Resolve one upstream class symbol when its module imports cleanly."""
    module_report = probe_runner(module_name)
    if not module_report.get("available"):
        return {
            "available": False,
            "module": module_name,
            "attr": attr_name,
            "error": module_report.get("error", "ModuleNotFoundError"),
            "message": module_report.get("message", f"Module {module_name!r} unavailable"),
        }
    try:
        import importlib

        module = importlib.import_module(module_name)
        symbol = getattr(module, attr_name)
    except Exception as exc:  # noqa: BLE001 — binding probe must not crash callers
        return {
            "available": False,
            "module": module_name,
            "attr": attr_name,
            "error": type(exc).__name__,
            "message": str(exc),
        }
    return {
        "available": True,
        "module": module_name,
        "attr": attr_name,
        "symbol": f"{module_name}.{attr_name}",
        "symbol_type": type(symbol).__name__,
    }


def resolve_tencent_pipeline_bindings(
    *,
    probe_runner: Callable[[str], dict[str, Any]] = probe_tencent_module,
) -> dict[str, Any]:
    shape_module = SHAPE_PIPELINE_MODULES[0][1]
    texture_module = TEXTURE_PIPELINE_MODULES[0][1]
    shape = resolve_tencent_symbol(
        shape_module,
        SHAPE_PIPELINE_CLASS,
        probe_runner=probe_runner,
    )
    texture = resolve_tencent_symbol(
        texture_module,
        TEXTURE_PIPELINE_CLASS,
        probe_runner=probe_runner,
    )
    missing_bindings: list[str] = []
    if not shape.get("available"):
        missing_bindings.append("shape_pipeline_class")
    if not texture.get("available"):
        missing_bindings.append("texture_pipeline_class")
    bindings_ready = not missing_bindings
    return {
        "shape_class": shape,
        "texture_class": texture,
        "missing_bindings": missing_bindings,
        "bindings_ready": bindings_ready,
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
    bindings = resolve_tencent_pipeline_bindings(probe_runner=probe_runner)
    pipeline_ready = shape_ready and texture_ready and bindings["bindings_ready"]
    return {
        "upstream_commit": TENCENT_UPSTREAM_COMMIT,
        "shape": shape,
        "texture": texture,
        "missing_shape": missing_shape,
        "missing_texture": missing_texture,
        "shape_ready": shape_ready,
        "texture_ready": texture_ready,
        "bindings": bindings,
        "bindings_ready": bindings["bindings_ready"],
        "pipeline_ready": pipeline_ready,
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
    if not report["bindings_ready"]:
        missing = ", ".join(report["bindings"]["missing_bindings"]) or "unknown"
        message = f"Missing Tencent pipeline class bindings: {missing}"
        raise TencentPipelineReadinessError(message, report=report)
    return report


def run_tencent_shape_stage(
    *,
    context: TencentStageContext,
    probe_runner: Callable[[str], dict[str, Any]] = probe_tencent_module,
) -> None:
    report = ensure_tencent_pipeline_ready(probe_runner=probe_runner)
    shape_binding = report["bindings"]["shape_class"]
    if not shape_binding.get("available"):
        message = "Tencent shape pipeline class binding is unavailable."
        raise TencentPipelineReadinessError(message, report=report)
    if not context.shape_checkpoint.is_file():
        message = f"Shape checkpoint missing at {context.shape_checkpoint}"
        raise FileNotFoundError(message)
    if not context.processed_image.is_file():
        message = f"Processed image missing at {context.processed_image}"
        raise FileNotFoundError(message)
    _ = context  # reserved for upstream from_pretrained / __call__ wiring (post-R)
    raise NotImplementedError(_SHAPE_FORWARD_NOT_WIRED)


def run_tencent_texture_stage(
    *,
    context: TencentStageContext,
    shape_mesh_path: Path | None = None,
    probe_runner: Callable[[str], dict[str, Any]] = probe_tencent_module,
) -> None:
    report = ensure_tencent_pipeline_ready(probe_runner=probe_runner)
    texture_binding = report["bindings"]["texture_class"]
    if not texture_binding.get("available"):
        message = "Tencent texture pipeline class binding is unavailable."
        raise TencentPipelineReadinessError(message, report=report)
    if shape_mesh_path is not None and not shape_mesh_path.is_file():
        message = f"Shape mesh missing at {shape_mesh_path}"
        raise FileNotFoundError(message)
    _ = (context, shape_mesh_path)  # reserved for upstream paint __call__ (post-R)
    raise NotImplementedError(_TEXTURE_FORWARD_NOT_WIRED)


def format_tencent_pipeline_report(report: dict[str, Any]) -> str:
    lines = [
        "hunyuan_tencent_pipeline_probe_ok=True",
        f"upstream_commit={report['upstream_commit']}",
        f"shape_ready={report['shape_ready']}",
        f"texture_ready={report['texture_ready']}",
        f"bindings_ready={report['bindings_ready']}",
        f"pipeline_ready={report['pipeline_ready']}",
    ]
    if report.get("missing_shape"):
        lines.append(f"missing_shape={','.join(report['missing_shape'])}")
    if report.get("missing_texture"):
        lines.append(f"missing_texture={','.join(report['missing_texture'])}")
    missing_bindings = report.get("bindings", {}).get("missing_bindings") or []
    if missing_bindings:
        lines.append(f"missing_bindings={','.join(missing_bindings)}")
    return "\n".join(lines) + "\n"
