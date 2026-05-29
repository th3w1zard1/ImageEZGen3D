from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from imageezgen3d.hunyuan_g9_workstation_bundle import (
    format_g9_workstation_bundle_report,
    run_g9_workstation_bundle,
)
from imageezgen3d.hunyuan_workstation_enablement_record import (
    WorkstationEnablementAttestation,
)


class HunyuanG9WorkstationBundleTests(unittest.TestCase):
    def test_ci_like_bundle_without_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            result = run_g9_workstation_bundle(
                record_dir=Path(directory),
                skip_weight_warm=True,
            )
            self.assertTrue(result.preflight_bundle_ok)
            self.assertTrue(result.g9_workstation_bundle_ok)
            self.assertFalse(result.workstation_evidence_ready)
            self.assertTrue(result.record_path.is_file())
            self.assertTrue(result.bundle_record_path.is_file())

    def test_format_report(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            result = run_g9_workstation_bundle(
                record_dir=Path(directory),
                skip_weight_warm=True,
            )
        text = format_g9_workstation_bundle_report(result)
        self.assertIn("hunyuan_g9_workstation_bundle_ok=True", text)
        self.assertIn("workstation_evidence_ready=False", text)

    @mock.patch("imageezgen3d.hunyuan_g9_workstation_bundle._run_preflight_bundle")
    @mock.patch(
        "imageezgen3d.hunyuan_g9_workstation_bundle.run_workstation_enablement_attestation"
    )
    def test_bundle_fails_when_preflight_fails(
        self,
        attestation_fn: mock.MagicMock,
        preflight_fn: mock.MagicMock,
    ) -> None:
        preflight_fn.return_value = False
        attestation_fn.return_value = WorkstationEnablementAttestation(
            ok=False,
            enablement_workstation_ready=False,
            bundle_ok=True,
            workstation_evidence_ok=False,
            workstation_ready=False,
            attempt_status="skipped",
            issues=(),
            bundle={},
            evidence={},
        )
        with tempfile.TemporaryDirectory() as directory:
            result = run_g9_workstation_bundle(record_dir=Path(directory))
        self.assertFalse(result.g9_workstation_bundle_ok)

    def test_g9_workstation_bundle_script(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                "scripts/hunyuan_g9_workstation_bundle.py",
                "--skip-weight-warm",
            ],
            check=False,
            capture_output=True,
            text=True,
            env={**__import__("os").environ, "PYTHONPATH": "src"},
        )
        self.assertEqual(result.returncode, 0, msg=result.stderr or result.stdout)
        self.assertIn("g9_workstation_bundle_ok=True", result.stdout)


if __name__ == "__main__":
    unittest.main()
