from __future__ import annotations

import argparse
import subprocess

from imageezgen3d.hf_cli import hf_cli_status
from imageezgen3d.release_config import load_release_settings, resolve_target_repo_slug


def _commands_for_sync(space_id: str, *, space_sdk: str) -> tuple[str, ...]:
    status = hf_cli_status(space_id, space_sdk=space_sdk)
    return (
        status.recommended_commands[0],
        status.recommended_commands[1],
        status.recommended_commands[2],
        status.recommended_commands[-1],
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Preview or sync the configured Hugging Face Space.")
    parser.add_argument("--execute", action="store_true")
    args = parser.parse_args()

    settings = load_release_settings()
    target = resolve_target_repo_slug(
        settings,
        owner=settings.forge.huggingface.owner,
        repo=settings.forge.huggingface.repo,
    )
    commands = _commands_for_sync(target, space_sdk=settings.forge.huggingface.space_sdk)
    print(f"space id: {target}")
    print(f"space sdk: {settings.forge.huggingface.space_sdk}")
    for command in commands:
        print(command)
    if not args.execute:
        return
    for command in commands:
        subprocess.run(command, shell=True, check=True)


if __name__ == "__main__":
    main()