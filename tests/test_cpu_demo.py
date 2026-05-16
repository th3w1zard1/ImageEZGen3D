from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from PIL import Image

from imageezgen3d.config import AppConfig, AppSettings, StorageSettings
from imageezgen3d.mesh_checks import inspect_artifacts
from imageezgen3d.orchestrator import ImageEZOrchestrator


class CpuDemoTests(unittest.TestCase):
    def test_adapter_choices_hide_unconfigured_backends(self) -> None:
        orchestrator = ImageEZOrchestrator(AppConfig())
        self.assertEqual(orchestrator.adapter_choices(), ["auto", "cpu-demo"])

    def test_select_adapter_rejects_unconfigured_backend(self) -> None:
        orchestrator = ImageEZOrchestrator(AppConfig())
        with self.assertRaisesRegex(ValueError, "not enabled yet"):
            orchestrator.select_adapter("hunyuan-zerogpu")

    def test_generate_creates_artifacts_and_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            config = AppConfig(
                app=AppSettings(output_dir=Path(directory)),
                storage=StorageSettings(retention_runs=10),
            )
            orchestrator = ImageEZOrchestrator(config)
            image = Image.new("RGBA", (640, 640), (40, 120, 180, 255))
            result = orchestrator.generate(
                image, adapter_name="cpu-demo", quality="draft", seed=1
            )
            artifacts = result["artifacts"]
            self.assertTrue(Path(artifacts["glb"]).exists())
            self.assertTrue(Path(artifacts["obj"]).exists())
            self.assertTrue(Path(artifacts["manifest"]).exists())
            self.assertEqual(result["stage"], "done")

    def test_mesh_check_validates_glb_header(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            config = AppConfig(app=AppSettings(output_dir=Path(directory)))
            result = ImageEZOrchestrator(config).generate(
                Image.new("RGB", (512, 512), (120, 80, 60)), adapter_name="cpu-demo"
            )
            paths = {
                key: Path(value)
                for key, value in result["artifacts"].items()
                if key in {"glb", "obj", "ply", "stl"}
            }
            report = inspect_artifacts(paths)
            self.assertEqual(report.status, "ok")
            self.assertEqual(report.metrics["glb_version"], 2)


if __name__ == "__main__":
    unittest.main()
