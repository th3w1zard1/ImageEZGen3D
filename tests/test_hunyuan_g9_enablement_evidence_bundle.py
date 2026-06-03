from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from imageezgen3d.hunyuan_g9_enablement_evidence_bundle import (
    format_g9_enablement_evidence_bundle_report,
    run_g9_enablement_evidence_bundle,
)
from imageezgen3d.hunyuan_g9_enablement_evidence_record import (
    verify_g9_enablement_evidence_fixture_files,
    verify_g9_enablement_evidence_record,
)
from imageezgen3d.hunyuan_neural_enablement_preflight_bundle import (
    NeuralEnablementPreflightBundleResult,
)

FIXTURES = Path(__file__).resolve().parent / "fixtures"


def _neural_result(
    *,
    directory: Path,
    ready: bool = False,
    preflight_ok: bool = True,
    hosted_requested: bool = False,
    hosted_ok: bool | None = None,
) -> NeuralEnablementPreflightBundleResult:
    g7_enablement = mock.MagicMock()
    g7_enablement.to_dict.return_value = {"g7_enablement_ready": ready}
    return NeuralEnablementPreflightBundleResult(
        g7_enablement_preflight_ok=True,
        neural_enablement_preflight_ok=preflight_ok,
        neural_enablement_ready=ready,
        g7_enablement_ready=ready,
        neural_forward_ready=ready,
        record_dir=directory,
        g7_enablement=g7_enablement,
        configured_inference={"expected_outcome": "adapter_disabled"},
        issues=() if ready else ("configured_adapter_neural_forward_not_ready",),
        record_path=directory / "neural-enablement-preflight.json",
        record_verify_ok=True,
        parity_ok=True,
        live_probe_requested=False,
        live_probe_ok=None,
        live_probe_path=None,
        hosted_neural_requested=hosted_requested,
        hosted_neural_ok=hosted_ok,
        hosted_neural_path=(
            directory / "hunyuan-g7-hosted-neural.json" if hosted_requested else None
        ),
    )


class HunyuanG9EnablementEvidenceRecordTests(unittest.TestCase):
    def test_fixture_verify_passes(self) -> None:
        issues = verify_g9_enablement_evidence_fixture_files(FIXTURES)
        self.assertEqual(issues, [])

    def test_verify_rejects_ok_without_evidence_ready(self) -> None:
        payload = json.loads(
            (FIXTURES / "g9-enablement-evidence-skipped.json").read_text(
                encoding="utf-8"
            )
        )
        payload["ok"] = True
        issues = verify_g9_enablement_evidence_record(payload)
        self.assertTrue(any("g9_enablement_evidence_ready" in issue for issue in issues))

    def test_verify_record_script(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                "scripts/verify_g9_enablement_evidence_record.py",
                str(FIXTURES / "g9-enablement-evidence-skipped.json"),
            ],
            check=False,
            capture_output=True,
            text=True,
            env={**__import__("os").environ, "PYTHONPATH": "src"},
        )
        self.assertEqual(result.returncode, 0, msg=result.stderr or result.stdout)

    def test_verify_fixtures_script(self) -> None:
        result = subprocess.run(
            [sys.executable, "scripts/verify_g9_enablement_evidence_record_fixtures.py"],
            check=False,
            capture_output=True,
            text=True,
            env={**__import__("os").environ, "PYTHONPATH": "src"},
        )
        self.assertEqual(result.returncode, 0, msg=result.stderr or result.stdout)


class HunyuanG9EnablementEvidenceBundleTests(unittest.TestCase):
    @mock.patch(
        "imageezgen3d.hunyuan_g9_enablement_evidence_bundle."
        "verify_neural_enablement_artifact_files"
    )
    @mock.patch(
        "imageezgen3d.hunyuan_g9_enablement_evidence_bundle."
        "run_neural_enablement_preflight_bundle"
    )
    def test_ci_like_bundle(
        self,
        neural_bundle: mock.MagicMock,
        artifact_parity: mock.MagicMock,
    ) -> None:
        artifact_parity.return_value = []
        with tempfile.TemporaryDirectory() as directory:
            record_dir = Path(directory)
            neural_bundle.return_value = _neural_result(directory=record_dir)
            result = run_g9_enablement_evidence_bundle(record_dir=record_dir)
            self.assertTrue(result.g9_enablement_preflight_ok)
            self.assertFalse(result.g9_enablement_evidence_ready)
            self.assertTrue(result.record_verify_ok)
            self.assertTrue(result.parity_ok)
            self.assertTrue(result.record_path.is_file())

    @mock.patch(
        "imageezgen3d.hunyuan_g9_enablement_evidence_bundle."
        "verify_neural_enablement_artifact_files"
    )
    @mock.patch(
        "imageezgen3d.hunyuan_g9_enablement_evidence_bundle."
        "run_neural_enablement_preflight_bundle"
    )
    def test_evidence_ready_when_neural_and_hosted_pass(
        self,
        neural_bundle: mock.MagicMock,
        artifact_parity: mock.MagicMock,
    ) -> None:
        artifact_parity.return_value = []
        with tempfile.TemporaryDirectory() as directory:
            record_dir = Path(directory)
            neural_bundle.return_value = _neural_result(
                directory=record_dir,
                ready=True,
                hosted_requested=True,
                hosted_ok=True,
            )
            result = run_g9_enablement_evidence_bundle(
                record_dir=record_dir,
                hosted_neural=True,
                require_hosted_neural=True,
            )
            self.assertTrue(result.g9_enablement_evidence_ready)
            self.assertTrue(result.hosted_neural_required)
            self.assertTrue(result.hosted_neural_ok)

    @mock.patch(
        "imageezgen3d.hunyuan_g9_enablement_evidence_bundle."
        "verify_neural_enablement_artifact_files"
    )
    @mock.patch(
        "imageezgen3d.hunyuan_g9_enablement_evidence_bundle."
        "run_neural_enablement_preflight_bundle"
    )
    def test_require_hosted_neural_fails_without_record(
        self,
        neural_bundle: mock.MagicMock,
        artifact_parity: mock.MagicMock,
    ) -> None:
        artifact_parity.return_value = []
        with tempfile.TemporaryDirectory() as directory:
            record_dir = Path(directory)
            neural_bundle.return_value = _neural_result(
                directory=record_dir,
                ready=True,
            )
            result = run_g9_enablement_evidence_bundle(
                record_dir=record_dir,
                require_hosted_neural=True,
            )
            self.assertFalse(result.g9_enablement_evidence_ready)
            self.assertIn("hosted_neural_not_ready", result.issues)

    @mock.patch(
        "imageezgen3d.hunyuan_g9_enablement_evidence_bundle."
        "verify_neural_enablement_artifact_files"
    )
    @mock.patch(
        "imageezgen3d.hunyuan_g9_enablement_evidence_bundle."
        "run_neural_enablement_preflight_bundle"
    )
    def test_existing_hosted_neural_record_is_detected(
        self,
        neural_bundle: mock.MagicMock,
        artifact_parity: mock.MagicMock,
    ) -> None:
        artifact_parity.return_value = []
        with tempfile.TemporaryDirectory() as directory:
            record_dir = Path(directory)
            neural_bundle.return_value = _neural_result(
                directory=record_dir,
                ready=True,
            )
            hosted_fixture = FIXTURES / "hunyuan-g7-hosted-neural-pass.json"
            (record_dir / "hunyuan-g7-hosted-neural.json").write_text(
                hosted_fixture.read_text(encoding="utf-8"),
                encoding="utf-8",
            )
            result = run_g9_enablement_evidence_bundle(
                record_dir=record_dir,
                require_hosted_neural=True,
            )
            self.assertTrue(result.hosted_neural_ok)
            self.assertTrue(result.g9_enablement_evidence_ready)

    @mock.patch(
        "imageezgen3d.hunyuan_g9_enablement_evidence_bundle."
        "verify_neural_enablement_artifact_files"
    )
    def test_format_report(self, artifact_parity: mock.MagicMock) -> None:
        artifact_parity.return_value = []
        with tempfile.TemporaryDirectory() as directory:
            result = run_g9_enablement_evidence_bundle(
                record_dir=Path(directory),
                skip_weight_warm=True,
            )
        text = format_g9_enablement_evidence_bundle_report(result)
        self.assertIn("g9_enablement_preflight_ok=", text)
        self.assertIn("g9_enablement_evidence_ready=", text)

    def test_g9_enablement_evidence_bundle_script(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                "scripts/hunyuan_g9_enablement_evidence_bundle.py",
                "--skip-weight-warm",
            ],
            check=False,
            capture_output=True,
            text=True,
            env={**__import__("os").environ, "PYTHONPATH": "src"},
        )
        self.assertEqual(result.returncode, 0, msg=result.stderr or result.stdout)
        self.assertIn("g9_enablement_preflight_ok=True", result.stdout)


if __name__ == "__main__":
    unittest.main()
