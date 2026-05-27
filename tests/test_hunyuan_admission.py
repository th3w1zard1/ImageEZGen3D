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
    _g7_hosted_validation_passed,
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

    def test_g4_zerogpu_wiring_gate_passes_with_gpu_scaffold(self) -> None:
        gates = {gate.gate_id: gate for gate in evaluate_admission_gates()}
        self.assertEqual(gates["G4"].status, "pass")

    def test_g3_dependency_gate_passes_with_audit_record(self) -> None:
        gates = {gate.gate_id: gate for gate in evaluate_admission_gates()}
        self.assertEqual(gates["G3"].status, "pass")

    def test_g5_resource_fit_gate_passes_with_budget_doc(self) -> None:
        gates = {gate.gate_id: gate for gate in evaluate_admission_gates()}
        self.assertEqual(gates["G5"].status, "pass")

    def test_g6_manifest_parity_gate_passes_with_sample_fixture(self) -> None:
        gates = {gate.gate_id: gate for gate in evaluate_admission_gates()}
        self.assertEqual(gates["G6"].status, "pass")

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
            self.assertTrue(payload["g7_readiness"]["ready"])
            self.assertIn("g8_enablement", payload)
            self.assertFalse(payload["g8_enablement"]["documented"])
            self.assertTrue(payload["g8_enablement"]["interim_open"])

    def test_g7_gate_open_until_hosted_validation_records_pass(self) -> None:
        gates = {gate.gate_id: gate for gate in evaluate_admission_gates()}
        self.assertEqual(gates["G7"].status, "open")

    def test_g7_hosted_validation_ignores_prose_mentions(self) -> None:
        prose = "## Plan 061\n\nMentions G7_STATUS: PASS and hunyuan-zerogpu in prose only.\n"
        self.assertFalse(_g7_hosted_validation_passed(prose))

    def test_g7_hosted_validation_passes_in_dedicated_section(self) -> None:
        text = "\n".join(
            [
                "## G7 validation",
                "",
                "G7_STATUS: PASS",
                "- **Adapter:** hunyuan-zerogpu",
                "",
                "## Plan 062",
            ]
        )
        self.assertTrue(_g7_hosted_validation_passed(text))

    def test_g7_placeholder_open_does_not_close_gate(self) -> None:
        text = "\n".join(
            [
                "## G7 validation",
                "",
                "G7_STATUS: OPEN",
                "hunyuan-zerogpu path not validated yet",
            ]
        )
        self.assertFalse(_g7_hosted_validation_passed(text))

    def test_g8_gate_open_until_hosted_validation_records_pass(self) -> None:
        gates = {gate.gate_id: gate for gate in evaluate_admission_gates()}
        self.assertEqual(gates["G8"].status, "open")


if __name__ == "__main__":
    unittest.main()
