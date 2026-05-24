from __future__ import annotations

import argparse
import shlex
import subprocess
import tempfile
from pathlib import Path

from imageezgen3d.hf_cli import deploy_commit_message, hf_cli_status, stage_space_payload
from imageezgen3d.release_config import load_release_settings, resolve_target_repo_slug


_SPACE_DELETE_PATTERNS = (
    ".dockerignore",
    ".firecrawl/**",
    ".gitattributes",
    ".github/**",
    ".history/**",
    ".mypy_cache/**",
    ".pytest_cache/**",
    ".ruff_cache/**",
    ".vscode/**",
    ".venv/**",
    "Dockerfile",
    "deploy/**",
    "docs/**",
    "outputs/**",
    "scripts/**",
    "tests/**",
    "tmp/**",
    "build/**",
    "dist/**",
    "src/imageezgen3d.egg-info/**",
)


def _commands_for_sync(
    space_id: str,
    *,
    space_sdk: str,
    payload_dir: Path | None = None,
    commit_message: str = "Deploy ImageEZGen3D",
) -> tuple[str, ...]:
    status = hf_cli_status(space_id, space_sdk=space_sdk)
    command = status.executable or "hf"
    upload_command = status.recommended_commands[-1]
    if payload_dir is not None:
        delete_args = " ".join(
            f"--delete={shlex.quote(pattern)}" for pattern in _SPACE_DELETE_PATTERNS
        )
        upload_command = (
            f"{command} upload {space_id} {shlex.quote(str(payload_dir))} . "
            f"--repo-type=space {delete_args} "
            f"--commit-message={shlex.quote(commit_message)}"
        )
    return (
        status.recommended_commands[0],
        status.recommended_commands[1],
        status.recommended_commands[2],
        upload_command,
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Preview or sync the configured Hugging Face Space."
    )
    parser.add_argument("--execute", action="store_true")
    args = parser.parse_args()

    settings = load_release_settings()
    target = resolve_target_repo_slug(
        settings,
        owner=settings.forge.huggingface.owner,
        repo=settings.forge.huggingface.repo,
    )
    commit_message = deploy_commit_message()
    if not args.execute:
        commands = _commands_for_sync(
            target,
            space_sdk=settings.forge.huggingface.space_sdk,
            commit_message=commit_message,
        )
        print(f"space id: {target}")
        print(f"space sdk: {settings.forge.huggingface.space_sdk}")
        print(
            "note: --execute stages a minimal Space payload before calling hf upload."
        )
        for command in commands:
            print(command)
        return

    with tempfile.TemporaryDirectory(prefix="imageezgen3d-hf-space-") as directory:
        payload_dir = stage_space_payload(Path(directory))
        commands = _commands_for_sync(
            target,
            space_sdk=settings.forge.huggingface.space_sdk,
            payload_dir=payload_dir,
            commit_message=commit_message,
        )
        print(f"space id: {target}")
        print(f"space sdk: {settings.forge.huggingface.space_sdk}")
        print(f"staged payload: {payload_dir}")
        for command in commands:
            print(command)
        for command in commands:
            subprocess.run(command, shell=True, check=True)


if __name__ == "__main__":
    main()
