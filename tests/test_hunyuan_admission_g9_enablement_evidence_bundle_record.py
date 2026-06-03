from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

from imageezgen3d.hunyuan_admission_g9_enablement_evidence_bundle_record import (
    verify_admission_g9_enablement_evidence_bundle_fixture_files,
    verify_admission_g9_enablement_evidence_bundle_record,
    verify_admission_g9_enablement_evidence_bundle_record_file,
)

FIXTURES = Path(__file__).resolve().parent / "fixtures"


class HunyuanAdmissionG9EnablementEvidenceBundleRecordTests(unittest.TestCase):
    def test_fixture_verify_passes(self) -> None:
        issues = verify_admission_g9_enablement_evidence_bundle_fixture_files(FIXTURES)
        self.assertEqual(issues, [])

    def test_verify_rejects_ok_without_evidence_ready(self) -> None:
        payload = json.loads(
            (
                FIXTURES / "admission-g9-enablement-evidence-bundle-skipped.json"
            ).read_text(encoding="utf-8")
        )
        payload["ok"] = True
        issues = verify_admission_g9_enablement_evidence_bundle_record(payload)
        self.assertTrue(any("g9_enablement_evidence_ready" in issue for issue in issues))

    def test_verify_record_script(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                "scripts/verify_admission_g9_enablement_evidence_bundle_record.py",
                str(FIXTURES / "admission-g9-enablement-evidence-bundle-skipped.json"),
            ],
            check=False,
            capture_output=True,
            text=True,
            env={**__import__("os").environ, "PYTHONPATH": "src"},
        )
        self.assertEqual(result.returncode, 0, msg=result.stderr or result.stdout)

    def test_verify_fixtures_script(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                "scripts/verify_admission_g9_enablement_evidence_bundle_record_fixtures.py",
            ],
            check=False,
            capture_output=True,
            text=True,
            env={**__import__("os").environ, "PYTHONPATH": "src"},
        )
        self.assertEqual(result.returncode, 0, msg=result.stderr or result.stdout)

    def test_verify_record_file(self) -> None:
        issues = verify_admission_g9_enablement_evidence_bundle_record_file(
            FIXTURES / "admission-g9-enablement-evidence-bundle-skipped.json"
        )
        self.assertEqual(issues, [])


if __name__ == "__main__":
    unittest.main()
