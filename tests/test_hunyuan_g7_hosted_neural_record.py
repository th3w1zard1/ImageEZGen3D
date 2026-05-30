from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from imageezgen3d.hunyuan_g7_hosted_neural_record import (
    attestation_from_status_markdown,
    verify_g7_hosted_neural_fixture_files,
    verify_g7_hosted_neural_record,
    verify_g7_hosted_neural_record_file,
    write_g7_hosted_neural_record,
)

FIXTURES = Path(__file__).resolve().parent / "fixtures"

_VALID_STATUS = "\n".join(
    [
        "Run `20260527-120000-abcdef01` complete.",
        "- **Export budget:** up to 25,000 faces",
        "- **Backend used:** Hosted ZeroGPU (hunyuan-zerogpu)",
        "Downloads: manifest, glb, obj",
    ]
)


class HunyuanG7HostedNeuralRecordTests(unittest.TestCase):
    def test_fixture_verify_passes(self) -> None:
        issues = verify_g7_hosted_neural_fixture_files(FIXTURES)
        self.assertEqual(issues, [])

    def test_attestation_from_valid_status(self) -> None:
        attestation = attestation_from_status_markdown(
            _VALID_STATUS,
            sample="Block",
            space_url="https://example.hf.space/",
        )
        self.assertTrue(attestation.ok)
        self.assertTrue(attestation.g7_status_valid)
        self.assertEqual(attestation.run_id, "20260527-120000-abcdef01")

    def test_attestation_rejects_cpu_fallback(self) -> None:
        status = "\n".join(
            [
                "Run `20260527-120000-abcdef01` complete.",
                "- **Export budget:** up to 25,000 faces",
                "- **Backend used:** Local CPU Preview",
                "Downloads: manifest, glb",
            ]
        )
        attestation = attestation_from_status_markdown(status)
        self.assertFalse(attestation.ok)
        self.assertFalse(attestation.g7_status_valid)

    def test_verify_rejects_ok_with_invalid_status(self) -> None:
        payload = json.loads(
            (FIXTURES / "hunyuan-g7-hosted-neural-pass.json").read_text(encoding="utf-8")
        )
        payload["status_markdown"] = "cpu-demo fallback"
        payload["ok"] = True
        issues = verify_g7_hosted_neural_record(payload)
        self.assertTrue(issues)

    def test_record_and_verify_round_trip(self) -> None:
        attestation = attestation_from_status_markdown(_VALID_STATUS)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "hunyuan-g7-hosted-neural.json"
            write_g7_hosted_neural_record(path, attestation)
            self.assertEqual(verify_g7_hosted_neural_record_file(path), [])

    def test_verify_record_cli_subprocess(self) -> None:
        env = {**__import__("os").environ, "PYTHONPATH": "src"}
        valid_path = FIXTURES / "hunyuan-g7-hosted-neural-pass.json"
        with tempfile.TemporaryDirectory() as directory:
            invalid_path = Path(directory) / "invalid.json"
            invalid_path.write_text(
                json.dumps(
                    {
                        "record_kind": "hunyuan_g7_hosted_neural",
                        "ok": True,
                        "g7_status_valid": True,
                        "run_id": "x",
                        "status_markdown": "cpu-demo",
                        "adapter": "hunyuan-zerogpu",
                        "issues": [],
                    }
                ),
                encoding="utf-8",
            )
            ok_proc = subprocess.run(
                [
                    sys.executable,
                    "scripts/verify_hunyuan_g7_hosted_neural_record.py",
                    str(valid_path),
                ],
                check=False,
                env=env,
                capture_output=True,
                text=True,
            )
            bad_proc = subprocess.run(
                [
                    sys.executable,
                    "scripts/verify_hunyuan_g7_hosted_neural_record.py",
                    str(invalid_path),
                ],
                check=False,
                env=env,
                capture_output=True,
                text=True,
            )
        self.assertEqual(ok_proc.returncode, 0, msg=ok_proc.stderr or ok_proc.stdout)
        self.assertEqual(bad_proc.returncode, 1, msg=bad_proc.stderr or bad_proc.stdout)


if __name__ == "__main__":
    unittest.main()
