from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class HunyuanPreflightBundleTests(unittest.TestCase):
    def test_bundle_writes_json_and_exits_zero(self) -> None:
        repo_root = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as directory:
            record_dir = Path(directory)
            result = subprocess.run(
                [
                    sys.executable,
                    "scripts/hunyuan_preflight_bundle.py",
                    "--record-dir",
                    str(record_dir),
                ],
                cwd=repo_root,
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(
                result.returncode,
                0,
                msg=result.stderr or result.stdout,
            )
            audit_path = record_dir / "hunyuan-admission-audit.json"
            preflight_path = record_dir / "hunyuan-enablement-preflight.json"
            self.assertTrue(audit_path.is_file())
            self.assertTrue(preflight_path.is_file())
            audit = json.loads(audit_path.read_text(encoding="utf-8"))
            preflight = json.loads(preflight_path.read_text(encoding="utf-8"))
            self.assertEqual(audit["g7_readiness"], preflight["g7_readiness"])
            self.assertEqual(audit["g8_enablement"], preflight["g8_enablement"])

    def test_bundle_json_flag_writes_valid_json(self) -> None:
        repo_root = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as directory:
            record_dir = Path(directory)
            result = subprocess.run(
                [
                    sys.executable,
                    "scripts/hunyuan_preflight_bundle.py",
                    "--json",
                    "--record-dir",
                    str(record_dir),
                ],
                cwd=repo_root,
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 0, msg=result.stderr or result.stdout)
            audit = json.loads(
                (record_dir / "hunyuan-admission-audit.json").read_text(encoding="utf-8")
            )
            self.assertIn("gates", audit)
            self.assertIn("g8_enablement", audit)


if __name__ == "__main__":
    unittest.main()
