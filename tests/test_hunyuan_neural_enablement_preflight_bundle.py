from __future__ import annotations

import importlib.util
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
    NeuralEnablementPreflightBundleResult,
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
            self.assertTrue(result.record_verify_ok)
            self.assertTrue(result.parity_ok)
            self.assertTrue(result.record_path.is_file())
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
        "imageezgen3d.hunyuan_neural_enablement_preflight_bundle.write_g7_live_probe_record"
    )
    def test_live_probe_writes_record_and_sets_flags(
        self,
        live_probe_record: mock.MagicMock,
    ) -> None:
        with tempfile.TemporaryDirectory() as directory:
            record_dir = Path(directory)
            live_probe_record.return_value = mock.MagicMock(
                ok=True,
                issues=(),
                record_path=record_dir / "hunyuan-g7-live-probe.json",
                payload={"ok": True, "issues": [], "readiness": {}, "hosted_probe": {}},
            )
            result = run_neural_enablement_preflight_bundle(
                record_dir=record_dir,
                skip_weight_warm=True,
                live_probe=True,
            )
            self.assertTrue(result.live_probe_requested)
            self.assertTrue(result.live_probe_ok)
            self.assertEqual(
                result.live_probe_path,
                record_dir / "hunyuan-g7-live-probe.json",
            )
            live_probe_record.assert_called_once()
            self.assertTrue(result.parity_ok)

    @mock.patch(
        "imageezgen3d.hunyuan_neural_enablement_preflight_bundle."
        "attestation_from_status_markdown"
    )
    @mock.patch(
        "imageezgen3d.hunyuan_neural_enablement_preflight_bundle."
        "write_g7_hosted_neural_record"
    )
    def test_hosted_neural_writes_record_and_sets_flags(
        self,
        write_record: mock.MagicMock,
        attestation_from_status: mock.MagicMock,
    ) -> None:
        attestation = mock.MagicMock(ok=True, issues=())
        attestation_from_status.return_value = attestation
        status = (
            "Run `20260527-120000-abcdef01` complete.\n"
            "- **Backend used:** Hosted ZeroGPU (hunyuan-zerogpu)\n"
        )
        with tempfile.TemporaryDirectory() as directory:
            record_dir = Path(directory)
            status_file = record_dir / "status.md"
            status_file.write_text(status, encoding="utf-8")
            result = run_neural_enablement_preflight_bundle(
                record_dir=record_dir,
                skip_weight_warm=True,
                hosted_neural=True,
                hosted_neural_status_file=status_file,
                hosted_neural_sample="Block",
            )
            self.assertTrue(result.hosted_neural_requested)
            self.assertTrue(result.hosted_neural_ok)
            self.assertEqual(
                result.hosted_neural_path,
                record_dir / "hunyuan-g7-hosted-neural.json",
            )
            attestation_from_status.assert_called_once_with(
                status,
                sample="Block",
                space_url=None,
            )
            write_record.assert_called_once()
            self.assertTrue(result.parity_ok)

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

    @mock.patch(
        "imageezgen3d.hunyuan_neural_enablement_preflight_bundle."
        "run_neural_enablement_preflight_bundle"
    )
    def test_strict_script_fails_when_parity_not_ok(
        self,
        bundle_fn: mock.MagicMock,
    ) -> None:
        with tempfile.TemporaryDirectory() as directory:
            record_dir = Path(directory)
            g7_result = _g7_enablement_result(directory=record_dir, enablement_ready=True)
            bundle_fn.return_value = NeuralEnablementPreflightBundleResult(
                g7_enablement_preflight_ok=True,
                neural_enablement_preflight_ok=True,
                neural_enablement_ready=True,
                g7_enablement_ready=True,
                neural_forward_ready=True,
                record_dir=record_dir,
                g7_enablement=g7_result,
                configured_inference={
                    "neural_forward_ready": True,
                    "expected_outcome": "neural_forward_attempt",
                },
                issues=("artifact_parity_mismatch",),
                record_path=record_dir / "neural-enablement-preflight.json",
                record_verify_ok=True,
                parity_ok=False,
                live_probe_requested=False,
                live_probe_ok=None,
                live_probe_path=None,
                hosted_neural_requested=False,
                hosted_neural_ok=None,
                hosted_neural_path=None,
            )
            repo_root = Path(__file__).resolve().parents[1]
            script_path = repo_root / "scripts" / "hunyuan_neural_enablement_preflight_bundle.py"
            spec = importlib.util.spec_from_file_location(
                "hunyuan_neural_enablement_preflight_bundle_cli",
                script_path,
            )
            assert spec is not None and spec.loader is not None
            cli_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(cli_module)
            exit_code = cli_module.main(["--record-dir", str(record_dir), "--strict"])
        self.assertEqual(exit_code, 1)

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
