from __future__ import annotations

from imageezgen3d.release_config import load_release_settings, resolve_target_repo_slug
from imageezgen3d.hf_cli import hf_cli_status


def main() -> None:
    settings = load_release_settings()
    target = resolve_target_repo_slug(
        settings,
        owner=settings.forge.huggingface.owner,
        repo=settings.forge.huggingface.repo,
    )
    status = hf_cli_status(target, space_sdk=settings.forge.huggingface.space_sdk)
    print(f"space id: {target}")
    print(f"hf available: {status.available}")
    if status.executable:
        print(f"hf executable: {status.executable}")
    print("recommended commands:")
    for command in status.recommended_commands:
        print(f"  {command}")


if __name__ == "__main__":
    main()
