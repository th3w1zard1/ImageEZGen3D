from __future__ import annotations

import json
import os
import subprocess
import sys
import unittest
from unittest.mock import patch

from imageezgen3d.hunyuan_inference_runner import (
    describe_hunyuan_inference_runner,
    resolve_hunyuan_inference_runner,
)


class HunyuanInferenceRunnerTests(unittest.TestCase):
    def test_resolve_runner_default_unwired(self) -> None:
        self.assertIsNone(resolve_hunyuan_inference_runner())

    def test_describe_runner_reports_unwired(self) -> None:
        payload = describe_hunyuan_inference_runner()
        self.assertFalse(payload["inference_wired"])
        self.assertEqual(payload["runner_id"], "")
        self.assertIn("is registered", payload["note"])

    @patch("imageezgen3d.hunyuan_tier_c_runtime.resolve_hunyuan_inference_runner")
    def test_readiness_report_reflects_runner_resolver(
        self,
        resolve_runner: object,
    ) -> None:
        from imageezgen3d.hunyuan_tier_c_runtime import evaluate_tier_c_readiness

        resolve_runner.return_value = object()
        report = evaluate_tier_c_readiness(skip_weight_warm=True)
        self.assertTrue(report["inference_wired"])

    def test_runner_probe_script(self) -> None:
        result = subprocess.run(
            [sys.executable, "scripts/hunyuan_inference_runner_probe.py"],
            check=False,
            capture_output=True,
            text=True,
            env={**os.environ, "PYTHONPATH": "src"},
        )
        self.assertEqual(result.returncode, 0, msg=result.stderr or result.stdout)
        self.assertIn("hunyuan_inference_runner_probe_ok=True", result.stdout)
        self.assertIn("inference_wired=False", result.stdout)

    def test_runner_probe_script_json(self) -> None:
        result = subprocess.run(
            [sys.executable, "scripts/hunyuan_inference_runner_probe.py", "--json"],
            check=False,
            capture_output=True,
            text=True,
            env={**os.environ, "PYTHONPATH": "src"},
        )
        self.assertEqual(result.returncode, 0, msg=result.stderr or result.stdout)
        payload = json.loads(result.stdout)
        self.assertFalse(payload["inference_wired"])


if __name__ == "__main__":
    unittest.main()
