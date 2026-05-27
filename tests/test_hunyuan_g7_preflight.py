from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from imageezgen3d.hunyuan_admission import GateResult
from imageezgen3d.hunyuan_g7_preflight import (
    G7ReadinessResult,
    evaluate_g7_readiness,
    probe_hosted_hunyuan_not_enabled,
    validate_g7_hosted_generate_status,
)


def _gates_g1_g6_pass_g7_open() -> tuple[GateResult, ...]:
    return tuple(
        GateResult(f"G{i}", f"Gate {i}", "pass" if i <= 6 else "open", ("ok",))
        for i in range(1, 10)
    )


class HunyuanG7PreflightTests(unittest.TestCase):
    def test_evaluate_g7_readiness_passes_when_g1_through_g6_pass(self) -> None:
        result = evaluate_g7_readiness(_gates_g1_g6_pass_g7_open())
        self.assertTrue(result.ready, result.issues)

    def test_evaluate_g7_readiness_fails_when_g6_open(self) -> None:
        gates = tuple(
            GateResult(
                gate.gate_id,
                gate.title,
                "open" if gate.gate_id == "G6" else gate.status,
                gate.evidence,
            )
            for gate in _gates_g1_g6_pass_g7_open()
        )
        result = evaluate_g7_readiness(gates)
        self.assertFalse(result.ready)
        self.assertTrue(any("G6" in issue for issue in result.issues))

    def test_validate_g7_hosted_status_accepts_neural_markers(self) -> None:
        status = "\n".join(
            [
                "Run `20260527-120000-abcdef01` complete.",
                "- **Export budget:** up to 25,000 faces",
                "- **Backend used:** Hosted ZeroGPU (hunyuan-zerogpu)",
                "Downloads: manifest, glb, obj",
            ]
        )
        ok, issues, run_id = validate_g7_hosted_generate_status(status)
        self.assertTrue(ok, issues)
        self.assertEqual(run_id, "20260527-120000-abcdef01")

    def test_validate_g7_hosted_status_rejects_cpu_fallback(self) -> None:
        status = "\n".join(
            [
                "Run `20260527-120000-abcdef01` complete.",
                "- **Export budget:** up to 25,000 faces",
                "- **Backend used:** Local CPU Preview",
                "Downloads: manifest, glb",
            ]
        )
        ok, issues, _ = validate_g7_hosted_generate_status(status)
        self.assertFalse(ok)
        self.assertTrue(any("cpu-demo" in issue or "Local CPU" in issue for issue in issues))

    @patch("gradio_client.Client")
    def test_probe_hosted_rejects_false_g7_success(self, client_cls: object) -> None:
        client = client_cls.return_value
        client.predict.return_value = (
            None,
            "\n".join(
                [
                    "Run `20260527-120000-abcdef01` complete.",
                    "- **Export budget:** up to 25,000 faces",
                    "- **Backend used:** Hosted ZeroGPU (hunyuan-zerogpu)",
                    "manifest glb obj",
                ]
            ),
        )
        ready = G7ReadinessResult(ready=True, issues=(), gates=())
        with tempfile.TemporaryDirectory() as directory:
            sample = Path(directory) / "block.png"
            sample.write_bytes(b"png")
            with patch(
                "imageezgen3d.hunyuan_g7_preflight.evaluate_g7_readiness",
                return_value=ready,
            ):
                result = probe_hosted_hunyuan_not_enabled(
                    space_url="https://test.hf.space/",
                    sample_path=sample,
                )

        self.assertFalse(result.ok)
        self.assertTrue(
            any("g7-valid" in issue.lower() or "false g7" in issue.lower() for issue in result.issues)
        )

    @patch("gradio_client.Client")
    def test_probe_hosted_ok_when_client_raises(self, client_cls: object) -> None:
        client = client_cls.return_value
        client.predict.side_effect = ValueError("adapter not enabled")

        ready = G7ReadinessResult(ready=True, issues=(), gates=())
        with tempfile.TemporaryDirectory() as directory:
            sample = Path(directory) / "block.png"
            sample.write_bytes(b"png")
            with patch(
                "imageezgen3d.hunyuan_g7_preflight.evaluate_g7_readiness",
                return_value=ready,
            ):
                result = probe_hosted_hunyuan_not_enabled(
                    space_url="https://test.hf.space/",
                    sample_path=sample,
                )

        self.assertTrue(result.ok, result.issues)


if __name__ == "__main__":
    unittest.main()
