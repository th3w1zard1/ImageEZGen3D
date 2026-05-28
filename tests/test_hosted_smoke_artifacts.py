from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from imageezgen3d.hosted_golden_smoke import HostedGoldenSmokeResult


class HostedSmokeArtifactsTests(unittest.TestCase):
    def test_verify_hosted_smoke_artifacts_cli_subprocess(self) -> None:
        draft = HostedGoldenSmokeResult(
            ok=True,
            run_id="20260524-000000-00000001",
            space_url="https://example.hf.space/",
            adapter_hint="cpu-demo",
            quality="draft",
            issues=(),
            g7_false_neural_guard_ok=True,
        )
        balanced = HostedGoldenSmokeResult(
            ok=True,
            run_id="20260524-000000-00000002",
            space_url="https://example.hf.space/",
            adapter_hint="cpu-demo",
            quality="balanced",
            issues=(),
            g7_false_neural_guard_ok=True,
        )
        env = {**os.environ, "PYTHONPATH": "src"}
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            golden_path = root / "hosted-golden-smoke.json"
            golden_path.write_text(
                json.dumps(draft.to_dict(), indent=2),
                encoding="utf-8",
            )
            tier_path = root / "hosted-export-tier-smoke.json"
            tier_path.write_text(
                json.dumps(
                    {"checks": [draft.to_dict(), balanced.to_dict()]},
                    indent=2,
                ),
                encoding="utf-8",
            )
            proc = subprocess.run(
                [
                    sys.executable,
                    "scripts/verify_hosted_smoke_artifacts.py",
                    str(golden_path),
                    str(tier_path),
                ],
                check=False,
                env=env,
                capture_output=True,
                text=True,
            )
        self.assertEqual(proc.returncode, 0, msg=proc.stderr or proc.stdout)
        self.assertIn("hosted_smoke_artifacts=ok", proc.stdout)


if __name__ == "__main__":
    unittest.main()
