from __future__ import annotations

import shutil
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class GhCliStatus:
    available: bool
    executable: str | None
    recommended_commands: tuple[str, ...]


def gh_cli_status(
    repository: str,
    *,
    release_tag: str = "",
) -> GhCliStatus:
    executable = shutil.which("gh")
    if executable is None:
        sibling = Path(sys.executable).with_name("gh")
        if sibling.is_file():
            executable = str(sibling)
    command = executable or "gh"
    repo_view = (
        f"{command} repo view {repository}" if repository else f"{command} repo view"
    )
    workflow_list = (
        f"{command} workflow list --repo {repository}"
        if repository
        else f"{command} workflow list"
    )
    commands = [
        f"{command} auth status",
        repo_view,
        workflow_list,
    ]
    if release_tag:
        repo_flag = f" --repo {repository}" if repository else ""
        commands.extend(
            (
                f"{command} release view {release_tag}{repo_flag}",
                (
                    f"{command} release create {release_tag}{repo_flag} "
                    f"--title 'Runtime artifacts {release_tag}' "
                    "--notes 'Automated runtime artifact bundle'"
                ),
                (
                    f"{command} release upload {release_tag} "
                    "dist/runtime-artifacts/runtime-artifacts.tgz"
                    f"{repo_flag} --clobber"
                ),
            )
        )
    return GhCliStatus(
        available=executable is not None,
        executable=executable,
        recommended_commands=tuple(commands),
    )
