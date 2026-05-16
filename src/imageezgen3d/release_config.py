from __future__ import annotations

import os
import re
from dataclasses import dataclass, field
from pathlib import Path

from imageezgen3d.config import (
    _as_bool,
    _bool_value,
    _env_bool,
    _env_str,
    _load_env_file,
    _load_pyproject,
    _section,
    _str_value,
    _str_tuple_value,
)


def _env_csv(name: str, current: tuple[str, ...]) -> tuple[str, ...]:
    if name not in os.environ:
        return current
    return _csv_tuple(os.environ[name], current)


def _csv_tuple(value: object, default: tuple[str, ...]) -> tuple[str, ...]:
    if isinstance(value, list | tuple):
        return tuple(str(item) for item in value if str(item).strip())
    if isinstance(value, str):
        items = tuple(part.strip() for part in value.split(",") if part.strip())
        return items or default
    return default


def _slugify_tag(value: str, *, default: str = "latest") -> str:
    normalized = re.sub(r"[^A-Za-z0-9._-]+", "-", value.strip()).strip("-._")
    return normalized.lower() or default


def _unique_items(*values: str) -> tuple[str, ...]:
    seen: list[str] = []
    for value in values:
        cleaned = value.strip()
        if cleaned and cleaned not in seen:
            seen.append(cleaned)
    return tuple(seen)


def _ref_name(env: dict[str, str]) -> str:
    if env.get("GITHUB_HEAD_REF"):
        return str(env["GITHUB_HEAD_REF"])
    if env.get("GITHUB_REF_NAME"):
        return str(env["GITHUB_REF_NAME"])
    ref = env.get("GITHUB_REF", "")
    for prefix in ("refs/heads/", "refs/tags/"):
        if ref.startswith(prefix):
            return ref[len(prefix) :]
    return ref


def _pull_request_number(env: dict[str, str]) -> str | None:
    for key in ("GITHUB_EVENT_PULL_REQUEST_NUMBER", "PR_NUMBER"):
        if env.get(key):
            return str(env[key])
    ref = env.get("GITHUB_REF", "")
    match = re.match(r"refs/pull/(\d+)/", ref)
    if match:
        return match.group(1)
    return None


def _short_sha(env: dict[str, str]) -> str:
    sha = env.get("GITHUB_SHA", "")
    return sha[:7] if sha else "unknown"


def _has_values(*values: str) -> bool:
    return all(value.strip() for value in values)


@dataclass(frozen=True)
class RepositorySettings:
    owner: str = ""
    repo: str = ""


@dataclass(frozen=True)
class BranchSettings:
    primary_branch: str = "main"
    fallback_branches: tuple[str, ...] = ("master",)
    publish_latest_branches: tuple[str, ...] = ("main", "master")


@dataclass(frozen=True)
class TagSettings:
    default_image_tag: str = "latest"
    immutable_tag_prefix: str = "sha"
    pr_tag_prefix: str = "pr"
    publish_latest_by_default: bool = True


@dataclass(frozen=True)
class MirrorTargetSettings:
    enabled: bool = True
    required: bool = False
    owner: str = ""
    repo: str = ""
    visibility: str = "public"
    base_url: str = ""


@dataclass(frozen=True)
class HuggingFaceSettings:
    enabled: bool = True
    required: bool = False
    owner: str = ""
    repo: str = "ImageEZGen3D"
    repo_type: str = "space"
    space_sdk: str = "gradio"


@dataclass(frozen=True)
class RegistryTargetSettings:
    enabled: bool = False
    required: bool = False
    namespace: str = ""
    image: str = ""
    registry: str = ""


@dataclass(frozen=True)
class ArtifactSettings:
    helm_enabled: bool = True
    kubernetes_enabled: bool = True
    nomad_enabled: bool = True
    podman_enabled: bool = True
    attach_to_github_release: bool = True


@dataclass(frozen=True)
class ForgeSettings:
    gitlab: MirrorTargetSettings = field(default_factory=MirrorTargetSettings)
    codeberg: MirrorTargetSettings = field(default_factory=MirrorTargetSettings)
    huggingface: HuggingFaceSettings = field(default_factory=HuggingFaceSettings)


@dataclass(frozen=True)
class RegistrySettings:
    ghcr: RegistryTargetSettings = field(
        default_factory=lambda: RegistryTargetSettings(enabled=True, registry="ghcr.io")
    )
    dockerhub: RegistryTargetSettings = field(
        default_factory=lambda: RegistryTargetSettings(enabled=False, registry="docker.io")
    )
    gitlab: RegistryTargetSettings = field(
        default_factory=lambda: RegistryTargetSettings(enabled=False, registry="registry.gitlab.com")
    )


@dataclass(frozen=True)
class ReleaseSettings:
    repository: RepositorySettings = field(default_factory=RepositorySettings)
    branches: BranchSettings = field(default_factory=BranchSettings)
    tags: TagSettings = field(default_factory=TagSettings)
    create_missing_targets: bool = True
    forge: ForgeSettings = field(default_factory=ForgeSettings)
    registry: RegistrySettings = field(default_factory=RegistrySettings)
    artifacts: ArtifactSettings = field(default_factory=ArtifactSettings)


@dataclass(frozen=True)
class RepositoryRef:
    owner: str
    repo: str

    @property
    def slug(self) -> str:
        return f"{self.owner}/{self.repo}" if _has_values(self.owner, self.repo) else ""


@dataclass(frozen=True)
class TargetDecision:
    action: str
    reason: str


@dataclass(frozen=True)
class ImageTagResolution:
    primary_tag: str
    additional_tags: tuple[str, ...]
    source: str
    branch: str
    event_name: str
    is_default_branch: bool
    publish_latest: bool

    @property
    def all_tags(self) -> tuple[str, ...]:
        return _unique_items(self.primary_tag, *self.additional_tags)


def load_release_settings(path: str | Path | None = None) -> ReleaseSettings:
    if path is None:
        _load_env_file()
        config_path = Path(os.environ.get("IMAGEEZ_CONFIG", "pyproject.toml"))
    else:
        config_path = Path(path)
    root = _load_pyproject(config_path)
    raw = _section(root, "release")
    repository_raw = _section(raw, "repository")
    branches_raw = _section(raw, "branches")
    tags_raw = _section(raw, "tags")
    forge_raw = _section(raw, "forge")
    registry_raw = _section(raw, "registry")
    artifacts_raw = _section(raw, "artifacts")
    gitlab_raw = _section(forge_raw, "gitlab")
    codeberg_raw = _section(forge_raw, "codeberg")
    huggingface_raw = _section(forge_raw, "huggingface")
    ghcr_raw = _section(registry_raw, "ghcr")
    dockerhub_raw = _section(registry_raw, "dockerhub")
    gitlab_registry_raw = _section(registry_raw, "gitlab")

    return ReleaseSettings(
        repository=RepositorySettings(
            owner=_env_str(
                "IMAGEEZ_RELEASE_OWNER",
                _str_value(repository_raw, "owner", RepositorySettings.owner),
            ),
            repo=_env_str(
                "IMAGEEZ_RELEASE_REPO",
                _str_value(repository_raw, "repo", RepositorySettings.repo),
            ),
        ),
        branches=BranchSettings(
            primary_branch=_env_str(
                "IMAGEEZ_RELEASE_PRIMARY_BRANCH",
                _str_value(branches_raw, "primary_branch", BranchSettings.primary_branch),
            ),
            fallback_branches=_env_csv(
                "IMAGEEZ_RELEASE_FALLBACK_BRANCHES",
                _csv_tuple(
                    branches_raw.get("fallback_branches"),
                    BranchSettings.fallback_branches,
                ),
            ),
            publish_latest_branches=_env_csv(
                "IMAGEEZ_RELEASE_PUBLISH_LATEST_BRANCHES",
                _csv_tuple(
                    branches_raw.get("publish_latest_branches"),
                    BranchSettings.publish_latest_branches,
                ),
            ),
        ),
        tags=TagSettings(
            default_image_tag=_env_str(
                "IMAGEEZ_RELEASE_DEFAULT_IMAGE_TAG",
                _str_value(tags_raw, "default_image_tag", TagSettings.default_image_tag),
            ),
            immutable_tag_prefix=_env_str(
                "IMAGEEZ_RELEASE_IMMUTABLE_TAG_PREFIX",
                _str_value(
                    tags_raw,
                    "immutable_tag_prefix",
                    TagSettings.immutable_tag_prefix,
                ),
            ),
            pr_tag_prefix=_env_str(
                "IMAGEEZ_RELEASE_PR_TAG_PREFIX",
                _str_value(tags_raw, "pr_tag_prefix", TagSettings.pr_tag_prefix),
            ),
            publish_latest_by_default=_env_bool(
                "IMAGEEZ_RELEASE_PUBLISH_LATEST_BY_DEFAULT",
                _bool_value(
                    tags_raw,
                    "publish_latest_by_default",
                    TagSettings.publish_latest_by_default,
                ),
            ),
        ),
        create_missing_targets=_env_bool(
            "IMAGEEZ_RELEASE_CREATE_MISSING_TARGETS",
            _bool_value(raw, "create_missing_targets", True),
        ),
        forge=ForgeSettings(
            gitlab=MirrorTargetSettings(
                enabled=_env_bool(
                    "IMAGEEZ_RELEASE_GITLAB_ENABLED",
                    _bool_value(gitlab_raw, "enabled", MirrorTargetSettings.enabled),
                ),
                required=_env_bool(
                    "IMAGEEZ_RELEASE_GITLAB_REQUIRED",
                    _bool_value(gitlab_raw, "required", MirrorTargetSettings.required),
                ),
                owner=_env_str(
                    "IMAGEEZ_RELEASE_GITLAB_OWNER",
                    _str_value(gitlab_raw, "owner", MirrorTargetSettings.owner),
                ),
                repo=_env_str(
                    "IMAGEEZ_RELEASE_GITLAB_REPO",
                    _str_value(gitlab_raw, "repo", MirrorTargetSettings.repo),
                ),
                visibility=_env_str(
                    "IMAGEEZ_RELEASE_GITLAB_VISIBILITY",
                    _str_value(gitlab_raw, "visibility", MirrorTargetSettings.visibility),
                ),
                base_url=_env_str(
                    "IMAGEEZ_RELEASE_GITLAB_BASE_URL",
                    _str_value(gitlab_raw, "base_url", "https://gitlab.com"),
                ),
            ),
            codeberg=MirrorTargetSettings(
                enabled=_env_bool(
                    "IMAGEEZ_RELEASE_CODEBERG_ENABLED",
                    _bool_value(codeberg_raw, "enabled", MirrorTargetSettings.enabled),
                ),
                required=_env_bool(
                    "IMAGEEZ_RELEASE_CODEBERG_REQUIRED",
                    _bool_value(codeberg_raw, "required", MirrorTargetSettings.required),
                ),
                owner=_env_str(
                    "IMAGEEZ_RELEASE_CODEBERG_OWNER",
                    _str_value(codeberg_raw, "owner", MirrorTargetSettings.owner),
                ),
                repo=_env_str(
                    "IMAGEEZ_RELEASE_CODEBERG_REPO",
                    _str_value(codeberg_raw, "repo", MirrorTargetSettings.repo),
                ),
                visibility=_env_str(
                    "IMAGEEZ_RELEASE_CODEBERG_VISIBILITY",
                    _str_value(codeberg_raw, "visibility", MirrorTargetSettings.visibility),
                ),
                base_url=_env_str(
                    "IMAGEEZ_RELEASE_CODEBERG_BASE_URL",
                    _str_value(codeberg_raw, "base_url", "https://codeberg.org"),
                ),
            ),
            huggingface=HuggingFaceSettings(
                enabled=_env_bool(
                    "IMAGEEZ_RELEASE_HF_ENABLED",
                    _bool_value(huggingface_raw, "enabled", HuggingFaceSettings.enabled),
                ),
                required=_env_bool(
                    "IMAGEEZ_RELEASE_HF_REQUIRED",
                    _bool_value(huggingface_raw, "required", HuggingFaceSettings.required),
                ),
                owner=_env_str(
                    "IMAGEEZ_RELEASE_HF_OWNER",
                    _str_value(huggingface_raw, "owner", HuggingFaceSettings.owner),
                ),
                repo=_env_str(
                    "IMAGEEZ_RELEASE_HF_REPO",
                    _str_value(huggingface_raw, "repo", HuggingFaceSettings.repo),
                ),
                repo_type=_env_str(
                    "IMAGEEZ_RELEASE_HF_REPO_TYPE",
                    _str_value(
                        huggingface_raw,
                        "repo_type",
                        HuggingFaceSettings.repo_type,
                    ),
                ),
                space_sdk=_env_str(
                    "IMAGEEZ_RELEASE_HF_SPACE_SDK",
                    _str_value(
                        huggingface_raw,
                        "space_sdk",
                        HuggingFaceSettings.space_sdk,
                    ),
                ),
            ),
        ),
        registry=RegistrySettings(
            ghcr=RegistryTargetSettings(
                enabled=_env_bool(
                    "IMAGEEZ_RELEASE_GHCR_ENABLED",
                    _bool_value(ghcr_raw, "enabled", True),
                ),
                required=_env_bool(
                    "IMAGEEZ_RELEASE_GHCR_REQUIRED",
                    _bool_value(ghcr_raw, "required", False),
                ),
                namespace=_env_str(
                    "IMAGEEZ_RELEASE_GHCR_NAMESPACE",
                    _str_value(ghcr_raw, "namespace", ""),
                ),
                image=_env_str(
                    "IMAGEEZ_RELEASE_GHCR_IMAGE",
                    _str_value(ghcr_raw, "image", ""),
                ),
                registry=_env_str(
                    "IMAGEEZ_RELEASE_GHCR_REGISTRY",
                    _str_value(ghcr_raw, "registry", "ghcr.io"),
                ),
            ),
            dockerhub=RegistryTargetSettings(
                enabled=_env_bool(
                    "IMAGEEZ_RELEASE_DOCKERHUB_ENABLED",
                    _bool_value(dockerhub_raw, "enabled", False),
                ),
                required=_env_bool(
                    "IMAGEEZ_RELEASE_DOCKERHUB_REQUIRED",
                    _bool_value(dockerhub_raw, "required", False),
                ),
                namespace=_env_str(
                    "IMAGEEZ_RELEASE_DOCKERHUB_NAMESPACE",
                    _str_value(dockerhub_raw, "namespace", ""),
                ),
                image=_env_str(
                    "IMAGEEZ_RELEASE_DOCKERHUB_IMAGE",
                    _str_value(dockerhub_raw, "image", ""),
                ),
                registry=_env_str(
                    "IMAGEEZ_RELEASE_DOCKERHUB_REGISTRY",
                    _str_value(dockerhub_raw, "registry", "docker.io"),
                ),
            ),
            gitlab=RegistryTargetSettings(
                enabled=_env_bool(
                    "IMAGEEZ_RELEASE_GITLAB_REGISTRY_ENABLED",
                    _bool_value(gitlab_registry_raw, "enabled", False),
                ),
                required=_env_bool(
                    "IMAGEEZ_RELEASE_GITLAB_REGISTRY_REQUIRED",
                    _bool_value(gitlab_registry_raw, "required", False),
                ),
                namespace=_env_str(
                    "IMAGEEZ_RELEASE_GITLAB_REGISTRY_NAMESPACE",
                    _str_value(gitlab_registry_raw, "namespace", ""),
                ),
                image=_env_str(
                    "IMAGEEZ_RELEASE_GITLAB_REGISTRY_IMAGE",
                    _str_value(gitlab_registry_raw, "image", ""),
                ),
                registry=_env_str(
                    "IMAGEEZ_RELEASE_GITLAB_REGISTRY",
                    _str_value(gitlab_registry_raw, "registry", "registry.gitlab.com"),
                ),
            ),
        ),
        artifacts=ArtifactSettings(
            helm_enabled=_env_bool(
                "IMAGEEZ_RELEASE_HELM_ENABLED",
                _bool_value(artifacts_raw, "helm_enabled", ArtifactSettings.helm_enabled),
            ),
            kubernetes_enabled=_env_bool(
                "IMAGEEZ_RELEASE_KUBERNETES_ENABLED",
                _bool_value(
                    artifacts_raw,
                    "kubernetes_enabled",
                    ArtifactSettings.kubernetes_enabled,
                ),
            ),
            nomad_enabled=_env_bool(
                "IMAGEEZ_RELEASE_NOMAD_ENABLED",
                _bool_value(artifacts_raw, "nomad_enabled", ArtifactSettings.nomad_enabled),
            ),
            podman_enabled=_env_bool(
                "IMAGEEZ_RELEASE_PODMAN_ENABLED",
                _bool_value(
                    artifacts_raw,
                    "podman_enabled",
                    ArtifactSettings.podman_enabled,
                ),
            ),
            attach_to_github_release=_env_bool(
                "IMAGEEZ_RELEASE_ATTACH_TO_GITHUB_RELEASE",
                _bool_value(
                    artifacts_raw,
                    "attach_to_github_release",
                    ArtifactSettings.attach_to_github_release,
                ),
            ),
        ),
    )


def resolve_default_branch_names(settings: ReleaseSettings) -> tuple[str, ...]:
    return _unique_items(
        settings.branches.primary_branch,
        *settings.branches.fallback_branches,
    )


def resolve_repository_ref(
    settings: ReleaseSettings, env: dict[str, str] | None = None
) -> RepositoryRef:
    current = env or dict(os.environ)
    repository = current.get("GITHUB_REPOSITORY", "")
    owner = settings.repository.owner.strip()
    repo = settings.repository.repo.strip()
    if repository and "/" in repository:
        current_owner, current_repo = repository.split("/", 1)
        owner = owner or current_owner
        repo = repo or current_repo
    owner = owner or current.get("GITHUB_REPOSITORY_OWNER", "")
    repo = repo or Path.cwd().name
    return RepositoryRef(owner=owner, repo=repo)


def resolve_target_repo_slug(
    settings: ReleaseSettings,
    *,
    owner: str = "",
    repo: str = "",
    env: dict[str, str] | None = None,
) -> str:
    current = resolve_repository_ref(settings, env)
    resolved_owner = owner.strip() or current.owner
    resolved_repo = repo.strip() or current.repo
    if not _has_values(resolved_owner, resolved_repo):
        return ""
    return f"{resolved_owner}/{resolved_repo}"


def resolve_registry_image(
    settings: ReleaseSettings,
    registry: RegistryTargetSettings,
    env: dict[str, str] | None = None,
) -> str:
    current = resolve_repository_ref(settings, env)
    namespace = registry.namespace.strip() or current.owner.lower()
    image = registry.image.strip() or current.repo.lower()
    if not _has_values(registry.registry, namespace, image):
        return ""
    return f"{registry.registry}/{namespace}/{image}"


def resolve_image_tags(
    settings: ReleaseSettings,
    *,
    env: dict[str, str] | None = None,
    image_tag: str = "",
    publish_latest: bool | None = None,
) -> ImageTagResolution:
    current = env or dict(os.environ)
    event_name = current.get("GITHUB_EVENT_NAME", "workflow_dispatch")
    branch = _ref_name(current)
    default_branches = resolve_default_branch_names(settings)
    publish_latest_branches = _unique_items(*settings.branches.publish_latest_branches)
    is_default_branch = branch in default_branches
    requested_tag = image_tag.strip() or current.get("IMAGEEZ_RELEASE_IMAGE_TAG", "").strip()
    sha_tag = _slugify_tag(
        f"{settings.tags.immutable_tag_prefix}-{_short_sha(current)}",
        default=settings.tags.default_image_tag,
    )
    source = "default"
    if requested_tag:
        primary_tag = _slugify_tag(requested_tag, default=settings.tags.default_image_tag)
        source = "input"
    elif event_name == "pull_request":
        number = _pull_request_number(current)
        pr_identifier = number or _short_sha(current)
        primary_tag = _slugify_tag(
            f"{settings.tags.pr_tag_prefix}-{pr_identifier}",
            default=settings.tags.default_image_tag,
        )
        source = "pull_request"
    elif is_default_branch:
        primary_tag = _slugify_tag(
            settings.tags.default_image_tag,
            default=settings.tags.default_image_tag,
        )
        source = "default_branch"
    elif branch:
        primary_tag = _slugify_tag(branch, default=settings.tags.default_image_tag)
        source = "branch"
    else:
        primary_tag = _slugify_tag(
            settings.tags.default_image_tag,
            default=settings.tags.default_image_tag,
        )
    should_publish_latest = (
        settings.tags.publish_latest_by_default
        and event_name != "pull_request"
        and branch in publish_latest_branches
        and primary_tag == _slugify_tag(settings.tags.default_image_tag)
    )
    if publish_latest is not None:
        should_publish_latest = publish_latest
    additional_tags = tuple(
        tag
        for tag in _unique_items(sha_tag)
        if tag and tag != primary_tag
    )
    return ImageTagResolution(
        primary_tag=primary_tag,
        additional_tags=additional_tags,
        source=source,
        branch=branch,
        event_name=event_name,
        is_default_branch=is_default_branch,
        publish_latest=should_publish_latest,
    )


def resolve_target_enablement(
    *,
    enabled: bool,
    required: bool,
    credentials_present: bool,
    force: bool = False,
) -> TargetDecision:
    if force:
        if credentials_present:
            return TargetDecision(action="push", reason="target forced on")
        return TargetDecision(action="fail", reason="target forced on but credentials are missing")
    if not enabled:
        return TargetDecision(action="skip", reason="target disabled")
    if credentials_present:
        return TargetDecision(action="push", reason="target enabled and credentials available")
    if required:
        return TargetDecision(action="fail", reason="required target is missing credentials")
    return TargetDecision(action="skip", reason="target enabled but credentials are missing")


def summarize_skipped_target_reason(
    *,
    enabled: bool,
    credentials_present: bool,
    required: bool,
    force: bool = False,
) -> str:
    return resolve_target_enablement(
        enabled=enabled,
        required=required,
        credentials_present=credentials_present,
        force=force,
    ).reason