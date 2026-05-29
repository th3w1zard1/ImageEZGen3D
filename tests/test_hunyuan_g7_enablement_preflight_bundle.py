from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from imageezgen3d.hunyuan_g7_enablement_preflight_bundle import (
    format_g7_enablement_preflight_bundle_report,
    run_g7_enablement_preflight_bundle,
)
from imageezgen3d.hunyuan_g7_preflight import G7ReadinessResult
from imageezgen3d.hunyuan_g9_preflight_bundle import G9PreflightBundleResult


class HunyuanG7EnablementPreflightBundleTests(unittest.TestCase):
    def test_ci_like_bundle(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            result = run_g7_enablement_preflight_bundle(
                record_dir=Path(directory),
                skip_weight_warm=True,
            )
            self.assertTrue(result.g7_enablement_preflight_ok)
            self.assertFalse(result.g7_enablement_ready)

    def test_format_report(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            result = run_g7_enablement_preflight_bundle(
                record_dir=Path(directory),
                skip_weight_warm=True,
            )
        text = format_g7_enablement_preflight_bundle_report(result)
        self.assertIn("g7_enablement_preflight_ok=True", text)
        self.assertIn("g7_enablement_ready=False", text)

    @mock.patch(
        "imageezgen3d.hunyuan_g7_enablement_preflight_bundle.evaluate_g7_readiness"
    )
    @mock.patch(
        "imageezgen3d.hunyuan_g7_enablement_preflight_bundle.run_g9_preflight_bundle"
    )
    def test_bundle_fails_when_g7_not_ready(
        self,
        g9_fn: mock.MagicMock,
        g7_fn: mock.MagicMock,
    ) -> None:
        g9_fn.return_value = G9PreflightBundleResult(
            bundle_ok=True,
            record_verify_ok=True,
            parity_ok=True,
            g9_preflight_bundle_ok=True,
            workstation_evidence_ready=False,
            record_dir=Path("/tmp"),
            issues=(),
        )
        g7_fn.return_value = G7ReadinessResult(
            ready=False,
            issues=("G6 [OPEN] exports",),
            gates=(),
        )
        result = run_g7_enablement_preflight_bundle(record_dir=Path("/tmp"))
        self.assertFalse(result.g7_enablement_preflight_ok)

    def test_g7_enablement_preflight_bundle_script(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                "scripts/hunyuan_g7_enablement_preflight_bundle.py",
                "--skip-weight-warm",
            ],
            check=False,
            capture_output=True,
            text=True,
            env={**__import__("os").environ, "PYTHONPATH": "src"},
        )
        self.assertEqual(result.returncode, 0, msg=result.stderr or result.stdout)
        self.assertIn("g7_enablement_preflight_ok=True", result.stdout)


if __name__ == "__main__":
    unittest.main()
