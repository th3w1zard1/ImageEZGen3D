from __future__ import annotations

import unittest
from unittest.mock import patch

from imageezgen3d.hunyuan_admission import GateResult
from imageezgen3d.hunyuan_enablement_preflight import (
    enablement_preflight_exit_code,
    evaluate_enablement_preflight,
)


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


class HunyuanEnablementPreflightTests(unittest.TestCase):
    def test_prerequisites_met_when_g1_through_g6_pass(self) -> None:
        with patch(
            "imageezgen3d.hunyuan_enablement_preflight.evaluate_admission_gates",
            return_value=_gates_g1_g6_pass(),
        ):
            with patch(
                "imageezgen3d.hunyuan_enablement_preflight.g8_enablement_validation_passed",
                return_value=False,
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
                "imageezgen3d.hunyuan_enablement_preflight.HunyuanPlaceholderAdapter"
            ) as adapter_cls:
                adapter_cls.return_value.capabilities.configured = False
                with patch(
                    "imageezgen3d.hunyuan_enablement_preflight.g8_enablement_validation_passed",
                    return_value=False,
                ):
                    result = evaluate_enablement_preflight()

        self.assertEqual(enablement_preflight_exit_code(result), 0)

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
                "imageezgen3d.hunyuan_enablement_preflight.g8_enablement_validation_passed",
                return_value=False,
            ):
                result = evaluate_enablement_preflight()

        self.assertEqual(enablement_preflight_exit_code(result), 1)


if __name__ == "__main__":
    unittest.main()
