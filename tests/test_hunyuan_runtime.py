from __future__ import annotations

import json
import os
import subprocess
import sys
import unittest
from unittest.mock import patch

from imageezgen3d.hunyuan_runtime import (
    TIER_B_MODULES,
    TIER_C_MODULES,
    format_hunyuan_runtime_report,
    probe_hunyuan_runtime,
    probe_import,
)


class HunyuanRuntimeTests(unittest.TestCase):
    def test_probe_import_missing_module(self) -> None:
        payload = probe_import("imageezgen3d_nonexistent_runtime_probe_module")
        self.assertFalse(payload["available"])
        self.assertEqual(payload["error"], "ModuleNotFoundError")

    def test_probe_hunyuan_runtime_structure(self) -> None:
        report = probe_hunyuan_runtime()
        self.assertIn("tier_b", report)
        self.assertIn("tier_c", report)
        self.assertIn("tier_b_available", report)
        self.assertIn("tier_c_available", report)
        self.assertIn("weight_pin", report)
        self.assertEqual(len(report["tier_b"]), len(TIER_B_MODULES))
        self.assertEqual(len(report["tier_c"]), len(TIER_C_MODULES))
        self.assertIsInstance(report["tier_b_available"], bool)
        self.assertIsInstance(report["tier_c_available"], bool)

    def test_format_report_includes_tier_lines(self) -> None:
        report = probe_hunyuan_runtime()
        text = format_hunyuan_runtime_report(report)
        self.assertIn("hunyuan_runtime_probe_ok=True", text)
        self.assertIn("tier_b_available=", text)
        self.assertIn("tier_c_available=", text)
        self.assertIn("tier_b.transformers=", text)
        self.assertIn("tier_c.open3d=", text)

    @patch("imageezgen3d.hunyuan_runtime.probe_import")
    def test_probe_hunyuan_runtime_aggregates_availability(
        self,
        probe_import_mock: object,
    ) -> None:
        probe_import_mock.side_effect = lambda module: {
            "available": module == "yaml",
        }
        report = probe_hunyuan_runtime()
        self.assertFalse(report["tier_b_available"])
        self.assertFalse(report["tier_c_available"])

    def test_tier_c_probe_script_runs(self) -> None:
        result = subprocess.run(
            [sys.executable, "scripts/hunyuan_tier_c_probe.py"],
            check=False,
            capture_output=True,
            text=True,
            env={**os.environ, "PYTHONPATH": "src"},
        )
        self.assertEqual(result.returncode, 0, msg=result.stderr or result.stdout)
        self.assertIn("hunyuan_runtime_probe_ok=True", result.stdout)

    def test_tier_c_probe_script_json(self) -> None:
        result = subprocess.run(
            [sys.executable, "scripts/hunyuan_tier_c_probe.py", "--json"],
            check=False,
            capture_output=True,
            text=True,
            env={**os.environ, "PYTHONPATH": "src"},
        )
        self.assertEqual(result.returncode, 0, msg=result.stderr or result.stdout)
        payload = json.loads(result.stdout)
        self.assertIn("tier_b", payload)
        self.assertIn("tier_c", payload)

    def test_warm_weights_describe_only(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                "scripts/hunyuan_warm_weights.py",
                "--describe-only",
            ],
            check=False,
            capture_output=True,
            text=True,
            env={**os.environ, "PYTHONPATH": "src"},
        )
        self.assertEqual(result.returncode, 0, msg=result.stderr or result.stdout)
        self.assertIn("hunyuan_warm_weights_ok=True", result.stdout)
        self.assertIn("downloaded=False", result.stdout)


if __name__ == "__main__":
    unittest.main()
