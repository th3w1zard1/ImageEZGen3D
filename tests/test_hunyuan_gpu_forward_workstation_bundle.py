from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from imageezgen3d.hunyuan_gpu_forward_workstation_bundle import (
    format_workstation_bundle_report,
    run_gpu_forward_workstation_bundle,
    verify_gpu_forward_e2e_fixture_files,
)

FIXTURES = Path(__file__).resolve().parent / "fixtures"


class HunyuanGpuForwardWorkstationBundleTests(unittest.TestCase):
    def test_bundle_skips_on_ci_like_env(self) -> None:
        result = run_gpu_forward_workstation_bundle(skip_weight_warm=True)
        self.assertTrue(result.bundle_ok)
        self.assertFalse(result.workstation_ready)
        self.assertFalse(result.evidence_ok)
        self.assertEqual(result.attestation.attempt_status, "skipped")

    def test_bundle_writes_and_verifies_record(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            result = run_gpu_forward_workstation_bundle(
                record_dir=Path(directory),
                skip_weight_warm=True,
            )
            self.assertTrue(result.bundle_ok)
            self.assertIsNotNone(result.record_path)
            assert result.record_path is not None
            self.assertTrue(result.record_path.is_file())
            payload = json.loads(result.record_path.read_text(encoding="utf-8"))
            self.assertEqual(payload["record_kind"], "hunyuan_gpu_forward_e2e")
            self.assertFalse(payload["ok"])

    def test_format_bundle_report(self) -> None:
        result = run_gpu_forward_workstation_bundle(skip_weight_warm=True)
        text = format_workstation_bundle_report(result)
        self.assertIn("hunyuan_gpu_forward_workstation_bundle_ok=True", text)
        self.assertIn("evidence_ok=False", text)

    def test_verify_fixture_files(self) -> None:
        issues = verify_gpu_forward_e2e_fixture_files(FIXTURES)
        self.assertEqual(issues, [])

    def test_bundle_script(self) -> None:
        result = subprocess.run(
            [sys.executable, "scripts/hunyuan_gpu_forward_workstation_bundle.py"],
            check=False,
            capture_output=True,
            text=True,
            env={**__import__("os").environ, "PYTHONPATH": "src"},
        )
        self.assertEqual(result.returncode, 0, msg=result.stderr or result.stdout)
        self.assertIn("hunyuan_gpu_forward_workstation_bundle_ok=True", result.stdout)

    def test_fixture_verify_script(self) -> None:
        result = subprocess.run(
            [sys.executable, "scripts/verify_gpu_forward_e2e_fixtures.py"],
            check=False,
            capture_output=True,
            text=True,
            env={**__import__("os").environ, "PYTHONPATH": "src"},
        )
        self.assertEqual(result.returncode, 0, msg=result.stderr or result.stdout)
        self.assertIn("gpu_forward_e2e_fixtures=ok", result.stdout)

    @mock.patch(
        "imageezgen3d.hunyuan_gpu_forward_workstation_bundle.verify_gpu_forward_e2e_record_file"
    )
    @mock.patch(
        "imageezgen3d.hunyuan_gpu_forward_workstation_bundle.run_gpu_forward_e2e_attestation"
    )
    def test_bundle_not_ok_when_verify_fails(
        self,
        attestation_fn: mock.MagicMock,
        verify_fn: mock.MagicMock,
    ) -> None:
        from imageezgen3d.hunyuan_gpu_forward_e2e_attestation import (
            GpuForwardE2eAttestation,
        )

        attestation_fn.return_value = GpuForwardE2eAttestation(
            ok=False,
            attempt_status="skipped",
            workstation_ready=False,
            mesh_vertices=None,
            mesh_faces=None,
            blockers=("tier_c",),
            issues=("attempt_status='skipped' (expected 'succeeded' for ok=True)",),
            with_exports=True,
        )
        verify_fn.return_value = ["record_kind mismatch"]
        with tempfile.TemporaryDirectory() as directory:
            result = run_gpu_forward_workstation_bundle(record_dir=Path(directory))
        self.assertFalse(result.bundle_ok)
        self.assertEqual(result.verify_issues, ("record_kind mismatch",))


if __name__ == "__main__":
    unittest.main()
