from __future__ import annotations

import os
import sys
from dataclasses import dataclass, field
from pathlib import Path

if sys.version_info >= (3, 11):
    import tomllib
else:  # pragma: no cover - Python 3.10 compatibility
    import tomli as tomllib


def _load_env_file(path: str | Path = ".env", *, override: bool = False) -> None:
    env_path = Path(path)
    if not env_path.exists():
        return
    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and (override or key not in os.environ):
            os.environ[key] = value


def _as_bool(value: object, default: bool = False) -> bool:
    if isinstance(value, bool):
        return value
    if value is None:
        return default
    return str(value).strip().lower() in {"1", "true", "yes", "on"}


def _env_bool(name: str, current: bool) -> bool:
    return _as_bool(os.environ.get(name), current) if name in os.environ else current


def _env_int(name: str, current: int) -> int:
    if name not in os.environ:
        return current
    return int(os.environ[name])


def _env_float(name: str, current: float) -> float:
    if name not in os.environ:
        return current
    return float(os.environ[name])


def _env_str(name: str, current: str) -> str:
    return os.environ.get(name, current)


def _running_on_hugging_face_space() -> bool:
    markers = ("SPACE_ID", "SPACE_HOST", "SPACE_AUTHOR_NAME", "SPACE_REPO_NAME")
    return any(os.environ.get(marker) for marker in markers)


def resolve_output_dir(
    *,
    configured: str = "outputs",
    data_root: Path | None = None,
    space_runtime: bool | None = None,
) -> Path:
    """Pick run storage root: explicit env, then Space /data when writable, else configured."""
    if "IMAGEEZ_OUTPUT_DIR" in os.environ:
        return Path(os.environ["IMAGEEZ_OUTPUT_DIR"])

    on_space = (
        _running_on_hugging_face_space()
        if space_runtime is None
        else space_runtime
    )
    if on_space:
        root = data_root if data_root is not None else Path("/data")
        if root.is_dir() and os.access(root, os.W_OK):
            return root / "outputs"

    return Path(configured)


def _resolve_launch_port(launch_raw: dict[str, object]) -> int:
    default_port = _int_value(launch_raw, "port", LaunchSettings.port)
    port = _env_int(
        "PORT",
        _env_int(
            "GRADIO_SERVER_PORT",
            _env_int("IMAGEEZ_PORT", default_port),
        ),
    )
    if (
        _running_on_hugging_face_space()
        and port == default_port
        and "PORT" not in os.environ
        and "GRADIO_SERVER_PORT" not in os.environ
        and "IMAGEEZ_PORT" not in os.environ
    ):
        return 7860
    return port


def _str_value(section: dict[str, object], key: str, default: str) -> str:
    value = section.get(key, default)
    return str(value)


def _int_value(section: dict[str, object], key: str, default: int) -> int:
    value = section.get(key, default)
    if isinstance(value, int):
        return value
    if isinstance(value, float | str):
        return int(value)
    return default


def _float_value(section: dict[str, object], key: str, default: float) -> float:
    value = section.get(key, default)
    if isinstance(value, int | float | str):
        return float(value)
    return default


def _bool_value(section: dict[str, object], key: str, default: bool) -> bool:
    return _as_bool(section.get(key), default)


def _str_tuple_value(
    section: dict[str, object], key: str, default: tuple[str, ...]
) -> tuple[str, ...]:
    value = section.get(key, default)
    if isinstance(value, list | tuple):
        return tuple(str(item) for item in value)
    return default


@dataclass(frozen=True)
class AppSettings:
    title: str = "ImageEZGen3D"
    output_dir: Path = Path("outputs")
    adapter: str = "auto"
    cpu_adapter: str = "cpu-demo"
    zerogpu_adapter: str = "hunyuan-zerogpu"


@dataclass(frozen=True)
class LaunchSettings:
    host: str = "0.0.0.0"
    port: int = 7865
    share: bool = False
    queue_max_size: int = 32
    default_concurrency_limit: int = 1


@dataclass(frozen=True)
class StorageSettings:
    retention_runs: int = 100
    keep_failed_runs: bool = True


@dataclass(frozen=True)
class GenerationSettings:
    seed: int = 42
    quality: str = "draft"
    texture_size: int = 1024
    decimation_target: int = 500_000
    preserve_intermediates: bool = True


@dataclass(frozen=True)
class PreprocessingSettings:
    target_size: int = 768
    minimum_short_side: int = 256
    maximum_long_side: int = 4096
    blur_edge_variance_threshold: float = 90.0
    low_contrast_threshold: float = 18.0


@dataclass(frozen=True)
class RuntimeSettings:
    mode: str = "auto"
    prefer_zerogpu: bool = True
    fallback_to_cpu: bool = True
    force_cpu: bool = False


@dataclass(frozen=True)
class ZeroGPUSettings:
    enabled: bool = True
    default_duration_seconds: int = 60
    texture_duration_seconds: int = 180
    size: str = "large"
    require_spaces_runtime: bool = True


@dataclass(frozen=True)
class HunyuanSettings:
    """Admission-controlled enablement flag. Default off; inference may still be unwired."""

    configured: bool = False
    model_repo: str = "tencent/Hunyuan3D-2.1"
    model_revision: str = "0b94677654c57bb9a6b6845cd7b704ccf551d327"
    cache_dir: str = ""


@dataclass(frozen=True)
class TextNeuralSettings:
    """Admission-controlled text-to-3D neural enablement. Default off."""

    configured: bool = False


@dataclass(frozen=True)
class ExportSettings:
    default_format: str = "glb"
    formats: tuple[str, ...] = ("glb", "obj", "ply", "stl")


@dataclass(frozen=True)
class AppConfig:
    app: AppSettings = field(default_factory=AppSettings)
    launch: LaunchSettings = field(default_factory=LaunchSettings)
    storage: StorageSettings = field(default_factory=StorageSettings)
    generation: GenerationSettings = field(default_factory=GenerationSettings)
    preprocessing: PreprocessingSettings = field(default_factory=PreprocessingSettings)
    runtime: RuntimeSettings = field(default_factory=RuntimeSettings)
    zerogpu: ZeroGPUSettings = field(default_factory=ZeroGPUSettings)
    hunyuan: HunyuanSettings = field(default_factory=HunyuanSettings)
    text_neural: TextNeuralSettings = field(default_factory=TextNeuralSettings)
    exports: ExportSettings = field(default_factory=ExportSettings)


def _section(data: dict[str, object], key: str) -> dict[str, object]:
    value = data.get(key, {})
    return value if isinstance(value, dict) else {}


def _load_pyproject(path: Path) -> dict[str, object]:
    if not path.exists():
        return {}
    loaded = tomllib.loads(path.read_text(encoding="utf-8"))
    tool = loaded.get("tool", {})
    if isinstance(tool, dict):
        imageez = tool.get("imageezgen3d", {})
        if isinstance(imageez, dict):
            return imageez
    return loaded if isinstance(loaded, dict) else {}


def load_config(path: str | Path | None = None) -> AppConfig:
    if path is None:
        _load_env_file()
        config_path = Path(os.environ.get("IMAGEEZ_CONFIG", "pyproject.toml"))
    else:
        config_path = Path(path)
    raw = _load_pyproject(config_path)

    app_raw = _section(raw, "app")
    launch_raw = _section(raw, "launch")
    storage_raw = _section(raw, "storage")
    generation_raw = _section(raw, "generation")
    preprocessing_raw = _section(raw, "preprocessing")
    runtime_raw = _section(raw, "runtime")
    zerogpu_raw = _section(raw, "zerogpu")
    hunyuan_raw = _section(raw, "hunyuan")
    text_neural_raw = _section(raw, "text_neural")
    exports_raw = _section(raw, "exports")

    formats = _str_tuple_value(exports_raw, "formats", ExportSettings.formats)
    return AppConfig(
        app=AppSettings(
            title=_env_str(
                "IMAGEEZ_TITLE", _str_value(app_raw, "title", AppSettings.title)
            ),
            output_dir=resolve_output_dir(
                configured=_str_value(
                    app_raw, "output_dir", str(AppSettings.output_dir)
                ),
            ),
            adapter=_env_str(
                "IMAGEEZ_ADAPTER", _str_value(app_raw, "adapter", AppSettings.adapter)
            ),
            cpu_adapter=_env_str(
                "IMAGEEZ_CPU_ADAPTER",
                _str_value(app_raw, "cpu_adapter", AppSettings.cpu_adapter),
            ),
            zerogpu_adapter=_env_str(
                "IMAGEEZ_ZEROGPU_ADAPTER",
                _str_value(app_raw, "zerogpu_adapter", AppSettings.zerogpu_adapter),
            ),
        ),
        launch=LaunchSettings(
            host=_env_str(
                "IMAGEEZ_HOST", _str_value(launch_raw, "host", LaunchSettings.host)
            ),
            port=_resolve_launch_port(launch_raw),
            share=_env_bool(
                "IMAGEEZ_SHARE", _bool_value(launch_raw, "share", LaunchSettings.share)
            ),
            queue_max_size=_env_int(
                "IMAGEEZ_QUEUE_MAX_SIZE",
                _int_value(launch_raw, "queue_max_size", LaunchSettings.queue_max_size),
            ),
            default_concurrency_limit=_env_int(
                "IMAGEEZ_DEFAULT_CONCURRENCY_LIMIT",
                _int_value(
                    launch_raw,
                    "default_concurrency_limit",
                    LaunchSettings.default_concurrency_limit,
                ),
            ),
        ),
        storage=StorageSettings(
            retention_runs=_int_value(
                storage_raw, "retention_runs", StorageSettings.retention_runs
            ),
            keep_failed_runs=_bool_value(
                storage_raw, "keep_failed_runs", StorageSettings.keep_failed_runs
            ),
        ),
        generation=GenerationSettings(
            seed=_int_value(generation_raw, "seed", GenerationSettings.seed),
            quality=_str_value(generation_raw, "quality", GenerationSettings.quality),
            texture_size=_int_value(
                generation_raw, "texture_size", GenerationSettings.texture_size
            ),
            decimation_target=_int_value(
                generation_raw,
                "decimation_target",
                GenerationSettings.decimation_target,
            ),
            preserve_intermediates=_bool_value(
                generation_raw,
                "preserve_intermediates",
                GenerationSettings.preserve_intermediates,
            ),
        ),
        preprocessing=PreprocessingSettings(
            target_size=_env_int(
                "IMAGEEZ_PREPROCESS_TARGET_SIZE",
                _int_value(
                    preprocessing_raw, "target_size", PreprocessingSettings.target_size
                ),
            ),
            minimum_short_side=_env_int(
                "IMAGEEZ_MINIMUM_SHORT_SIDE",
                _int_value(
                    preprocessing_raw,
                    "minimum_short_side",
                    PreprocessingSettings.minimum_short_side,
                ),
            ),
            maximum_long_side=_env_int(
                "IMAGEEZ_MAXIMUM_LONG_SIDE",
                _int_value(
                    preprocessing_raw,
                    "maximum_long_side",
                    PreprocessingSettings.maximum_long_side,
                ),
            ),
            blur_edge_variance_threshold=_env_float(
                "IMAGEEZ_BLUR_EDGE_VARIANCE_THRESHOLD",
                _float_value(
                    preprocessing_raw,
                    "blur_edge_variance_threshold",
                    PreprocessingSettings.blur_edge_variance_threshold,
                ),
            ),
            low_contrast_threshold=_env_float(
                "IMAGEEZ_LOW_CONTRAST_THRESHOLD",
                _float_value(
                    preprocessing_raw,
                    "low_contrast_threshold",
                    PreprocessingSettings.low_contrast_threshold,
                ),
            ),
        ),
        runtime=RuntimeSettings(
            mode=_env_str(
                "IMAGEEZ_RUNTIME", _str_value(runtime_raw, "mode", RuntimeSettings.mode)
            ),
            prefer_zerogpu=_env_bool(
                "IMAGEEZ_PREFER_ZEROGPU",
                _bool_value(
                    runtime_raw, "prefer_zerogpu", RuntimeSettings.prefer_zerogpu
                ),
            ),
            fallback_to_cpu=_env_bool(
                "IMAGEEZ_FALLBACK_TO_CPU",
                _bool_value(
                    runtime_raw, "fallback_to_cpu", RuntimeSettings.fallback_to_cpu
                ),
            ),
            force_cpu=_env_bool(
                "IMAGEEZ_FORCE_CPU",
                _bool_value(runtime_raw, "force_cpu", RuntimeSettings.force_cpu),
            ),
        ),
        zerogpu=ZeroGPUSettings(
            enabled=_env_bool(
                "IMAGEEZ_ZEROGPU_ENABLED",
                _bool_value(zerogpu_raw, "enabled", ZeroGPUSettings.enabled),
            ),
            default_duration_seconds=_int_value(
                zerogpu_raw,
                "default_duration_seconds",
                ZeroGPUSettings.default_duration_seconds,
            ),
            texture_duration_seconds=_int_value(
                zerogpu_raw,
                "texture_duration_seconds",
                ZeroGPUSettings.texture_duration_seconds,
            ),
            size=_env_str(
                "IMAGEEZ_ZEROGPU_SIZE",
                _str_value(zerogpu_raw, "size", ZeroGPUSettings.size),
            ),
            require_spaces_runtime=_env_bool(
                "IMAGEEZ_ZEROGPU_REQUIRE_SPACES_RUNTIME",
                _bool_value(
                    zerogpu_raw,
                    "require_spaces_runtime",
                    ZeroGPUSettings.require_spaces_runtime,
                ),
            ),
        ),
        hunyuan=HunyuanSettings(
            configured=_env_bool(
                "IMAGEEZ_HUNYUAN_CONFIGURED",
                _bool_value(
                    hunyuan_raw, "configured", HunyuanSettings.configured
                ),
            ),
            model_repo=_env_str(
                "IMAGEEZ_HUNYUAN_MODEL_REPO",
                str(hunyuan_raw.get("model_repo", HunyuanSettings.model_repo)),
            ),
            model_revision=_env_str(
                "IMAGEEZ_HUNYUAN_MODEL_REVISION",
                str(
                    hunyuan_raw.get(
                        "model_revision", HunyuanSettings.model_revision
                    )
                ),
            ),
            cache_dir=_env_str(
                "IMAGEEZ_HUNYUAN_CACHE_DIR",
                str(hunyuan_raw.get("cache_dir", HunyuanSettings.cache_dir)),
            ),
        ),
        text_neural=TextNeuralSettings(
            configured=_env_bool(
                "IMAGEEZ_TEXT_NEURAL_CONFIGURED",
                _bool_value(
                    text_neural_raw,
                    "configured",
                    TextNeuralSettings.configured,
                ),
            ),
        ),
        exports=ExportSettings(
            default_format=str(
                exports_raw.get("default_format", ExportSettings.default_format)
            ),
            formats=formats,
        ),
    )
