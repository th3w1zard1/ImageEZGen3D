from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from imageezgen3d.hunyuan_neural_enablement_artifact_parity import (
    verify_neural_enablement_artifact_files,
    verify_neural_enablement_artifact_parity,
)

FIXTURES = Path(__file__).resolve().parent / "fixtures"


class HunyuanNeuralEnablementArtifactParityTests(unittest.TestCase):
    def test_verify_passes_for_matching_fixtures(self) -> None:
        neural_payload = json.loads(
            (FIXTURES / "neural-enablement-preflight-skipped.json").read_text(
                encoding="utf-8"
            )
        )
        g9_payload = json.loads(
            (FIXTURES / "g9-workstation-bundle-skipped.json").read_text(encoding="utf-8")
        )
        issues = verify_neural_enablement_artifact_parity(
            neural_payload=neural_payload,
            g9_bundle_payload=g9_payload,
        )
        self.assertEqual(issues, [])

    def test_verify_fails_on_workstation_evidence_mismatch(self) -> None:
        neural_payload = json.loads(
            (FIXTURES / "neural-enablement-preflight-skipped.json").read_text(
                encoding="utf-8"
            )
        )
        g9_payload = json.loads(
            (FIXTURES / "g9-workstation-bundle-ready.json").read_text(encoding="utf-8")
        )
        issues = verify_neural_enablement_artifact_parity(
            neural_payload=neural_payload,
            g9_bundle_payload=g9_payload,
        )
        self.assertTrue(
            any("workstation_evidence_ready mismatch" in issue for issue in issues)
        )

    def test_verify_files_from_record_dir(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            record_dir = Path(directory)
            (record_dir / "neural-enablement-preflight.json").write_text(
                (FIXTURES / "neural-enablement-preflight-skipped.json").read_text(
                    encoding="utf-8"
                ),
                encoding="utf-8",
            )
            (record_dir / "g9-workstation-bundle.json").write_text(
                (FIXTURES / "g9-workstation-bundle-skipped.json").read_text(
                    encoding="utf-8"
                ),
                encoding="utf-8",
            )
            issues = verify_neural_enablement_artifact_files(record_dir)
            self.assertEqual(issues, [])

    def test_verify_artifact_parity_script(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            record_dir = Path(directory)
            (record_dir / "neural-enablement-preflight.json").write_text(
                (FIXTURES / "neural-enablement-preflight-skipped.json").read_text(
                    encoding="utf-8"
                ),
                encoding="utf-8",
            )
            (record_dir / "g9-workstation-bundle.json").write_text(
                (FIXTURES / "g9-workstation-bundle-skipped.json").read_text(
                    encoding="utf-8"
                ),
                encoding="utf-8",
            )
            result = subprocess.run(
                [
                    sys.executable,
                    "scripts/verify_neural_enablement_artifact_parity.py",
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
