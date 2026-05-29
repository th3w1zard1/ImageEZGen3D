from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from imageezgen3d.hunyuan_tier_c_runtime import (
    TierCReadinessError,
    evaluate_tier_c_readiness,
    format_tier_c_readiness_report,
    prepare_tier_c_runtime,
)
from imageezgen3d.hunyuan_weights import resolve_shape_checkpoint


class HunyuanTierCRuntimeTests(unittest.TestCase):
    def test_evaluate_readiness_without_weight_warm(self) -> None:
        report = evaluate_tier_c_readiness(skip_weight_warm=True)
        self.assertIn("tier_b_ready", report)
        self.assertIn("tier_c_ready", report)
        self.assertIn("missing_tier_c", report)
        self.assertFalse(report["weights_verified"])
        self.assertFalse(report["inference_wired"])

    def test_prepare_runtime_raises_when_tier_c_missing(self) -> None:
        probe_report = {
            "tier_b": {"transformers": {"available": True}},
            "tier_c": {"open3d": {"available": False}},
            "tier_b_available": True,
            "tier_c_available": False,
            "weight_pin": {},
        }

        def fake_probe() -> dict[str, object]:
            return probe_report

        def fake_ensure(**_: object) -> Path:
            root = Path("/tmp/hunyuan-weights")
            checkpoint = root / "hunyuan3d-dit-v2-1"
            checkpoint.mkdir(parents=True, exist_ok=True)
            (checkpoint / "model.fp16.ckpt").write_bytes(b"ckpt")
            return root

        with self.assertRaises(TierCReadinessError) as ctx:
            prepare_tier_c_runtime(
                probe_runner=fake_probe,
                ensure_weights=fake_ensure,
            )
        self.assertIn("Missing tier C modules", str(ctx.exception))

    def test_prepare_runtime_raises_not_implemented_when_ready(self) -> None:
        probe_report = {
            "tier_b": {"transformers": {"available": True}},
            "tier_c": {"open3d": {"available": True}},
            "tier_b_available": True,
            "tier_c_available": True,
            "weight_pin": {},
        }

        def fake_probe() -> dict[str, object]:
            return probe_report

        def fake_ensure(**_: object) -> Path:
            root = Path("/tmp/hunyuan-ready")
            checkpoint = root / "hunyuan3d-dit-v2-1"
            checkpoint.mkdir(parents=True, exist_ok=True)
            (checkpoint / "model.fp16.ckpt").write_bytes(b"ckpt")
            return root

        with self.assertRaisesRegex(
            NotImplementedError,
            "inference runner is not wired yet",
        ):
            prepare_tier_c_runtime(
                probe_runner=fake_probe,
                ensure_weights=fake_ensure,
            )

    def test_resolve_shape_checkpoint_validates_sentinel(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with self.assertRaisesRegex(FileNotFoundError, "missing expected checkpoint"):
                resolve_shape_checkpoint(root)

    def test_format_report_includes_missing_modules(self) -> None:
        report = evaluate_tier_c_readiness(skip_weight_warm=True)
        text = format_tier_c_readiness_report(report)
        self.assertIn("hunyuan_tier_c_readiness_ok=True", text)
        self.assertIn("tier_c_ready=", text)

    def test_readiness_script_skip_weight_warm(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                "scripts/hunyuan_tier_c_readiness.py",
                "--skip-weight-warm",
            ],
            check=False,
            capture_output=True,
            text=True,
            env={**os.environ, "PYTHONPATH": "src"},
        )
        self.assertEqual(result.returncode, 0, msg=result.stderr or result.stdout)
        self.assertIn("hunyuan_tier_c_readiness_ok=True", result.stdout)

    def test_readiness_script_json(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                "scripts/hunyuan_tier_c_readiness.py",
                "--skip-weight-warm",
                "--json",
            ],
            check=False,
            capture_output=True,
            text=True,
            env={**os.environ, "PYTHONPATH": "src"},
        )
        self.assertEqual(result.returncode, 0, msg=result.stderr or result.stdout)
        payload = json.loads(result.stdout)
        self.assertIn("missing_tier_c", payload)


if __name__ == "__main__":
    unittest.main()
