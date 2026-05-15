from __future__ import annotations

import importlib.util
import os
from dataclasses import dataclass

from .config import AppConfig


@dataclass(frozen=True)
class RuntimeStatus:
    requested_mode: str
    prefer_zerogpu: bool
    zerogpu_enabled: bool
    zerogpu_runtime_available: bool
    cpu_fallback_allowed: bool
    reason: str


def spaces_module_available() -> bool:
    return importlib.util.find_spec("spaces") is not None


def running_on_hugging_face_space() -> bool:
    markers = ("SPACE_ID", "SPACE_HOST", "SPACE_AUTHOR_NAME", "SPACE_REPO_NAME")
    return any(os.environ.get(marker) for marker in markers)


def zero_gpu_runtime_available(config: AppConfig) -> bool:
    if config.runtime.force_cpu:
        return False
    if not config.zerogpu.enabled:
        return False
    if config.zerogpu.require_spaces_runtime and not running_on_hugging_face_space():
        return False
    return spaces_module_available()


def runtime_status(config: AppConfig) -> RuntimeStatus:
    available = zero_gpu_runtime_available(config)
    if config.runtime.mode == "cpu":
        reason = "CPU runtime mode was selected explicitly."
    elif config.runtime.force_cpu:
        reason = "CPU was forced with IMAGEEZ_FORCE_CPU or pyproject runtime.force_cpu."
    elif available:
        reason = "ZeroGPU runtime is available and preferred."
    elif not config.zerogpu.enabled:
        reason = "ZeroGPU is disabled by configuration."
    elif config.zerogpu.require_spaces_runtime and not running_on_hugging_face_space():
        reason = "ZeroGPU requires a Hugging Face Space runtime; local execution falls back to CPU."
    elif not spaces_module_available():
        reason = "The optional spaces package is not importable; CPU fallback is used."
    else:
        reason = "ZeroGPU is not available; CPU fallback is used."
    return RuntimeStatus(
        requested_mode=config.runtime.mode,
        prefer_zerogpu=config.runtime.prefer_zerogpu,
        zerogpu_enabled=config.zerogpu.enabled,
        zerogpu_runtime_available=available,
        cpu_fallback_allowed=config.runtime.fallback_to_cpu,
        reason=reason,
    )
