from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from PIL import Image

from imageezgen3d.config import AppConfig, AppSettings, StorageSettings
from imageezgen3d.mesh_checks import inspect_artifacts
from imageezgen3d.orchestrator import PREVIEW_FALLBACK_DISCLAIMER, ImageEZOrchestrator
from imageezgen3d.runtime import RuntimeStatus


class CpuDemoTests(unittest.TestCase):
    def test_adapter_choices_hide_unconfigured_backends(self) -> None:
        orchestrator = ImageEZOrchestrator(AppConfig())
        self.assertEqual(orchestrator.adapter_choices(), ["auto", "cpu-demo"])

    def test_select_adapter_rejects_unconfigured_backend(self) -> None:
        orchestrator = ImageEZOrchestrator(AppConfig())
        with self.assertRaisesRegex(ValueError, "not enabled yet"):
            orchestrator.select_adapter("hunyuan-zerogpu")

    def test_resolve_adapter_reports_cpu_fallback_when_zerogpu_adapter_is_disabled(
        self,
    ) -> None:
        orchestrator = ImageEZOrchestrator(AppConfig())
        mocked_status = RuntimeStatus(
            requested_mode="auto",
            prefer_zerogpu=True,
            zerogpu_enabled=True,
            zerogpu_runtime_available=True,
            cpu_fallback_allowed=True,
            reason="ZeroGPU runtime is available and preferred.",
        )
        with patch(
            "imageezgen3d.orchestrator.runtime_status", return_value=mocked_status
        ):
            resolution = orchestrator.resolve_adapter("auto")

        self.assertEqual(resolution.selected, "cpu-demo")
        self.assertFalse(resolution.zerogpu_runnable)
        self.assertEqual(
            resolution.fallback_reason,
            "ZeroGPU runtime is present, but the configured ZeroGPU model adapter is not enabled yet.",
        )
        self.assertIn("not enabled yet", resolution.message)

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
            self.assertTrue(Path(artifacts["export_sidecar"]).exists())
            self.assertEqual(result["stage"], "done")
            self.assertEqual(result["parameters"]["decimation_target"], 25_000)

    def test_generate_records_preview_disclaimer_on_cpu_fallback(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            config = AppConfig(
                app=AppSettings(output_dir=Path(directory)),
                storage=StorageSettings(retention_runs=10),
            )
            orchestrator = ImageEZOrchestrator(config)
            mocked_status = RuntimeStatus(
                requested_mode="auto",
                prefer_zerogpu=True,
                zerogpu_enabled=True,
                zerogpu_runtime_available=True,
                cpu_fallback_allowed=True,
                reason="ZeroGPU runtime is available and preferred.",
            )
            image = Image.new("RGBA", (640, 640), (40, 120, 180, 255))
            with patch(
                "imageezgen3d.orchestrator.runtime_status", return_value=mocked_status
            ):
                result = orchestrator.generate(image, adapter_name="auto", seed=3)

            self.assertEqual(
                result["parameters"]["preview_disclaimer"], PREVIEW_FALLBACK_DISCLAIMER
            )
            self.assertIn("not enabled yet", result["parameters"]["fallback_reason"])

    def test_generate_records_workspace_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            config = AppConfig(
                app=AppSettings(output_dir=Path(directory)),
                storage=StorageSettings(retention_runs=10),
            )
            orchestrator = ImageEZOrchestrator(config)
            image = Image.new("RGBA", (640, 640), (120, 80, 180, 255))
            brief_path = Path(directory) / "brief.txt"
            brief_path.write_text("Preserve the mug handle.", encoding="utf-8")

            result = orchestrator.generate(
                image,
                adapter_name="cpu-demo",
                quality="balanced",
                seed=7,
                project_brief="Preserve the mug handle silhouette.",
                starter_flow="clean-product-turntable",
                starter_flow_label="Clean Product Turntable",
                reference_brief=brief_path,
            )

            self.assertEqual(
                result["parameters"]["project_brief"],
                "Preserve the mug handle silhouette.",
            )
            self.assertEqual(
                result["parameters"]["starter_flow"], "clean-product-turntable"
            )
            self.assertEqual(
                result["parameters"]["starter_flow_label"],
                "Clean Product Turntable",
            )
            self.assertEqual(result["parameters"]["reference_brief_name"], "brief.txt")
            self.assertTrue(Path(result["artifacts"]["reference_brief"]).exists())

    def test_generate_high_quality_uses_higher_decimation_target(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            config = AppConfig(
                app=AppSettings(output_dir=Path(directory)),
                storage=StorageSettings(retention_runs=10),
            )
            orchestrator = ImageEZOrchestrator(config)
            image = Image.new("RGBA", (640, 640), (40, 120, 180, 255))
            result = orchestrator.generate(
                image, adapter_name="cpu-demo", quality="high", seed=2
            )
            self.assertEqual(result["parameters"]["decimation_target"], 500_000)

    def test_generate_balanced_exports_raw_and_decimates(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            config = AppConfig(
                app=AppSettings(output_dir=Path(directory)),
                storage=StorageSettings(retention_runs=10),
            )
            orchestrator = ImageEZOrchestrator(config)
            image = Image.new("RGBA", (640, 640), (40, 120, 180, 255))
            result = orchestrator.generate(
                image, adapter_name="cpu-demo", quality="balanced", seed=3
            )
            artifacts = result["artifacts"]
            self.assertTrue(Path(artifacts["raw_glb"]).exists())
            self.assertTrue(result["parameters"].get("decimation_applied"))
            self.assertTrue(result["parameters"].get("raw_exported"))
            sidecar = json.loads(
                Path(artifacts["export_sidecar"]).read_text(encoding="utf-8")
            )
            self.assertTrue(sidecar["raw_exported"])
            self.assertTrue(sidecar["decimation"]["decimation_applied"])
            self.assertLessEqual(
                sidecar["mesh_topology"]["face_count"],
                result["parameters"]["decimation_target"],
            )

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
