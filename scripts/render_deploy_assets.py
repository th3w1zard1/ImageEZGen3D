from __future__ import annotations

import argparse
import json

from imageezgen3d.deploy_assets import render_deploy_assets


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Render deploy assets for a specific image reference."
    )
    parser.add_argument("--image", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--app-name", default="imageezgen3d")
    parser.add_argument("--container-port", type=int, default=7865)
    parser.add_argument("--service-port", type=int, default=80)
    args = parser.parse_args()

    bundle = render_deploy_assets(
        args.image,
        args.output_dir,
        app_name=args.app_name,
        container_port=args.container_port,
        service_port=args.service_port,
    )
    print(
        json.dumps(
            {
                "image_reference": bundle.image_reference,
                "output_dir": str(bundle.output_dir),
                "helm_chart_dir": str(bundle.helm_chart_dir),
                "kubernetes_dir": str(bundle.kubernetes_dir),
                "nomad_dir": str(bundle.nomad_dir),
                "podman_dir": str(bundle.podman_dir),
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
