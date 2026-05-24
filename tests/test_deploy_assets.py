from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from imageezgen3d.deploy_assets import render_deploy_assets


class DeployAssetTests(unittest.TestCase):
    def test_render_deploy_assets_injects_same_image_reference(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            bundle = render_deploy_assets(
                "ghcr.io/th3w1zard1/imageezgen3d:latest",
                directory,
            )
            deployment = (bundle.kubernetes_dir / "deployment.yaml").read_text(encoding="utf-8")
            job = (bundle.nomad_dir / "imageezgen3d.nomad.hcl").read_text(encoding="utf-8")
            podman = (bundle.podman_dir / "imageezgen3d.container").read_text(encoding="utf-8")
            values = (bundle.helm_chart_dir / "values.yaml").read_text(encoding="utf-8")
            self.assertIn("ghcr.io/th3w1zard1/imageezgen3d:latest", deployment)
            self.assertIn("ghcr.io/th3w1zard1/imageezgen3d:latest", job)
            self.assertIn("ghcr.io/th3w1zard1/imageezgen3d:latest", podman)
            self.assertIn("repository: ghcr.io/th3w1zard1/imageezgen3d", values)
            self.assertIn('tag: "latest"', values)
            self.assertIn("targetPort: 7865", values)
            self.assertIn("containerPort: 7865", deployment)

    def test_render_deploy_assets_creates_expected_tree(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            bundle = render_deploy_assets(
                "ghcr.io/th3w1zard1/imageezgen3d:sha-1234567",
                Path(directory) / "dist",
            )
            self.assertTrue((bundle.helm_chart_dir / "Chart.yaml").exists())
            self.assertTrue((bundle.kubernetes_dir / "service.yaml").exists())
            self.assertTrue((bundle.nomad_dir / "imageezgen3d.nomad.hcl").exists())
            self.assertTrue((bundle.podman_dir / "imageezgen3d.container").exists())

    def test_render_deploy_assets_ignores_non_template_sources(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            stale = output / "kubernetes" / "deployment.yaml"
            stale.parent.mkdir(parents=True)
            stale.write_text("image: stale-owner:latest\n", encoding="utf-8")
            bundle = render_deploy_assets(
                "ghcr.io/th3w1zard1/imageezgen3d:latest",
                output,
            )
            deployment = (bundle.kubernetes_dir / "deployment.yaml").read_text(
                encoding="utf-8"
            )
            self.assertIn("ghcr.io/th3w1zard1/imageezgen3d:latest", deployment)
            self.assertNotIn("stale-owner:latest", deployment)


if __name__ == "__main__":
    unittest.main()