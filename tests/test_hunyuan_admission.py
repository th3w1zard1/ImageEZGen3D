from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from imageezgen3d.adapters.hunyuan import HunyuanPlaceholderAdapter
from imageezgen3d.hunyuan_admission import (
    audit_exit_code,
    evaluate_admission_gates,
    format_admission_report,
)


class HunyuanAdmissionTests(unittest.TestCase):
    def test_adapter_remains_disabled(self) -> None:
        self.assertFalse(HunyuanPlaceholderAdapter().capabilities.configured)

    def test_evaluate_returns_nine_gates(self) -> None:
        gates = evaluate_admission_gates()
        self.assertEqual(len(gates), 9)
        self.assertEqual([gate.gate_id for gate in gates], [f"G{i}" for i in range(1, 10)])

    def test_g1_legal_gate_passes_with_audit_record(self) -> None:
        gates = {gate.gate_id: gate for gate in evaluate_admission_gates()}
        self.assertEqual(gates["G1"].status, "pass")

    def test_g2_weight_access_gate_passes_with_dry_run_record(self) -> None:
        gates = {gate.gate_id: gate for gate in evaluate_admission_gates()}
        self.assertEqual(gates["G2"].status, "pass")

    def test_audit_exit_code_zero_while_disabled(self) -> None:
        self.assertEqual(audit_exit_code(), 0)

    def test_audit_exit_code_one_when_enabled_with_open_gates(self) -> None:
        gates = evaluate_admission_gates()
        with patch(
            "imageezgen3d.hunyuan_admission._adapter_configured",
            return_value=True,
        ):
            self.assertEqual(audit_exit_code(gates), 1)

    def test_format_report_mentions_adapter_configured(self) -> None:
        report = format_admission_report(evaluate_admission_gates())
        self.assertIn("adapter_configured=False", report)
        self.assertIn("G9", report)

    def test_audit_script_writes_record_file(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            record_path = Path(directory) / "audit.json"
            subprocess.run(
                [
                    sys.executable,
                    "scripts/hunyuan_admission_audit.py",
                    "--record",
                    str(record_path),
                ],
                check=True,
                env={**os.environ, "PYTHONPATH": "src"},
            )
            payload = json.loads(record_path.read_text(encoding="utf-8"))
            self.assertFalse(payload["adapter_configured"])
            self.assertEqual(len(payload["gates"]), 9)


if __name__ == "__main__":
    unittest.main()
