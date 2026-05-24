from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from imageezgen3d import __version__


def _workspace_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _split_image_reference(image_reference: str) -> tuple[str, str]:
    last_segment = image_reference.rsplit("/", 1)[-1]
    if ":" not in last_segment:
        return image_reference, "latest"
    repository, tag = image_reference.rsplit(":", 1)
    return repository, tag


def _replace_tokens(content: str, replacements: dict[str, str]) -> str:
    rendered = content
    for key, value in replacements.items():
        rendered = rendered.replace(key, value)
    return rendered


def _render_tree(
    source_root: Path, destination_root: Path, replacements: dict[str, str]
) -> None:
    for source_path in source_root.rglob("*.tmpl"):
        relative_path = source_path.relative_to(source_root)
        destination_path = destination_root / relative_path
        target_name = destination_path.name[:-5]
        target_path = destination_path.with_name(target_name)
        target_path.parent.mkdir(parents=True, exist_ok=True)
        rendered = _replace_tokens(
            source_path.read_text(encoding="utf-8"), replacements
        )
        target_path.write_text(rendered, encoding="utf-8")


@dataclass(frozen=True)
class DeployAssetBundle:
    image_reference: str
    output_dir: Path
    helm_chart_dir: Path
    kubernetes_dir: Path
    nomad_dir: Path
    podman_dir: Path


def render_deploy_assets(
    image_reference: str,
    output_dir: str | Path,
    *,
    app_name: str = "imageezgen3d",
    container_port: int = 7865,
    service_port: int = 80,
) -> DeployAssetBundle:
    repository, tag = _split_image_reference(image_reference)
    root = _workspace_root() / "deploy"
    destination_root = Path(output_dir)
    helm_chart_dir = destination_root / "helm" / app_name
    kubernetes_dir = destination_root / "kubernetes"
    nomad_dir = destination_root / "nomad"
    podman_dir = destination_root / "podman"
    replacements = {
        "__APP_NAME__": app_name,
        "__CHART_VERSION__": __version__,
        "__CHART_APP_VERSION__": __version__,
        "__IMAGE_REFERENCE__": image_reference,
        "__IMAGE_REPOSITORY__": repository,
        "__IMAGE_TAG__": tag,
        "__CONTAINER_PORT__": str(container_port),
        "__SERVICE_PORT__": str(service_port),
    }
    _render_tree(root / "helm", helm_chart_dir.parent, replacements)
    _render_tree(root / "kubernetes", kubernetes_dir, replacements)
    _render_tree(root / "nomad", nomad_dir, replacements)
    _render_tree(root / "podman", podman_dir, replacements)
    return DeployAssetBundle(
        image_reference=image_reference,
        output_dir=destination_root,
        helm_chart_dir=helm_chart_dir,
        kubernetes_dir=kubernetes_dir,
        nomad_dir=nomad_dir,
        podman_dir=podman_dir,
    )
