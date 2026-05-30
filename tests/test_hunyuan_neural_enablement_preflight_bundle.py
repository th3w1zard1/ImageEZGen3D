from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from imageezgen3d.hunyuan_g7_enablement_preflight_bundle import (
    G7EnablementPreflightBundleResult,
)
from imageezgen3d.hunyuan_g7_preflight import G7ReadinessResult
from imageezgen3d.hunyuan_g9_preflight_bundle import G9PreflightBundleResult
from imageezgen3d.hunyuan_neural_enablement_preflight_bundle import (
    format_neural_enablement_preflight_bundle_report,
    run_neural_enablement_preflight_bundle,
)


def _g7_enablement_result(
    *,
    directory: Path,
    enablement_ready: bool = False,
) -> G7EnablementPreflightBundleResult:
    g9 = G9PreflightBundleResult(
        bundle_ok=True,
        record_verify_ok=True,
        parity_ok=True,
        g9_preflight_bundle_ok=True,
        workstation_evidence_ready=enablement_ready,
        record_dir=directory,
        issues=(),
    )
    g7 = G7ReadinessResult(ready=True, issues=(), gates=())
    return G7EnablementPreflightBundleResult(
        g9_preflight_bundle_ok=True,
        g7_readiness_ok=True,
        g7_enablement_preflight_ok=True,
        g7_enablement_ready=enablement_ready,
        workstation_evidence_ready=enablement_ready,
        record_dir=directory,
        g9_preflight=g9,
        g7_readiness=g7,
        issues=(),
    )


class HunyuanNeuralEnablementPreflightBundleTests(unittest.TestCase):
    def test_ci_like_bundle(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            result = run_neural_enablement_preflight_bundle(
                record_dir=Path(directory),
                skip_weight_warm=True,
            )
            self.assertTrue(result.neural_enablement_preflight_ok)
            self.assertFalse(result.neural_enablement_ready)
            self.assertFalse(result.neural_forward_ready)

    def test_format_report(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            result = run_neural_enablement_preflight_bundle(
                record_dir=Path(directory),
                skip_weight_warm=True,
            )
        text = format_neural_enablement_preflight_bundle_report(result)
        self.assertIn("neural_enablement_preflight_ok=True", text)
        self.assertIn("neural_enablement_ready=False", text)

    @mock.patch(
        "imageezgen3d.hunyuan_neural_enablement_preflight_bundle."
        "describe_configured_adapter_inference_path"
    )
    @mock.patch(
        "imageezgen3d.hunyuan_neural_enablement_preflight_bundle."
        "run_g7_enablement_preflight_bundle"
    )
    def test_neural_enablement_ready_when_both_gates_pass(
        self,
        g7_bundle: mock.MagicMock,
        configured_path: mock.MagicMock,
    ) -> None:
        g7_bundle.return_value = _g7_enablement_result(
            directory=Path("/tmp"),
            enablement_ready=True,
        )
        configured_path.return_value = {
            "neural_forward_ready": True,
            "expected_outcome": "neural_forward_attempt",
        }
        result = run_neural_enablement_preflight_bundle(record_dir=Path("/tmp"))
        self.assertTrue(result.neural_enablement_ready)
        self.assertTrue(result.neural_forward_ready)

    @mock.patch(
        "imageezgen3d.hunyuan_neural_enablement_preflight_bundle."
        "run_g7_enablement_preflight_bundle"
    )
    def test_bundle_fails_when_g7_preflight_fails(
        self,
        g7_bundle: mock.MagicMock,
    ) -> None:
        g7_bundle.return_value = G7EnablementPreflightBundleResult(
            g9_preflight_bundle_ok=False,
            g7_readiness_ok=False,
            g7_enablement_preflight_ok=False,
            g7_enablement_ready=False,
            workstation_evidence_ready=False,
            record_dir=Path("/tmp"),
            g9_preflight=G9PreflightBundleResult(
                bundle_ok=False,
                record_verify_ok=False,
                parity_ok=False,
                g9_preflight_bundle_ok=False,
                workstation_evidence_ready=False,
                record_dir=Path("/tmp"),
                issues=("g9 failed",),
            ),
            g7_readiness=G7ReadinessResult(
                ready=False,
                issues=("g7 failed",),
                gates=(),
            ),
            issues=("g9 failed", "g7 failed"),
        )
        result = run_neural_enablement_preflight_bundle(record_dir=Path("/tmp"))
        self.assertFalse(result.neural_enablement_preflight_ok)

    def test_neural_enablement_preflight_bundle_script(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                "scripts/hunyuan_neural_enablement_preflight_bundle.py",
                "--skip-weight-warm",
            ],
            check=False,
            capture_output=True,
            text=True,
            env={**__import__("os").environ, "PYTHONPATH": "src"},
        )
        self.assertEqual(result.returncode, 0, msg=result.stderr or result.stdout)
        self.assertIn("neural_enablement_preflight_ok=True", result.stdout)


if __name__ == "__main__":
    unittest.main()
