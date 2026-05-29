from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path

from imageezgen3d.hunyuan_workstation_evidence_preflight import (
    evaluate_workstation_evidence_preflight,
    format_workstation_evidence_preflight_report,
    workstation_evidence_preflight_exit_code,
)

FIXTURES = Path(__file__).resolve().parent / "fixtures"


class HunyuanWorkstationEvidencePreflightTests(unittest.TestCase):
    def test_missing_record_informational(self) -> None:
        result = evaluate_workstation_evidence_preflight(
            Path("/tmp/nonexistent-gpu-forward-e2e.json")
        )
        self.assertFalse(result.record_present)
        self.assertFalse(result.workstation_evidence_ok)
        self.assertEqual(workstation_evidence_preflight_exit_code(result), 0)

    def test_skipped_fixture_not_evidence_ok(self) -> None:
        result = evaluate_workstation_evidence_preflight(
            FIXTURES / "gpu-forward-e2e-skipped.json"
        )
        self.assertTrue(result.record_present)
        self.assertTrue(result.record_verify_ok)
        self.assertFalse(result.workstation_evidence_ok)

    def test_succeeded_exports_fixture_evidence_ok(self) -> None:
        result = evaluate_workstation_evidence_preflight(
            FIXTURES / "gpu-forward-e2e-succeeded-exports.json"
        )
        self.assertTrue(result.workstation_evidence_ok)
        self.assertTrue(result.with_exports)
        self.assertEqual(result.attempt_status, "succeeded")

    def test_succeeded_without_exports_not_evidence_ok(self) -> None:
        result = evaluate_workstation_evidence_preflight(
            FIXTURES / "gpu-forward-e2e-succeeded.json"
        )
        self.assertFalse(result.workstation_evidence_ok)
        self.assertTrue(any("with_exports" in issue for issue in result.issues))

    def test_format_report(self) -> None:
        result = evaluate_workstation_evidence_preflight(
            FIXTURES / "gpu-forward-e2e-skipped.json"
        )
        text = format_workstation_evidence_preflight_report(result)
        self.assertIn("hunyuan_workstation_evidence_preflight_ok=True", text)
        self.assertIn("workstation_evidence_ok=False", text)

    def test_preflight_script_missing_record(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                "scripts/hunyuan_workstation_evidence_preflight.py",
                "/tmp/missing-gpu-forward-e2e.json",
            ],
            check=False,
            capture_output=True,
            text=True,
            env={**__import__("os").environ, "PYTHONPATH": "src"},
        )
        self.assertEqual(result.returncode, 0, msg=result.stderr or result.stdout)

    def test_preflight_script_exports_fixture_strict(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                "scripts/hunyuan_workstation_evidence_preflight.py",
                str(FIXTURES / "gpu-forward-e2e-succeeded-exports.json"),
                "--strict",
            ],
            check=False,
            capture_output=True,
            text=True,
            env={**__import__("os").environ, "PYTHONPATH": "src"},
        )
        self.assertEqual(result.returncode, 0, msg=result.stderr or result.stdout)
        self.assertIn("workstation_evidence_ok=True", result.stdout)

    def test_preflight_script_skipped_fixture_strict_fails(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                "scripts/hunyuan_workstation_evidence_preflight.py",
                str(FIXTURES / "gpu-forward-e2e-skipped.json"),
                "--strict",
            ],
            check=False,
            capture_output=True,
            text=True,
            env={**__import__("os").environ, "PYTHONPATH": "src"},
        )
        self.assertEqual(result.returncode, 1, msg=result.stderr or result.stdout)


if __name__ == "__main__":
    unittest.main()
