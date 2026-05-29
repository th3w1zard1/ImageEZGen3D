from __future__ import annotations

import json
import os
import subprocess
import sys
import unittest
from unittest.mock import patch

from imageezgen3d.tencent_hunyuan_pipeline import (
    TencentPipelineReadinessError,
    ensure_tencent_pipeline_ready,
    format_tencent_pipeline_report,
    probe_tencent_pipeline_modules,
    run_tencent_shape_stage,
)


class TencentHunyuanPipelineTests(unittest.TestCase):
    def test_probe_pipeline_structure(self) -> None:
        report = probe_tencent_pipeline_modules()
        self.assertIn("upstream_commit", report)
        self.assertIn("shape", report)
        self.assertIn("texture", report)
        self.assertIn("shape_ready", report)
        self.assertIn("texture_ready", report)
        self.assertIn("pipeline_ready", report)
        self.assertFalse(report["pipeline_ready"])

    def test_ensure_pipeline_raises_when_shape_missing(self) -> None:
        def fake_probe(_module: str) -> dict[str, object]:
            return {"available": False}

        with self.assertRaises(TencentPipelineReadinessError) as ctx:
            ensure_tencent_pipeline_ready(probe_runner=fake_probe)
        self.assertIn("Missing Tencent shape pipeline modules", str(ctx.exception))

    def test_run_shape_stage_raises_when_modules_ready(self) -> None:
        def fake_probe(_module: str) -> dict[str, object]:
            return {"available": True}

        with self.assertRaisesRegex(NotImplementedError, "shape tower entrypoints"):
            run_tencent_shape_stage(probe_runner=fake_probe)

    def test_format_report_includes_missing_modules(self) -> None:
        report = probe_tencent_pipeline_modules()
        text = format_tencent_pipeline_report(report)
        self.assertIn("hunyuan_tencent_pipeline_probe_ok=True", text)
        self.assertIn("shape_ready=", text)

    def test_pipeline_probe_script(self) -> None:
        result = subprocess.run(
            [sys.executable, "scripts/hunyuan_tencent_pipeline_probe.py"],
            check=False,
            capture_output=True,
            text=True,
            env={**os.environ, "PYTHONPATH": "src"},
        )
        self.assertEqual(result.returncode, 0, msg=result.stderr or result.stdout)
        self.assertIn("hunyuan_tencent_pipeline_probe_ok=True", result.stdout)

    def test_pipeline_probe_script_json(self) -> None:
        result = subprocess.run(
            [sys.executable, "scripts/hunyuan_tencent_pipeline_probe.py", "--json"],
            check=False,
            capture_output=True,
            text=True,
            env={**os.environ, "PYTHONPATH": "src"},
        )
        self.assertEqual(result.returncode, 0, msg=result.stderr or result.stdout)
        payload = json.loads(result.stdout)
        self.assertIn("missing_shape", payload)

    @patch("imageezgen3d.tencent_hunyuan_runner.ensure_tencent_pipeline_ready")
    def test_runner_reports_missing_pipeline_modules(
        self,
        ensure_ready: object,
    ) -> None:
        from pathlib import Path
        import tempfile

        from PIL import Image

        from imageezgen3d.adapters.base import GenerationRequest
        from imageezgen3d.generation_pipeline import PipelineStageTracker
        from imageezgen3d.tencent_hunyuan_runner import TencentHunyuanInferenceRunner

        ensure_ready.side_effect = TencentPipelineReadinessError(
            "Missing Tencent shape pipeline modules: hy3dshape_pipelines",
            report={"missing_shape": ["hy3dshape_pipelines"]},
        )
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            checkpoint = root / "hunyuan3d-dit-v2-1"
            checkpoint.mkdir(parents=True)
            (checkpoint / "model.fp16.ckpt").write_bytes(b"ckpt")
            image = root / "input.png"
            Image.new("RGB", (8, 8), color=(10, 20, 30)).save(image)
            request = GenerationRequest(
                run_dir=root,
                processed_image=image,
                view_images={},
                quality="draft",
                seed=1,
            )
            runner = TencentHunyuanInferenceRunner()
            with self.assertRaisesRegex(
                NotImplementedError,
                "Missing Tencent shape pipeline modules",
            ):
                runner.run_shape_texture(
                    request,
                    tracker=PipelineStageTracker(),
                    weight_root=root,
                    shape_checkpoint=checkpoint / "model.fp16.ckpt",
                )


if __name__ == "__main__":
    unittest.main()
