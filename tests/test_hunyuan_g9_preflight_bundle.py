from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from imageezgen3d.hunyuan_g9_preflight_bundle import (
    format_g9_preflight_bundle_report,
    run_g9_preflight_bundle,
)


class HunyuanG9PreflightBundleTests(unittest.TestCase):
    def test_ci_like_preflight_bundle(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            result = run_g9_preflight_bundle(
                record_dir=Path(directory),
                skip_weight_warm=True,
            )
            self.assertTrue(result.g9_preflight_bundle_ok)
            self.assertFalse(result.workstation_evidence_ready)

    def test_format_report(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            result = run_g9_preflight_bundle(
                record_dir=Path(directory),
                skip_weight_warm=True,
            )
        text = format_g9_preflight_bundle_report(result)
        self.assertIn("g9_preflight_bundle_ok=True", text)
        self.assertIn("workstation_evidence_ready=False", text)

    @mock.patch("imageezgen3d.hunyuan_g9_preflight_bundle.run_g9_workstation_bundle")
    def test_preflight_fails_when_bundle_fails(self, bundle_fn: mock.MagicMock) -> None:
        from imageezgen3d.hunyuan_g9_workstation_bundle import G9WorkstationBundleResult
        from imageezgen3d.hunyuan_g9_workstation_bundle_record import (
            G9WorkstationBundleAttestation,
        )
        from imageezgen3d.hunyuan_workstation_enablement_record import (
            WorkstationEnablementAttestation,
        )

        attestation = WorkstationEnablementAttestation(
            ok=False,
            enablement_workstation_ready=False,
            bundle_ok=False,
            workstation_evidence_ok=False,
            workstation_ready=False,
            attempt_status="skipped",
            issues=(),
            bundle={},
            evidence={},
        )
        bundle_attestation = G9WorkstationBundleAttestation(
            ok=False,
            g9_workstation_bundle_ok=False,
            preflight_bundle_ok=False,
            workstation_record_verify_ok=False,
            workstation_evidence_ready=False,
            issues=(),
            enablement=attestation.to_dict(),
        )
        bundle_fn.return_value = G9WorkstationBundleResult(
            preflight_bundle_ok=False,
            workstation_record_verify_ok=False,
            g9_workstation_bundle_ok=False,
            workstation_evidence_ready=False,
            record_path=Path("/tmp/workstation-enablement-preflight.json"),
            bundle_record_path=Path("/tmp/g9-workstation-bundle.json"),
            attestation=attestation,
            bundle_attestation=bundle_attestation,
            issues=("hunyuan_preflight_bundle failed",),
        )
        with tempfile.TemporaryDirectory() as directory:
            result = run_g9_preflight_bundle(record_dir=Path(directory))
        self.assertFalse(result.g9_preflight_bundle_ok)

    def test_g9_preflight_bundle_script(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                "scripts/hunyuan_g9_preflight_bundle.py",
                "--skip-weight-warm",
            ],
            check=False,
            capture_output=True,
            text=True,
            env={**__import__("os").environ, "PYTHONPATH": "src"},
        )
        self.assertEqual(result.returncode, 0, msg=result.stderr or result.stdout)
        self.assertIn("g9_preflight_bundle_ok=True", result.stdout)


if __name__ == "__main__":
    unittest.main()
