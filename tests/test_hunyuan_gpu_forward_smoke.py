from __future__ import annotations

import json
import os
import subprocess
import sys
import unittest
from unittest import mock

from imageezgen3d.config import HunyuanSettings
from imageezgen3d.hunyuan_gpu_forward_smoke import (
    evaluate_gpu_forward_workstation_readiness,
    format_gpu_forward_workstation_report,
)


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


if __name__ == "__main__":
    unittest.main()
