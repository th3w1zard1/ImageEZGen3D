from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from imageezgen3d.hunyuan_gpu_forward_e2e_attestation import GpuForwardE2eAttestation
from imageezgen3d.hunyuan_gpu_forward_workstation_bundle import (
    GpuForwardWorkstationBundleResult,
)
from imageezgen3d.hunyuan_workstation_enablement_preflight import (
    format_workstation_enablement_preflight_report,
    run_workstation_enablement_preflight,
    workstation_enablement_preflight_exit_code,
)
from imageezgen3d.hunyuan_workstation_evidence_preflight import (
    WorkstationEvidencePreflightResult,
)


class HunyuanWorkstationEnablementPreflightTests(unittest.TestCase):
    def test_ci_like_env_not_enablement_ready(self) -> None:
        result = run_workstation_enablement_preflight(
            record_dir=Path("/tmp/unused-enablement"),
            skip_weight_warm=True,
        )
        self.assertTrue(result.bundle_ok)
        self.assertFalse(result.enablement_workstation_ready)
        self.assertEqual(workstation_enablement_preflight_exit_code(result), 0)

    def test_bundle_writes_record(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            result = run_workstation_enablement_preflight(
                record_dir=Path(directory),
                skip_weight_warm=True,
            )
            self.assertTrue(result.bundle_ok)
            self.assertIsNotNone(result.bundle.record_path)

    def test_format_report(self) -> None:
        result = run_workstation_enablement_preflight(skip_weight_warm=True)
        text = format_workstation_enablement_preflight_report(result)
        self.assertIn("hunyuan_workstation_enablement_preflight_ok=True", text)
        self.assertIn("enablement_workstation_ready=False", text)

    @mock.patch(
        "imageezgen3d.hunyuan_workstation_enablement_preflight.evaluate_workstation_evidence_preflight"
    )
    @mock.patch(
        "imageezgen3d.hunyuan_workstation_enablement_preflight.run_gpu_forward_workstation_bundle"
    )
    def test_enablement_ready_when_bundle_and_evidence_pass(
        self,
        bundle_fn: mock.MagicMock,
        evidence_fn: mock.MagicMock,
    ) -> None:
        record = Path("/tmp/gpu-forward-e2e.json")
        attestation = GpuForwardE2eAttestation(
            ok=True,
            attempt_status="succeeded",
            workstation_ready=True,
            mesh_vertices=8,
            mesh_faces=12,
            blockers=(),
            issues=(),
            with_exports=True,
            artifacts=(("glb", 1000),),
        )
        bundle_fn.return_value = GpuForwardWorkstationBundleResult(
            bundle_ok=True,
            workstation_ready=True,
            evidence_ok=True,
            probe_blockers=(),
            attestation=attestation,
            record_path=record,
            verify_issues=(),
        )
        evidence_fn.return_value = WorkstationEvidencePreflightResult(
            record_path=record,
            record_present=True,
            record_verify_ok=True,
            workstation_evidence_ok=True,
            with_exports=True,
            attempt_status="succeeded",
            issues=(),
        )
        result = run_workstation_enablement_preflight(record_dir=Path("/tmp"))
        self.assertTrue(result.enablement_workstation_ready)

    def test_enablement_preflight_script(self) -> None:
        result = subprocess.run(
            [sys.executable, "scripts/hunyuan_workstation_enablement_preflight.py"],
            check=False,
            capture_output=True,
            text=True,
            env={**__import__("os").environ, "PYTHONPATH": "src"},
        )
        self.assertEqual(result.returncode, 0, msg=result.stderr or result.stdout)
        self.assertIn("enablement_workstation_ready=False", result.stdout)


if __name__ == "__main__":
    unittest.main()
