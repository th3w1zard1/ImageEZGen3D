from __future__ import annotations

import argparse
import os

from imageezgen3d.release_plan import build_release_plan


def _normalize_target_name(name: str) -> str:
    return name.replace("-", "_")


def main() -> None:
    parser = argparse.ArgumentParser(description="Emit release workflow outputs.")
    parser.add_argument("--image-tag", default="")
    args = parser.parse_args()

    plan = build_release_plan(env=dict(os.environ), image_tag=args.image_tag)
    targets = {target.name: target for target in plan.targets}
    registry_candidates = [
        targets.get("ghcr"),
        targets.get("dockerhub"),
        targets.get("gitlab-registry"),
    ]
    default_registry = next(
        (target for target in registry_candidates if target and target.destination),
        None,
    )
    release_tag = (
        plan.image.additional_tags[0]
        if plan.image.additional_tags
        else plan.image.primary_tag
    )
    output_lines = [
        f"repository={plan.repository}",
        f"event_name={plan.event_name}",
        f"branch={plan.branch}",
        f"primary_tag={plan.image.primary_tag}",
        f"additional_tags={','.join(plan.image.additional_tags)}",
        f"release_tag={release_tag}",
        f"publish_latest={str(plan.image.publish_latest).lower()}",
        f"default_registry_destination={default_registry.destination if default_registry else ''}",
        (
            f"default_image_reference={default_registry.destination}:{plan.image.primary_tag}"
            if default_registry and default_registry.destination
            else "default_image_reference="
        ),
    ]
    if (
        default_registry
        and default_registry.name == "ghcr"
        and default_registry.destination
    ):
        parts = default_registry.destination.split("/")
        if len(parts) >= 2:
            output_lines.append(
                f"ghcr_chart_registry=oci://{parts[0]}/{parts[1]}/charts"
            )
    for target in plan.targets:
        prefix = _normalize_target_name(target.name)
        output_lines.append(f"{prefix}_action={target.action}")
        output_lines.append(f"{prefix}_destination={target.destination}")
        output_lines.append(f"{prefix}_operation={target.operation}")
    if os.environ.get("GITHUB_OUTPUT"):
        with open(os.environ["GITHUB_OUTPUT"], "a", encoding="utf-8") as handle:
            for line in output_lines:
                handle.write(line + "\n")
        return
    for line in output_lines:
        print(line)


if __name__ == "__main__":
    main()
