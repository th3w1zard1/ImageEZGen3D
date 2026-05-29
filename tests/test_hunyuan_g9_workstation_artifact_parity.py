from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from imageezgen3d.hunyuan_g9_workstation_artifact_parity import (
    verify_g9_workstation_artifact_files,
    verify_g9_workstation_artifact_parity,
)

FIXTURES = Path(__file__).resolve().parent / "fixtures"


class HunyuanG9WorkstationArtifactParityTests(unittest.TestCase):
    def test_verify_passes_for_matching_fixtures(self) -> None:
        g9_payload = json.loads(
            (FIXTURES / "g9-workstation-bundle-skipped.json").read_text(encoding="utf-8")
        )
        enablement_payload = g9_payload["enablement"]
        issues = verify_g9_workstation_artifact_parity(
            g9_bundle_payload=g9_payload,
            enablement_payload=enablement_payload,
        )
        self.assertEqual(issues, [])

    def test_verify_fails_on_enablement_mismatch(self) -> None:
        g9_payload = json.loads(
            (FIXTURES / "g9-workstation-bundle-skipped.json").read_text(encoding="utf-8")
        )
        enablement_payload = dict(g9_payload["enablement"])
        enablement_payload["ok"] = True
        issues = verify_g9_workstation_artifact_parity(
            g9_bundle_payload=g9_payload,
            enablement_payload=enablement_payload,
        )
        self.assertTrue(any("enablement mismatch" in issue for issue in issues))

    def test_verify_fails_when_adapter_configured(self) -> None:
        g9_payload = json.loads(
            (FIXTURES / "g9-workstation-bundle-skipped.json").read_text(encoding="utf-8")
        )
        enablement_payload = g9_payload["enablement"]
        issues = verify_g9_workstation_artifact_parity(
            g9_bundle_payload=g9_payload,
            enablement_payload=enablement_payload,
            audit_payload={"adapter_configured": True},
        )
        self.assertTrue(any("adapter_configured=true" in issue for issue in issues))

    def test_verify_files_from_record_dir(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            record_dir = Path(directory)
            g9_payload = json.loads(
                (FIXTURES / "g9-workstation-bundle-skipped.json").read_text(
                    encoding="utf-8"
                )
            )
            (record_dir / "g9-workstation-bundle.json").write_text(
                json.dumps(g9_payload),
                encoding="utf-8",
            )
            (record_dir / "workstation-enablement-preflight.json").write_text(
                json.dumps(g9_payload["enablement"]),
                encoding="utf-8",
            )
            issues = verify_g9_workstation_artifact_files(record_dir)
            self.assertEqual(issues, [])


if __name__ == "__main__":
    unittest.main()
