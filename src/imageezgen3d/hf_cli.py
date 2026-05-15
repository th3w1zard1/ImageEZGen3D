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


def hf_cli_status(space_id: str = "YOUR_USERNAME/ImageEZGen3D") -> HfCliStatus:
    executable = shutil.which("hf")
    if executable is None:
        sibling = Path(sys.executable).with_name("hf")
        if sibling.is_file():
            executable = str(sibling)
    command = executable or "hf"
    commands = (
        f"{command} auth whoami",
        f"{command} env",
        f"{command} repos create ImageEZGen3D --repo-type space --space-sdk gradio --exist-ok",
        f"{command} download tencent/Hunyuan3D-2.1 --dry-run",
        f"{command} cache ls",
        f"{command} cache verify tencent/Hunyuan3D-2.1",
        f"{command} upload {space_id} . . --repo-type=space --exclude='/outputs/*' --exclude='/.env*' --commit-message='Deploy ImageEZGen3D'",
    )
    return HfCliStatus(
        available=executable is not None,
        executable=executable,
        recommended_commands=commands,
    )
