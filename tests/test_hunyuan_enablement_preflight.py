from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from imageezgen3d.hunyuan_admission import GateResult
from imageezgen3d.hunyuan_enablement_preflight import (
    enablement_preflight_exit_code,
    evaluate_enablement_preflight,
)
from imageezgen3d.hunyuan_g8_preflight import G8EnablementStatus


def _gates_g1_g6_pass() -> tuple[GateResult, ...]:
    return tuple(
        GateResult(
            f"G{i}",
            f"Gate {i}",
            "pass" if i <= 6 else "open",
            ("ok",),
        )
        for i in range(1, 10)
    )


def _g8_not_documented() -> G8EnablementStatus:
    return G8EnablementStatus(
        section_present=True,
        documented=False,
        interim_open=True,
        gate_status="open",
    )


class HunyuanEnablementPreflightTests(unittest.TestCase):
    def test_prerequisites_met_when_g1_through_g6_pass(self) -> None:
        with patch(
            "imageezgen3d.hunyuan_enablement_preflight.evaluate_admission_gates",
            return_value=_gates_g1_g6_pass(),
        ):
            with patch(
                "imageezgen3d.hunyuan_enablement_preflight.g8_enablement_for_gates",
                return_value=_g8_not_documented(),
            ):
                result = evaluate_enablement_preflight()

        self.assertTrue(result.prerequisites_met)
        self.assertFalse(result.enablement_complete)
        self.assertEqual(len(result.blocking_enablement), 3)

    def test_exit_code_zero_while_adapter_disabled(self) -> None:
        with patch(
            "imageezgen3d.hunyuan_enablement_preflight.evaluate_admission_gates",
            return_value=_gates_g1_g6_pass(),
        ):
            with patch(
                "imageezgen3d.hunyuan_enablement_preflight.resolve_hunyuan_configured",
                return_value=False,
            ):
                with patch(
                    "imageezgen3d.hunyuan_enablement_preflight.g8_enablement_for_gates",
                    return_value=_g8_not_documented(),
                ):
                    result = evaluate_enablement_preflight()

        self.assertEqual(enablement_preflight_exit_code(result), 0)

    def test_exit_code_one_when_env_configured_with_open_enablement_gates(self) -> None:
        with patch.dict(os.environ, {"IMAGEEZ_HUNYUAN_CONFIGURED": "true"}, clear=True):
            with patch(
                "imageezgen3d.hunyuan_enablement_preflight.evaluate_admission_gates",
                return_value=_gates_g1_g6_pass(),
            ):
                with patch(
                    "imageezgen3d.hunyuan_enablement_preflight.g8_enablement_for_gates",
                    return_value=_g8_not_documented(),
                ):
                    result = evaluate_enablement_preflight()

        self.assertTrue(result.adapter_configured)
        self.assertEqual(enablement_preflight_exit_code(result), 1)

    def test_exit_code_one_when_g6_regresses(self) -> None:
        gates = tuple(
            GateResult(
                f"G{i}",
                f"Gate {i}",
                "open" if i == 6 else ("pass" if i <= 6 else "open"),
                ("ok",),
            )
            for i in range(1, 10)
        )
        with patch(
            "imageezgen3d.hunyuan_enablement_preflight.evaluate_admission_gates",
            return_value=gates,
        ):
            with patch(
                "imageezgen3d.hunyuan_enablement_preflight.g8_enablement_for_gates",
                return_value=_g8_not_documented(),
            ):
                result = evaluate_enablement_preflight()

        self.assertEqual(enablement_preflight_exit_code(result), 1)

    def test_enablement_preflight_script_writes_record_file(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            record_path = Path(directory) / "enablement-preflight.json"
            subprocess.run(
                [
                    sys.executable,
                    "scripts/hunyuan_enablement_preflight.py",
                    "--record",
                    str(record_path),
                ],
                check=True,
                env={**os.environ, "PYTHONPATH": "src"},
            )
            payload = json.loads(record_path.read_text(encoding="utf-8"))
            self.assertFalse(payload["adapter_configured"])
            self.assertTrue(payload["prerequisites_met"])
            self.assertFalse(payload["g8_enablement_documented"])
            self.assertTrue(payload["g8_enablement"]["interim_open"])
            self.assertTrue(payload["g7_readiness"]["ready"])


if __name__ == "__main__":
    unittest.main()
