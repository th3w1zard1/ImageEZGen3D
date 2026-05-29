from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from imageezgen3d.hunyuan_gpu_forward_e2e_attestation import (
    GpuForwardE2eAttestation,
    attestation_from_attempt_report,
    format_attestation_report,
    run_gpu_forward_e2e_attestation,
    verify_gpu_forward_e2e_record,
    verify_gpu_forward_e2e_record_file,
)
from imageezgen3d.hunyuan_inference import HUNYUAN_ADAPTER

FIXTURES = Path(__file__).resolve().parent / "fixtures"


class HunyuanGpuForwardE2eAttestationTests(unittest.TestCase):
    def test_skipped_attempt_not_ok(self) -> None:
        attestation = attestation_from_attempt_report(
            {
                "readiness": {"workstation_ready": False, "blockers": ["tier_c"]},
                "attempt_status": "skipped",
                "skip_reason": "workstation_not_ready",
            }
        )
        self.assertFalse(attestation.ok)
        self.assertIn("attempt_status", attestation.issues[0])

    def test_succeeded_attempt_ok_with_stages(self) -> None:
        attestation = attestation_from_attempt_report(
            {
                "readiness": {"workstation_ready": True, "blockers": []},
                "attempt_status": "succeeded",
                "mesh_vertices": 100,
                "mesh_faces": 50,
                "pipeline_stages": [
                    {
                        "name": "shape",
                        "status": "succeeded",
                        "adapter": HUNYUAN_ADAPTER,
                    },
                    {
                        "name": "texture",
                        "status": "succeeded",
                        "adapter": HUNYUAN_ADAPTER,
                    },
                ],
            }
        )
        self.assertTrue(attestation.ok)
        self.assertEqual(attestation.issues, ())

    def test_succeeded_without_stages_not_ok(self) -> None:
        attestation = attestation_from_attempt_report(
            {
                "readiness": {"workstation_ready": True, "blockers": []},
                "attempt_status": "succeeded",
                "mesh_vertices": 100,
                "mesh_faces": 50,
                "pipeline_stages": [],
            }
        )
        self.assertFalse(attestation.ok)
        self.assertTrue(any("shape" in issue for issue in attestation.issues))

    def test_verify_skipped_fixture(self) -> None:
        issues = verify_gpu_forward_e2e_record_file(
            FIXTURES / "gpu-forward-e2e-skipped.json"
        )
        self.assertEqual(issues, [])

    def test_verify_succeeded_fixture(self) -> None:
        issues = verify_gpu_forward_e2e_record_file(
            FIXTURES / "gpu-forward-e2e-succeeded.json"
        )
        self.assertEqual(issues, [])

    def test_verify_rejects_false_ok_with_succeeded_status(self) -> None:
        payload = json.loads(
            (FIXTURES / "gpu-forward-e2e-succeeded.json").read_text(encoding="utf-8")
        )
        payload["pipeline_stages"] = []
        issues = verify_gpu_forward_e2e_record(payload)
        self.assertTrue(issues)

    @mock.patch(
        "imageezgen3d.hunyuan_gpu_forward_e2e_attestation.attempt_gpu_forward_workstation_e2e"
    )
    def test_run_attestation_delegates_to_attempt(
        self,
        attempt: mock.MagicMock,
    ) -> None:
        attempt.return_value = {
            "readiness": {"workstation_ready": False, "blockers": ["cuda"]},
            "attempt_status": "skipped",
            "skip_reason": "workstation_not_ready",
        }
        attestation = run_gpu_forward_e2e_attestation(skip_weight_warm=True)
        self.assertFalse(attestation.ok)
        attempt.assert_called_once()

    def test_format_attestation_report(self) -> None:
        attestation = GpuForwardE2eAttestation(
            ok=False,
            attempt_status="skipped",
            workstation_ready=False,
            mesh_vertices=None,
            mesh_faces=None,
            blockers=("tier_c",),
            issues=("attempt_status='skipped' (expected 'succeeded' for ok=True)",),
            skip_reason="workstation_not_ready",
        )
        text = format_attestation_report(attestation)
        self.assertIn("gpu_forward_e2e_attestation_ok=False", text)
        self.assertIn("skip_reason=workstation_not_ready", text)

    def test_verify_script_skipped_fixture(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                "scripts/verify_gpu_forward_e2e_record.py",
                str(FIXTURES / "gpu-forward-e2e-skipped.json"),
            ],
            check=False,
            capture_output=True,
            text=True,
            env={**__import__("os").environ, "PYTHONPATH": "src"},
        )
        self.assertEqual(result.returncode, 0, msg=result.stderr or result.stdout)
        self.assertIn("gpu_forward_e2e_record=ok", result.stdout)

    def test_e2e_script_writes_record(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            record = Path(directory) / "gpu-forward-e2e.json"
            result = subprocess.run(
                [
                    sys.executable,
                    "scripts/hunyuan_gpu_forward_e2e.py",
                    "--skip-weight-warm",
                    "--record",
                    str(record),
                ],
                check=False,
                capture_output=True,
                text=True,
                env={**__import__("os").environ, "PYTHONPATH": "src"},
            )
            self.assertEqual(result.returncode, 0, msg=result.stderr or result.stdout)
            self.assertTrue(record.is_file())
            payload = json.loads(record.read_text(encoding="utf-8"))
            self.assertEqual(payload["record_kind"], "hunyuan_gpu_forward_e2e")
            self.assertFalse(payload["ok"])


if __name__ == "__main__":
    unittest.main()
