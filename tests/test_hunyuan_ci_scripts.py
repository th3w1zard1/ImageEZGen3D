from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class HunyuanCiScriptsTests(unittest.TestCase):
    def test_admission_audit_and_enablement_preflight_records_align(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            audit_path = Path(directory) / "hunyuan-admission-audit.json"
            preflight_path = Path(directory) / "hunyuan-enablement-preflight.json"
            env = {**os.environ, "PYTHONPATH": "src"}

            audit = subprocess.run(
                [
                    sys.executable,
                    "scripts/hunyuan_admission_audit.py",
                    "--record",
                    str(audit_path),
                ],
                check=False,
                env=env,
                capture_output=True,
                text=True,
            )
            preflight = subprocess.run(
                [
                    sys.executable,
                    "scripts/hunyuan_enablement_preflight.py",
                    "--record",
                    str(preflight_path),
                ],
                check=False,
                env=env,
                capture_output=True,
                text=True,
            )

            self.assertEqual(
                audit.returncode,
                0,
                msg=audit.stderr or audit.stdout,
            )
            self.assertEqual(
                preflight.returncode,
                0,
                msg=preflight.stderr or preflight.stdout,
            )

            audit_payload = json.loads(audit_path.read_text(encoding="utf-8"))
            preflight_payload = json.loads(preflight_path.read_text(encoding="utf-8"))

            self.assertEqual(
                audit_payload["g7_readiness"],
                preflight_payload["g7_readiness"],
            )
            self.assertEqual(
                audit_payload["g8_enablement"],
                preflight_payload["g8_enablement"],
            )
            self.assertFalse(audit_payload["adapter_configured"])
            self.assertTrue(preflight_payload["prerequisites_met"])


if __name__ == "__main__":
    unittest.main()
