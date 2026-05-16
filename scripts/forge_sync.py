from __future__ import annotations

import argparse
import os

from imageezgen3d.forge_sync import (
    ForgeSyncError,
    build_forgejo_remote_url,
    build_gitlab_remote_url,
    ensure_forgejo_repository,
    ensure_gitlab_repository,
    sync_git_repository,
)
from imageezgen3d.release_plan import build_release_plan
from imageezgen3d.release_config import load_release_settings


def _selected_targets(provider: str) -> tuple[str, ...]:
    if provider == "all":
        return ("gitlab", "codeberg")
    return (provider,)


def main() -> None:
    parser = argparse.ArgumentParser(description="Preview or sync GitLab and Codeberg mirrors.")
    parser.add_argument("--provider", choices=["all", "gitlab", "codeberg"], default="all")
    parser.add_argument("--execute", action="store_true")
    args = parser.parse_args()

    settings = load_release_settings()
    plan = build_release_plan(env=dict(os.environ), settings=settings)
    branch = plan.branch or settings.branches.primary_branch
    targets = {target.name: target for target in plan.targets}
    for provider in _selected_targets(args.provider):
        target = targets[provider]
        print(
            f"{provider}: action={target.action}; destination={target.destination}; "
            f"operation={target.operation}; reason={target.reason}"
        )
        if not args.execute or target.action != "push":
            continue
        if provider == "gitlab":
            token = os.environ.get("GITLAB_TOKEN", "")
            if not token:
                raise ForgeSyncError("GITLAB_TOKEN is required for GitLab mirror sync.")
            status = ensure_gitlab_repository(
                base_url=settings.forge.gitlab.base_url,
                slug=target.destination,
                token=token,
                visibility=settings.forge.gitlab.visibility,
            )
            remote_url = build_gitlab_remote_url(
                settings.forge.gitlab.base_url,
                target.destination,
                token,
            )
        else:
            token = os.environ.get("CODEBERG_TOKEN", "")
            if not token:
                raise ForgeSyncError("CODEBERG_TOKEN is required for Codeberg mirror sync.")
            status = ensure_forgejo_repository(
                base_url=settings.forge.codeberg.base_url,
                slug=target.destination,
                token=token,
                visibility=settings.forge.codeberg.visibility,
            )
            remote_url = build_forgejo_remote_url(
                settings.forge.codeberg.base_url,
                target.destination,
                status.auth_username,
                token,
            )
        print(
            f"{provider}: {'created' if status.created else 'reused'} {status.slug} -> {status.http_url}"
        )
        sync_git_repository(remote_url, branch)
        print(f"{provider}: pushed branch {branch} and tags")


if __name__ == "__main__":
    main()