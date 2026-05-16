from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from imageezgen3d.release_config import (
    ImageTagResolution,
    ReleaseSettings,
    RegistryTargetSettings,
    load_release_settings,
    resolve_default_branch_names,
    resolve_image_tags,
    resolve_registry_image,
    resolve_repository_ref,
    resolve_target_enablement,
    resolve_target_repo_slug,
)


def _credentials_present(name: str, env: dict[str, str]) -> bool:
    if name in {"gitlab", "gitlab-registry"}:
        return bool(env.get("GITLAB_TOKEN", "").strip())
    if name == "codeberg":
        return bool(env.get("CODEBERG_TOKEN", "").strip())
    if name == "huggingface":
        return bool(
            env.get("HF_TOKEN", "").strip()
            or env.get("HUGGINGFACE_HUB_TOKEN", "").strip()
        )
    if name == "ghcr":
        return bool(env.get("GITHUB_TOKEN", "").strip() or env.get("GH_TOKEN", "").strip())
    if name == "dockerhub":
        return bool(
            env.get("DOCKERHUB_USERNAME", "").strip()
            and env.get("DOCKERHUB_TOKEN", "").strip()
        )
    if name == "github-release":
        return bool(env.get("GITHUB_TOKEN", "").strip() or env.get("GH_TOKEN", "").strip())
    return False


@dataclass(frozen=True)
class ReleaseTargetPlan:
    name: str
    destination: str
    operation: str
    enabled: bool
    required: bool
    credentials_present: bool
    action: str
    reason: str


@dataclass(frozen=True)
class ReleasePlan:
    repository: str
    event_name: str
    branch: str
    default_branches: tuple[str, ...]
    create_missing_targets: bool
    image: ImageTagResolution
    targets: tuple[ReleaseTargetPlan, ...]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _mirror_plan(
    name: str,
    settings: ReleaseSettings,
    env: dict[str, str],
    *,
    enabled: bool,
    required: bool,
    owner: str,
    repo: str,
) -> ReleaseTargetPlan:
    credentials_present = _credentials_present(name, env)
    decision = resolve_target_enablement(
        enabled=enabled,
        required=required,
        credentials_present=credentials_present,
    )
    operation = "create-or-mirror" if settings.create_missing_targets else "mirror"
    destination = resolve_target_repo_slug(settings, owner=owner, repo=repo, env=env)
    return ReleaseTargetPlan(
        name=name,
        destination=destination,
        operation=operation,
        enabled=enabled,
        required=required,
        credentials_present=credentials_present,
        action=decision.action,
        reason=decision.reason,
    )


def _registry_plan(
    name: str,
    settings: ReleaseSettings,
    env: dict[str, str],
    registry: RegistryTargetSettings,
) -> ReleaseTargetPlan:
    credentials_present = _credentials_present(name, env)
    decision = resolve_target_enablement(
        enabled=registry.enabled,
        required=registry.required,
        credentials_present=credentials_present,
    )
    return ReleaseTargetPlan(
        name=name,
        destination=resolve_registry_image(settings, registry, env),
        operation="push-image",
        enabled=registry.enabled,
        required=registry.required,
        credentials_present=credentials_present,
        action=decision.action,
        reason=decision.reason,
    )


def _asset_plan(
    name: str,
    *,
    enabled: bool,
    operation: str,
) -> ReleaseTargetPlan:
    return ReleaseTargetPlan(
        name=name,
        destination=name,
        operation=operation,
        enabled=enabled,
        required=False,
        credentials_present=True,
        action="render" if enabled else "skip",
        reason="artifact enabled" if enabled else "artifact disabled",
    )


def _huggingface_plan(
    settings: ReleaseSettings,
    env: dict[str, str],
) -> ReleaseTargetPlan:
    credentials_present = _credentials_present("huggingface", env)
    decision = resolve_target_enablement(
        enabled=settings.forge.huggingface.enabled,
        required=settings.forge.huggingface.required,
        credentials_present=credentials_present,
    )
    return ReleaseTargetPlan(
        name="huggingface",
        destination=resolve_target_repo_slug(
            settings,
            owner=settings.forge.huggingface.owner,
            repo=settings.forge.huggingface.repo,
            env=env,
        ),
        operation="create-or-upload" if settings.create_missing_targets else "upload",
        enabled=settings.forge.huggingface.enabled,
        required=settings.forge.huggingface.required,
        credentials_present=credentials_present,
        action=decision.action,
        reason=decision.reason,
    )


def _github_release_plan(
    settings: ReleaseSettings,
    env: dict[str, str],
) -> ReleaseTargetPlan:
    credentials_present = _credentials_present("github-release", env)
    decision = resolve_target_enablement(
        enabled=settings.artifacts.attach_to_github_release,
        required=False,
        credentials_present=credentials_present,
    )
    return ReleaseTargetPlan(
        name="github-release",
        destination=resolve_repository_ref(settings, env).slug,
        operation="attach-assets",
        enabled=settings.artifacts.attach_to_github_release,
        required=False,
        credentials_present=credentials_present,
        action=decision.action,
        reason=decision.reason,
    )


def build_release_plan(
    *,
    env: dict[str, str] | None = None,
    settings: ReleaseSettings | None = None,
    image_tag: str = "",
) -> ReleasePlan:
    current = dict(env or {})
    active_settings = settings or load_release_settings()
    repository = resolve_repository_ref(active_settings, current)
    image = resolve_image_tags(active_settings, env=current, image_tag=image_tag)
    targets = (
        _mirror_plan(
            "gitlab",
            active_settings,
            current,
            enabled=active_settings.forge.gitlab.enabled,
            required=active_settings.forge.gitlab.required,
            owner=active_settings.forge.gitlab.owner,
            repo=active_settings.forge.gitlab.repo,
        ),
        _mirror_plan(
            "codeberg",
            active_settings,
            current,
            enabled=active_settings.forge.codeberg.enabled,
            required=active_settings.forge.codeberg.required,
            owner=active_settings.forge.codeberg.owner,
            repo=active_settings.forge.codeberg.repo,
        ),
        _huggingface_plan(active_settings, current),
        _registry_plan("ghcr", active_settings, current, active_settings.registry.ghcr),
        _registry_plan(
            "dockerhub",
            active_settings,
            current,
            active_settings.registry.dockerhub,
        ),
        _registry_plan(
            "gitlab-registry",
            active_settings,
            current,
            active_settings.registry.gitlab,
        ),
        _asset_plan(
            "helm",
            enabled=active_settings.artifacts.helm_enabled,
            operation="render-chart",
        ),
        _asset_plan(
            "kubernetes",
            enabled=active_settings.artifacts.kubernetes_enabled,
            operation="render-manifests",
        ),
        _asset_plan(
            "nomad",
            enabled=active_settings.artifacts.nomad_enabled,
            operation="render-job",
        ),
        _asset_plan(
            "podman",
            enabled=active_settings.artifacts.podman_enabled,
            operation="render-assets",
        ),
        _github_release_plan(active_settings, current),
    )
    return ReleasePlan(
        repository=repository.slug,
        event_name=current.get("GITHUB_EVENT_NAME", "workflow_dispatch"),
        branch=image.branch,
        default_branches=resolve_default_branch_names(active_settings),
        create_missing_targets=active_settings.create_missing_targets,
        image=image,
        targets=targets,
    )


def format_release_plan(plan: ReleasePlan) -> tuple[str, ...]:
    lines = [
        f"repository: {plan.repository}",
        f"event: {plan.event_name}",
        f"branch: {plan.branch or '<none>'}",
        f"default branches: {', '.join(plan.default_branches)}",
        f"create missing targets: {plan.create_missing_targets}",
        f"image tag: {plan.image.primary_tag}",
        f"image additional tags: {', '.join(plan.image.additional_tags) or '<none>'}",
        f"image tag source: {plan.image.source}",
        f"publish latest: {plan.image.publish_latest}",
        "targets:",
    ]
    for target in plan.targets:
        lines.append(
            "  - "
            f"{target.name}: action={target.action}; operation={target.operation}; "
            f"destination={target.destination or '<none>'}; reason={target.reason}"
        )
    return tuple(lines)