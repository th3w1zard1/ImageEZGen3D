from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from imageezgen3d.config import HunyuanSettings
from imageezgen3d.hunyuan_gpu_forward_smoke import (
    attempt_gpu_forward_workstation_e2e,
    attempt_gpu_forward_workstation_exports_e2e,
    evaluate_gpu_forward_workstation_readiness,
    format_gpu_forward_e2e_report,
    format_gpu_forward_workstation_report,
)
from imageezgen3d.hunyuan_inference import HunyuanMeshResult
from imageezgen3d.exporters import make_box_mesh


class HunyuanGpuForwardSmokeTests(unittest.TestCase):
    def test_default_workstation_not_ready(self) -> None:
        report = evaluate_gpu_forward_workstation_readiness(
            settings=HunyuanSettings(
                gpu_forward=False,
                inference_runner="tencent",
            ),
            skip_weight_warm=True,
        )
        self.assertFalse(report["workstation_ready"])
        self.assertIn("gpu_forward_disabled", report["blockers"])

    @mock.patch("imageezgen3d.hunyuan_gpu_forward_smoke.probe_tencent_pipeline_modules")
    @mock.patch("imageezgen3d.hunyuan_gpu_forward_smoke.evaluate_tier_c_readiness")
    @mock.patch("imageezgen3d.hunyuan_gpu_forward_smoke.describe_tencent_gpu_forward_readiness")
    def test_workstation_ready_when_gates_pass(
        self,
        gpu_readiness: mock.MagicMock,
        tier_c: mock.MagicMock,
        pipeline_probe: mock.MagicMock,
    ) -> None:
        tier_c.return_value = {
            "tier_b_ready": True,
            "tier_c_ready": True,
            "weights_verified": True,
            "inference_wired": True,
            "weight_root": "/weights",
        }
        pipeline_probe.return_value = {
            "pipeline_ready": True,
            "bindings_ready": True,
        }
        gpu_readiness.return_value = {
            "gpu_forward_enabled": True,
            "torch_available": True,
            "cuda_available": True,
            "gpu_forward_ready": True,
        }
        report = evaluate_gpu_forward_workstation_readiness(
            settings=HunyuanSettings(
                gpu_forward=True,
                inference_runner="tencent",
            ),
        )
        self.assertTrue(report["workstation_ready"])
        self.assertEqual(report["blockers"], [])

    def test_format_report_includes_blockers(self) -> None:
        report = evaluate_gpu_forward_workstation_readiness(skip_weight_warm=True)
        text = format_gpu_forward_workstation_report(report)
        self.assertIn("hunyuan_gpu_forward_probe_ok=True", text)
        self.assertIn("blockers=", text)

    def test_gpu_forward_probe_script(self) -> None:
        result = subprocess.run(
            [sys.executable, "scripts/hunyuan_gpu_forward_probe.py"],
            check=False,
            capture_output=True,
            text=True,
            env={**os.environ, "PYTHONPATH": "src"},
        )
        self.assertEqual(result.returncode, 0, msg=result.stderr or result.stdout)
        self.assertIn("hunyuan_gpu_forward_probe_ok=True", result.stdout)

    def test_gpu_forward_probe_script_json(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                "scripts/hunyuan_gpu_forward_probe.py",
                "--json",
                "--skip-weight-warm",
            ],
            check=False,
            capture_output=True,
            text=True,
            env={**os.environ, "PYTHONPATH": "src"},
        )
        self.assertEqual(result.returncode, 0, msg=result.stderr or result.stdout)
        payload = json.loads(result.stdout)
        self.assertIn("blockers", payload)
        self.assertIn("workstation_ready", payload)

    def test_e2e_skips_when_workstation_not_ready(self) -> None:
        report = attempt_gpu_forward_workstation_e2e(
            run_dir=Path("/tmp/unused"),
            settings=HunyuanSettings(gpu_forward=False),
            skip_weight_warm=True,
        )
        self.assertEqual(report["attempt_status"], "skipped")
        self.assertEqual(report["skip_reason"], "workstation_not_ready")

    @mock.patch("imageezgen3d.hunyuan_gpu_forward_smoke.WeightVerifiedHunyuanBackend")
    @mock.patch("imageezgen3d.hunyuan_gpu_forward_smoke.evaluate_gpu_forward_workstation_readiness")
    def test_e2e_not_implemented_when_runner_stops(
        self,
        readiness: mock.MagicMock,
        backend_cls: mock.MagicMock,
    ) -> None:
        readiness.return_value = {"workstation_ready": True, "blockers": []}
        backend_cls.return_value.run_shape_texture.side_effect = NotImplementedError(
            "Tencent shape forward executor is not registered"
        )
        with tempfile.TemporaryDirectory() as directory:
            sample = Path(directory) / "input.png"
            from PIL import Image

            Image.new("RGB", (8, 8), color=(1, 2, 3)).save(sample)
            report = attempt_gpu_forward_workstation_e2e(
                sample_path=sample,
                run_dir=Path(directory),
                settings=HunyuanSettings(
                    gpu_forward=True,
                    weight_backend=True,
                    inference_runner="tencent",
                ),
            )
        self.assertEqual(report["attempt_status"], "not_implemented")
        self.assertIn("executor", report["error"])

    @mock.patch("imageezgen3d.hunyuan_gpu_forward_smoke.WeightVerifiedHunyuanBackend")
    @mock.patch("imageezgen3d.hunyuan_gpu_forward_smoke.evaluate_gpu_forward_workstation_readiness")
    def test_e2e_succeeded_returns_mesh_topology(
        self,
        readiness: mock.MagicMock,
        backend_cls: mock.MagicMock,
    ) -> None:
        readiness.return_value = {"workstation_ready": True, "blockers": []}
        mesh = make_box_mesh(width=1.0, depth=1.0, height=1.0, color=(0.5, 0.5, 0.5, 1.0))
        backend_cls.return_value.run_shape_texture.return_value = HunyuanMeshResult(
            mesh=mesh
        )
        with tempfile.TemporaryDirectory() as directory:
            sample = Path(directory) / "input.png"
            from PIL import Image

            Image.new("RGB", (8, 8), color=(1, 2, 3)).save(sample)
            report = attempt_gpu_forward_workstation_e2e(
                sample_path=sample,
                run_dir=Path(directory),
                settings=HunyuanSettings(
                    gpu_forward=True,
                    weight_backend=True,
                    inference_runner="tencent",
                ),
            )
        self.assertEqual(report["attempt_status"], "succeeded")
        self.assertGreater(report["mesh_vertices"], 0)
        self.assertGreater(report["mesh_faces"], 0)

    def test_format_e2e_report(self) -> None:
        report = attempt_gpu_forward_workstation_e2e(
            run_dir=Path("/tmp/unused"),
            skip_weight_warm=True,
        )
        text = format_gpu_forward_e2e_report(report)
        self.assertIn("hunyuan_gpu_forward_e2e_ok=True", text)
        self.assertIn("attempt_status=skipped", text)

    def test_exports_e2e_skips_when_workstation_not_ready(self) -> None:
        report = attempt_gpu_forward_workstation_exports_e2e(
            run_dir=Path("/tmp/unused"),
            settings=HunyuanSettings(gpu_forward=False),
            skip_weight_warm=True,
        )
        self.assertEqual(report["attempt_status"], "skipped")
        self.assertTrue(report["with_exports"])

    def test_gpu_forward_e2e_script(self) -> None:
        result = subprocess.run(
            [sys.executable, "scripts/hunyuan_gpu_forward_e2e.py"],
            check=False,
            capture_output=True,
            text=True,
            env={**os.environ, "PYTHONPATH": "src"},
        )
        self.assertEqual(result.returncode, 0, msg=result.stderr or result.stdout)
        self.assertIn("hunyuan_gpu_forward_e2e_ok=True", result.stdout)
        self.assertIn("attempt_status=skipped", result.stdout)


if __name__ == "__main__":
    unittest.main()
