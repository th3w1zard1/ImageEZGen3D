from __future__ import annotations

import os
import subprocess
import sys
import unittest

from imageezgen3d.hunyuan_admission import evaluate_admission_gates


class HunyuanG1G5ScriptTests(unittest.TestCase):
    def test_g1_legal_verify_script_passes(self) -> None:
        subprocess.run(
            [sys.executable, "scripts/hunyuan_g1_legal_verify.py"],
            check=True,
            env={**os.environ, "PYTHONPATH": "src"},
        )

    def test_resource_estimate_script_passes(self) -> None:
        result = subprocess.run(
            [sys.executable, "scripts/hunyuan_resource_estimate.py"],
            check=True,
            capture_output=True,
            text=True,
            env={**os.environ, "PYTHONPATH": "src"},
        )
        self.assertIn("hunyuan_resource_estimate_ok=True", result.stdout)

    def test_g5_gate_passes_with_resource_fit_doc(self) -> None:
        gates = {gate.gate_id: gate for gate in evaluate_admission_gates()}
        self.assertEqual(gates["G5"].status, "pass")


if __name__ == "__main__":
    unittest.main()
