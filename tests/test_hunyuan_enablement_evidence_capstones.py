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
    verify_enablement_evidence_capstones_files,
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


if __name__ == "__main__":
    unittest.main()
