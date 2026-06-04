from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

import unittest

from imageezgen3d.hunyuan_admission_g9_enablement_evidence_bundle import (
    run_admission_g9_enablement_evidence_bundle,
)
from imageezgen3d.hunyuan_enablement_evidence_capstones import (
    run_enablement_evidence_capstones,
    verify_enablement_evidence_capstones_files,
)
from imageezgen3d.hunyuan_neural_enablement_artifact_parity import (
    verify_neural_enablement_artifact_files,
)


class HunyuanEnablementEvidenceCapstonesTests(unittest.TestCase):
    def test_verify_files_fails_on_empty_record_dir(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            issues = verify_enablement_evidence_capstones_files(Path(directory))
        self.assertTrue(issues)
        self.assertTrue(any(issue.startswith("admission:") for issue in issues))
        self.assertTrue(any(issue.startswith("g9:") for issue in issues))
        self.assertTrue(any(issue.startswith("neural:") for issue in issues))

    def test_verify_files_passes_after_ci_like_admission_capstone(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            record_dir = Path(directory)
            run_admission_g9_enablement_evidence_bundle(
                record_dir=record_dir,
                skip_weight_warm=True,
            )
            issues = verify_enablement_evidence_capstones_files(record_dir)
        self.assertEqual(issues, [])

    def test_run_passes_after_ci_like_skip(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            result = run_enablement_evidence_capstones(
                record_dir=Path(directory),
                skip_weight_warm=True,
            )
        self.assertTrue(result.enablement_evidence_capstones_ok)
        self.assertTrue(result.capstones_verify_ok)
        self.assertEqual(result.verify_issues, ())

    def test_verify_enablement_evidence_capstones_script(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            record_dir = Path(directory)
            run_admission_g9_enablement_evidence_bundle(
                record_dir=record_dir,
                skip_weight_warm=True,
            )
            result = subprocess.run(
                [
                    sys.executable,
                    "scripts/verify_enablement_evidence_capstones.py",
                    "--record-dir",
                    str(record_dir),
                ],
                check=False,
                capture_output=True,
                text=True,
                env={**__import__("os").environ, "PYTHONPATH": "src"},
            )
        self.assertEqual(result.returncode, 0, msg=result.stderr or result.stdout)

    def test_hunyuan_enablement_evidence_capstones_script(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                "scripts/hunyuan_enablement_evidence_capstones.py",
                "--skip-weight-warm",
            ],
            check=False,
            capture_output=True,
            text=True,
            env={**__import__("os").environ, "PYTHONPATH": "src"},
        )
        self.assertEqual(result.returncode, 0, msg=result.stderr or result.stdout)
        self.assertIn("capstones_verify_ok=True", result.stdout)

    def test_hunyuan_enablement_evidence_capstones_strict_exits_one_on_ci(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                "scripts/hunyuan_enablement_evidence_capstones.py",
                "--skip-weight-warm",
                "--strict",
            ],
            check=False,
            capture_output=True,
            text=True,
            env={**__import__("os").environ, "PYTHONPATH": "src"},
        )
        self.assertEqual(result.returncode, 1, msg=result.stderr or result.stdout)

    def test_capstones_verify_subsumes_neural_artifact_parity(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            record_dir = Path(directory)
            result = run_enablement_evidence_capstones(
                record_dir=record_dir,
                skip_weight_warm=True,
            )
            capstone_issues = verify_enablement_evidence_capstones_files(record_dir)
            parity_issues = verify_neural_enablement_artifact_files(record_dir)
        self.assertTrue(result.enablement_evidence_capstones_ok)
        self.assertEqual(capstone_issues, [])
        self.assertEqual(parity_issues, [])


if __name__ == "__main__":
    unittest.main()
