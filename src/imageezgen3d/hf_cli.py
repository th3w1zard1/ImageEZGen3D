from __future__ import annotations

import shutil
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class HfCliStatus:
    available: bool
    executable: str | None
    recommended_commands: tuple[str, ...]


_SPACE_PAYLOAD_PATHS = (
    "README.md",
    "app.py",
    "pyproject.toml",
    "requirements.txt",
    "runtime.txt",
    "assets",
    "src",
)


def _workspace_root() -> Path:
    return Path(__file__).resolve().parents[2]


def stage_space_payload(destination: Path, *, workspace_root: Path | None = None) -> Path:
    source_root = workspace_root or _workspace_root()
    destination.mkdir(parents=True, exist_ok=True)
    ignore = shutil.ignore_patterns(
        "__pycache__",
        "*.pyc",
        "*.pyo",
        "imageezgen3d.egg-info",
    )
    for relative in _SPACE_PAYLOAD_PATHS:
        source = source_root / relative
        if not source.exists():
            continue
        target = destination / relative
        if source.is_dir():
            shutil.copytree(source, target, dirs_exist_ok=True, ignore=ignore)
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
    return destination


def hf_cli_status(
    space_id: str = "YOUR_USERNAME/ImageEZGen3D",
    *,
    space_sdk: str = "gradio",
) -> HfCliStatus:
    executable = shutil.which("hf")
    if executable is None:
        sibling = Path(sys.executable).with_name("hf")
        if sibling.is_file():
            executable = str(sibling)
    command = executable or "hf"
    commands = (
        f"{command} auth whoami",
        f"{command} env",
        f"{command} repo create {space_id} --repo-type space --space-sdk {space_sdk} --exist-ok",
        f"{command} download tencent/Hunyuan3D-2.1 --dry-run",
        f"{command} cache ls",
        f"{command} cache verify tencent/Hunyuan3D-2.1",
        f"{command} upload {space_id} . . --repo-type=space --exclude='.git/**' --exclude='.venv/**' --exclude='**/__pycache__/**' --exclude='**/*.pyc' --exclude='.pytest_cache/**' --exclude='.ruff_cache/**' --exclude='build/**' --exclude='dist/**' --exclude='tmp/**' --exclude='outputs/**' --exclude='.env*' --exclude='src/imageezgen3d.egg-info/**' --commit-message='Deploy ImageEZGen3D'",
    )
    return HfCliStatus(
        available=executable is not None,
        executable=executable,
        recommended_commands=commands,
    )
