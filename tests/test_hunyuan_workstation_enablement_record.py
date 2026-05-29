from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from imageezgen3d.hunyuan_workstation_enablement_record import (
    attestation_from_enablement_result,
    run_workstation_enablement_attestation,
    verify_workstation_enablement_fixture_files,
    verify_workstation_enablement_record,
    verify_workstation_enablement_record_file,
)
from imageezgen3d.hunyuan_workstation_enablement_preflight import (
    run_workstation_enablement_preflight,
)

FIXTURES = Path(__file__).resolve().parent / "fixtures"


class HunyuanWorkstationEnablementRecordTests(unittest.TestCase):
    def test_skipped_attestation_not_ok(self) -> None:
        attestation = run_workstation_enablement_attestation(skip_weight_warm=True)
        self.assertFalse(attestation.ok)
        self.assertFalse(attestation.enablement_workstation_ready)

    def test_attestation_from_enablement_result(self) -> None:
        result = run_workstation_enablement_preflight(skip_weight_warm=True)
        attestation = attestation_from_enablement_result(result)
        self.assertEqual(
            attestation.enablement_workstation_ready,
            result.enablement_workstation_ready,
        )

    def test_verify_skipped_fixture(self) -> None:
        issues = verify_workstation_enablement_record_file(
            FIXTURES / "workstation-enablement-skipped.json"
        )
        self.assertEqual(issues, [])

    def test_verify_ready_fixture(self) -> None:
        issues = verify_workstation_enablement_record_file(
            FIXTURES / "workstation-enablement-ready.json"
        )
        self.assertEqual(issues, [])

    def test_verify_rejects_false_ok_marked_true(self) -> None:
        payload = json.loads(
            (FIXTURES / "workstation-enablement-skipped.json").read_text(encoding="utf-8")
        )
        payload["ok"] = True
        issues = verify_workstation_enablement_record(payload)
        self.assertTrue(issues)

    def test_verify_fixture_files(self) -> None:
        issues = verify_workstation_enablement_fixture_files(FIXTURES)
        self.assertEqual(issues, [])

    def test_enablement_preflight_writes_record(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            record = Path(directory) / "workstation-enablement-preflight.json"
            result = subprocess.run(
                [
                    sys.executable,
                    "scripts/hunyuan_workstation_enablement_preflight.py",
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
            self.assertEqual(payload["record_kind"], "hunyuan_workstation_enablement")
            self.assertFalse(payload["ok"])

    def test_verify_record_script_skipped_fixture(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                "scripts/verify_workstation_enablement_record.py",
                str(FIXTURES / "workstation-enablement-skipped.json"),
            ],
            check=False,
            capture_output=True,
            text=True,
            env={**__import__("os").environ, "PYTHONPATH": "src"},
        )
        self.assertEqual(result.returncode, 0, msg=result.stderr or result.stdout)


if __name__ == "__main__":
    unittest.main()
