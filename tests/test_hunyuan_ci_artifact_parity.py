from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from imageezgen3d.hunyuan_ci_artifact_parity import (
    verify_hunyuan_ci_artifact_files,
    verify_hunyuan_ci_artifact_parity,
)


class HunyuanCiArtifactParityVerifyTests(unittest.TestCase):
    def test_verify_passes_when_g7_g8_match(self) -> None:
        payload = {
            "g7_readiness": {"ready": True, "issues": []},
            "g8_enablement": {"documented": False, "interim_open": True},
        }
        self.assertEqual(verify_hunyuan_ci_artifact_parity(payload, payload), [])

    def test_verify_fails_on_g8_mismatch(self) -> None:
        audit = {"g7_readiness": {}, "g8_enablement": {"documented": False}}
        preflight = {"g7_readiness": {}, "g8_enablement": {"documented": True}}
        issues = verify_hunyuan_ci_artifact_parity(audit, preflight)
        self.assertTrue(any("g8_enablement" in issue for issue in issues))

    def test_verify_files_from_disk(self) -> None:
        payload = {
            "g7_readiness": {"ready": True, "issues": [], "gates": []},
            "g8_enablement": {
                "section_present": True,
                "documented": False,
                "interim_open": True,
                "gate_status": "open",
            },
        }
        with tempfile.TemporaryDirectory() as directory:
            audit_path = Path(directory) / "audit.json"
            preflight_path = Path(directory) / "preflight.json"
            audit_path.write_text(json.dumps(payload), encoding="utf-8")
            preflight_path.write_text(json.dumps(payload), encoding="utf-8")
            self.assertEqual(
                verify_hunyuan_ci_artifact_files(audit_path, preflight_path),
                [],
            )


if __name__ == "__main__":
    unittest.main()
