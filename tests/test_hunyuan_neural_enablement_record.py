from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path
from unittest import mock

from imageezgen3d.hunyuan_neural_enablement_preflight_bundle import (
    NeuralEnablementPreflightBundleResult,
    attestation_from_preflight_bundle,
)
from imageezgen3d.hunyuan_neural_enablement_record import (
    verify_neural_enablement_fixture_files,
    verify_neural_enablement_record,
    verify_neural_enablement_record_file,
)

FIXTURES = Path(__file__).resolve().parent / "fixtures"


class HunyuanNeuralEnablementRecordTests(unittest.TestCase):
    def test_fixture_verify_passes(self) -> None:
        issues = verify_neural_enablement_fixture_files(FIXTURES)
        self.assertEqual(issues, [])

    def test_verify_skipped_fixture_file(self) -> None:
        path = FIXTURES / "neural-enablement-preflight-skipped.json"
        self.assertEqual(verify_neural_enablement_record_file(path), [])

    def test_verify_rejects_ok_without_neural_ready(self) -> None:
        payload = json.loads(
            (FIXTURES / "neural-enablement-preflight-skipped.json").read_text(
                encoding="utf-8"
            )
        )
        payload["ok"] = True
        issues = verify_neural_enablement_record(payload)
        self.assertTrue(any("neural_enablement_ready" in issue for issue in issues))

    def test_verify_record_script(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                "scripts/verify_neural_enablement_record.py",
                str(FIXTURES / "neural-enablement-preflight-skipped.json"),
            ],
            check=False,
            capture_output=True,
            text=True,
            env={**__import__("os").environ, "PYTHONPATH": "src"},
        )
        self.assertEqual(result.returncode, 0, msg=result.stderr or result.stdout)

    def test_verify_fixtures_script(self) -> None:
        result = subprocess.run(
            [sys.executable, "scripts/verify_neural_enablement_record_fixtures.py"],
            check=False,
            capture_output=True,
            text=True,
            env={**__import__("os").environ, "PYTHONPATH": "src"},
        )
        self.assertEqual(result.returncode, 0, msg=result.stderr or result.stdout)

    def test_attestation_ok_requires_neural_enablement_ready(self) -> None:
        result = NeuralEnablementPreflightBundleResult(
            g7_enablement_preflight_ok=True,
            neural_enablement_preflight_ok=True,
            neural_enablement_ready=False,
            g7_enablement_ready=False,
            neural_forward_ready=False,
            record_dir=Path("/tmp"),
            g7_enablement=mock.MagicMock(),  # type: ignore[arg-type]
            configured_inference={"expected_outcome": "adapter_disabled"},
            issues=("configured_adapter_neural_forward_not_ready",),
            record_path=Path("/tmp/neural-enablement-preflight.json"),
            record_verify_ok=True,
            parity_ok=True,
        )
        attestation = attestation_from_preflight_bundle(result)
        self.assertFalse(attestation.ok)


if __name__ == "__main__":
    unittest.main()
