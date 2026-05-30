from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from imageezgen3d.hunyuan_neural_enablement_artifact_parity import (
    verify_enablement_neural_artifact_parity,
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
            neural_payload = json.loads(
                (FIXTURES / "neural-enablement-preflight-skipped.json").read_text(
                    encoding="utf-8"
                )
            )
            (record_dir / "neural-enablement-preflight.json").write_text(
                json.dumps(neural_payload),
                encoding="utf-8",
            )
            (record_dir / "g9-workstation-bundle.json").write_text(
                (FIXTURES / "g9-workstation-bundle-skipped.json").read_text(
                    encoding="utf-8"
                ),
                encoding="utf-8",
            )
            enablement_payload = {
                "g7_readiness": neural_payload["preflight"]["g7_enablement"][
                    "g7_readiness"
                ],
                "prerequisites_met": True,
            }
            (record_dir / "hunyuan-enablement-preflight.json").write_text(
                json.dumps(enablement_payload),
                encoding="utf-8",
            )
            issues = verify_neural_enablement_artifact_files(record_dir)
            self.assertEqual(issues, [])

    def test_verify_enablement_neural_g7_mismatch(self) -> None:
        neural_payload = json.loads(
            (FIXTURES / "neural-enablement-preflight-skipped.json").read_text(
                encoding="utf-8"
            )
        )
        enablement_payload = {
            "g7_readiness": {"ready": True, "issues": [], "gates": []},
        }
        issues = verify_enablement_neural_artifact_parity(
            enablement_payload=enablement_payload,
            neural_payload=neural_payload,
        )
        self.assertTrue(any("g7_readiness mismatch" in issue for issue in issues))

    def test_verify_artifact_parity_script(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            record_dir = Path(directory)
            neural_payload = json.loads(
                (FIXTURES / "neural-enablement-preflight-skipped.json").read_text(
                    encoding="utf-8"
                )
            )
            (record_dir / "neural-enablement-preflight.json").write_text(
                json.dumps(neural_payload),
                encoding="utf-8",
            )
            (record_dir / "g9-workstation-bundle.json").write_text(
                (FIXTURES / "g9-workstation-bundle-skipped.json").read_text(
                    encoding="utf-8"
                ),
                encoding="utf-8",
            )
            (record_dir / "hunyuan-enablement-preflight.json").write_text(
                json.dumps(
                    {
                        "g7_readiness": neural_payload["preflight"]["g7_enablement"][
                            "g7_readiness"
                        ],
                    }
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
