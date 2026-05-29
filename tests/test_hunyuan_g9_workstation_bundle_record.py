from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from imageezgen3d.hunyuan_g9_workstation_bundle import run_g9_workstation_bundle
from imageezgen3d.hunyuan_g9_workstation_bundle_record import (
    RECORD_KIND,
    attestation_from_enablement,
    verify_g9_workstation_bundle_fixture_files,
    verify_g9_workstation_bundle_record,
    verify_g9_workstation_bundle_record_file,
)

FIXTURES = Path(__file__).resolve().parent / "fixtures"


class HunyuanG9WorkstationBundleRecordTests(unittest.TestCase):
    def test_ci_like_bundle_writes_g9_record(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            result = run_g9_workstation_bundle(
                record_dir=Path(directory),
                skip_weight_warm=True,
            )
            self.assertTrue(result.bundle_record_path.is_file())
            payload = json.loads(result.bundle_record_path.read_text(encoding="utf-8"))
            self.assertEqual(payload["record_kind"], RECORD_KIND)
            self.assertTrue(result.g9_workstation_bundle_ok)
            self.assertFalse(payload["ok"])

    def test_verify_skipped_fixture(self) -> None:
        issues = verify_g9_workstation_bundle_record_file(
            FIXTURES / "g9-workstation-bundle-skipped.json"
        )
        self.assertEqual(issues, [])

    def test_verify_ready_fixture(self) -> None:
        issues = verify_g9_workstation_bundle_record_file(
            FIXTURES / "g9-workstation-bundle-ready.json"
        )
        self.assertEqual(issues, [])

    def test_verify_rejects_false_ok_marked_true(self) -> None:
        payload = json.loads(
            (FIXTURES / "g9-workstation-bundle-skipped.json").read_text(encoding="utf-8")
        )
        payload["ok"] = True
        issues = verify_g9_workstation_bundle_record(payload)
        self.assertTrue(issues)

    def test_verify_fixture_files(self) -> None:
        issues = verify_g9_workstation_bundle_fixture_files(FIXTURES)
        self.assertEqual(issues, [])

    def test_attestation_from_enablement_matches_bundle(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            result = run_g9_workstation_bundle(
                record_dir=Path(directory),
                skip_weight_warm=True,
            )
        attestation = attestation_from_enablement(
            preflight_bundle_ok=result.preflight_bundle_ok,
            workstation_record_verify_ok=result.workstation_record_verify_ok,
            g9_workstation_bundle_ok=result.g9_workstation_bundle_ok,
            workstation_evidence_ready=result.workstation_evidence_ready,
            issues=result.issues,
            attestation=result.attestation,
        )
        self.assertEqual(attestation.to_dict(), result.bundle_attestation.to_dict())

    def test_verify_record_script_skipped_fixture(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                "scripts/verify_g9_workstation_bundle_record.py",
                str(FIXTURES / "g9-workstation-bundle-skipped.json"),
            ],
            check=False,
            capture_output=True,
            text=True,
            env={**__import__("os").environ, "PYTHONPATH": "src"},
        )
        self.assertEqual(result.returncode, 0, msg=result.stderr or result.stdout)


if __name__ == "__main__":
    unittest.main()
