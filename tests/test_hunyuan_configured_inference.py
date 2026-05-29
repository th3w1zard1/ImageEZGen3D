from __future__ import annotations

import json
import os
import subprocess
import sys
import unittest
from unittest import mock

from imageezgen3d.config import HunyuanSettings
from imageezgen3d.hunyuan_configured_inference import (
    describe_configured_adapter_inference_path,
    format_configured_adapter_inference_report,
)


class HunyuanConfiguredInferenceTests(unittest.TestCase):
    def test_default_ci_like_adapter_disabled(self) -> None:
        with mock.patch.dict(os.environ, {}, clear=True):
            report = describe_configured_adapter_inference_path(
                settings=HunyuanSettings(),
                skip_weight_warm=True,
            )
        self.assertFalse(report["adapter_configured"])
        self.assertEqual(report["expected_outcome"], "adapter_disabled")
        self.assertFalse(report["neural_forward_eligible"])

    def test_configured_without_weight_backend_not_implemented(self) -> None:
        report = describe_configured_adapter_inference_path(
            settings=HunyuanSettings(configured=True),
            skip_weight_warm=True,
        )
        self.assertEqual(report["expected_outcome"], "not_implemented")
        self.assertEqual(report["backend_kind"], "none")

    @mock.patch(
        "imageezgen3d.hunyuan_configured_inference.evaluate_gpu_forward_workstation_readiness"
    )
    def test_neural_forward_ready_when_gates_pass(
        self,
        workstation: mock.MagicMock,
    ) -> None:
        workstation.return_value = {
            "workstation_ready": True,
            "blockers": [],
        }
        report = describe_configured_adapter_inference_path(
            settings=HunyuanSettings(
                configured=True,
                weight_backend=True,
                gpu_forward=True,
                inference_runner="tencent",
            ),
            skip_weight_warm=True,
        )
        self.assertTrue(report["neural_forward_eligible"])
        self.assertTrue(report["neural_forward_ready"])
        self.assertEqual(report["expected_outcome"], "neural_forward_attempt")

    def test_format_report_contains_probe_ok(self) -> None:
        report = describe_configured_adapter_inference_path(skip_weight_warm=True)
        text = format_configured_adapter_inference_report(report)
        self.assertIn("hunyuan_configured_inference_probe_ok=True", text)

    def test_configured_inference_probe_script(self) -> None:
        result = subprocess.run(
            [sys.executable, "scripts/hunyuan_configured_inference_probe.py"],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0)
        self.assertIn("hunyuan_configured_inference_probe_ok=True", result.stdout)

    def test_configured_inference_probe_script_json(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                "scripts/hunyuan_configured_inference_probe.py",
                "--json",
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0)
        payload = json.loads(result.stdout)
        self.assertIn("expected_outcome", payload)


if __name__ == "__main__":
    unittest.main()
