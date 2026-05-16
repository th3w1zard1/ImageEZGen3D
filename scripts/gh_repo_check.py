from __future__ import annotations

from imageezgen3d.gh_cli import gh_cli_status
from imageezgen3d.release_plan import build_release_plan


def main() -> None:
    plan = build_release_plan()
    release_tag = (
        plan.image.additional_tags[0]
        if plan.image.additional_tags
        else plan.image.primary_tag
    )
    status = gh_cli_status(plan.repository, release_tag=release_tag)
    print(f"repository: {plan.repository}")
    print(f"release tag: {release_tag}")
    print(f"gh available: {status.available}")
    if status.executable:
        print(f"gh executable: {status.executable}")
    print("recommended commands:")
    for command in status.recommended_commands:
        print(f"  {command}")


if __name__ == "__main__":
    main()
