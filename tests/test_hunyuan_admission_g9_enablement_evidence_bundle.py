from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from imageezgen3d.hunyuan_admission_g9_enablement_evidence_bundle import (
    format_admission_g9_enablement_evidence_bundle_report,
    run_admission_g9_enablement_evidence_bundle,
)
from imageezgen3d.hunyuan_g9_enablement_evidence_bundle import (
    G9EnablementEvidenceBundleResult,
)
from imageezgen3d.hunyuan_neural_enablement_preflight_bundle import (
    NeuralEnablementPreflightBundleResult,
)

FIXTURES = Path(__file__).resolve().parent / "fixtures"


def _neural_result(*, directory: Path) -> NeuralEnablementPreflightBundleResult:
    g7_enablement = mock.MagicMock()
    g7_enablement.to_dict.return_value = {"g7_enablement_ready": False}
    return NeuralEnablementPreflightBundleResult(
        g7_enablement_preflight_ok=True,
        neural_enablement_preflight_ok=True,
        neural_enablement_ready=False,
        g7_enablement_ready=False,
        neural_forward_ready=False,
        record_dir=directory,
        g7_enablement=g7_enablement,
        configured_inference={"expected_outcome": "adapter_disabled"},
        issues=("configured_adapter_neural_forward_not_ready",),
        record_path=directory / "neural-enablement-preflight.json",
        record_verify_ok=True,
        parity_ok=True,
        live_probe_requested=False,
        live_probe_ok=None,
        live_probe_path=None,
        hosted_neural_requested=False,
        hosted_neural_ok=None,
        hosted_neural_path=None,
    )


def _skipped_g9_evidence_result(*, directory: Path) -> G9EnablementEvidenceBundleResult:
    record_path = directory / "g9-enablement-evidence.json"
    record_path.write_text(
        (FIXTURES / "g9-enablement-evidence-skipped.json").read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    return G9EnablementEvidenceBundleResult(
        g9_enablement_preflight_ok=True,
        g9_enablement_evidence_ready=False,
        neural_enablement_ready=False,
        neural_enablement_preflight_ok=True,
        hosted_neural_required=False,
        hosted_neural_ok=None,
        record_dir=directory,
        neural_enablement=_neural_result(directory=directory),
        issues=(),
        record_path=record_path,
        record_verify_ok=True,
        parity_ok=True,
    )


class HunyuanAdmissionG9EnablementEvidenceBundleTests(unittest.TestCase):
    def test_ci_like_bundle_without_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            result = run_admission_g9_enablement_evidence_bundle(
                record_dir=Path(directory),
                skip_weight_warm=True,
            )
            self.assertTrue(result.admission_preflight_ok)
            self.assertTrue(result.admission_g9_enablement_evidence_ok)
            self.assertFalse(result.g9_enablement_evidence_ready)
            self.assertTrue(result.g9_enablement_evidence.record_path.is_file())
            self.assertTrue(result.bundle_record_path.is_file())

    def test_format_report(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            result = run_admission_g9_enablement_evidence_bundle(
                record_dir=Path(directory),
                skip_weight_warm=True,
            )
        text = format_admission_g9_enablement_evidence_bundle_report(result)
        self.assertIn("admission_g9_enablement_evidence_ok=True", text)
        self.assertIn("g9_enablement_evidence_ready=False", text)

    @mock.patch(
        "imageezgen3d.hunyuan_admission_g9_enablement_evidence_bundle."
        "run_g9_enablement_evidence_bundle"
    )
    @mock.patch(
        "imageezgen3d.hunyuan_admission_g9_enablement_evidence_bundle."
        "_run_preflight_bundle"
    )
    def test_bundle_fails_when_preflight_fails(
        self,
        preflight_fn: mock.MagicMock,
        g9_fn: mock.MagicMock,
    ) -> None:
        with tempfile.TemporaryDirectory() as directory:
            record_dir = Path(directory)
            preflight_fn.return_value = False
            g9_fn.return_value = _skipped_g9_evidence_result(directory=record_dir)
            result = run_admission_g9_enablement_evidence_bundle(record_dir=record_dir)
        self.assertFalse(result.admission_g9_enablement_evidence_ok)
        self.assertTrue(any("hunyuan_preflight_bundle failed" in issue for issue in result.issues))

    def test_admission_g9_enablement_evidence_bundle_script(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                "scripts/hunyuan_admission_g9_enablement_evidence_bundle.py",
                "--skip-weight-warm",
            ],
            check=False,
            capture_output=True,
            text=True,
            env={**__import__("os").environ, "PYTHONPATH": "src"},
        )
        self.assertEqual(result.returncode, 0, msg=result.stderr or result.stdout)
        self.assertIn("admission_g9_enablement_evidence_ok=True", result.stdout)


if __name__ == "__main__":
    unittest.main()
