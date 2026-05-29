from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from PIL import Image

from imageezgen3d.tencent_hunyuan_pipeline import (
    TencentPipelineReadinessError,
    TencentStageContext,
    build_tencent_shape_forward_plan,
    build_tencent_texture_forward_plan,
    describe_tencent_forward_contract,
    ensure_tencent_pipeline_ready,
    format_tencent_pipeline_report,
    probe_tencent_pipeline_modules,
    resolve_tencent_pipeline_bindings,
    run_tencent_shape_stage,
    run_tencent_texture_stage,
)


def _fake_available_probe(_module: str) -> dict[str, object]:
    return {"available": True}


def _fake_binding(symbol: str) -> dict[str, object]:
    return {
        "available": True,
        "module": symbol.rsplit(".", 1)[0],
        "attr": symbol.rsplit(".", 1)[-1],
        "symbol": symbol,
        "symbol_type": "type",
    }


class TencentHunyuanPipelineTests(unittest.TestCase):
    def test_probe_pipeline_structure(self) -> None:
        report = probe_tencent_pipeline_modules()
        self.assertIn("upstream_commit", report)
        self.assertIn("shape", report)
        self.assertIn("texture", report)
        self.assertIn("shape_ready", report)
        self.assertIn("texture_ready", report)
        self.assertIn("bindings", report)
        self.assertIn("bindings_ready", report)
        self.assertIn("forward_contract", report)
        self.assertIn("pipeline_ready", report)
        self.assertFalse(report["pipeline_ready"])

    def test_ensure_pipeline_raises_when_shape_missing(self) -> None:
        def fake_probe(_module: str) -> dict[str, object]:
            return {"available": False}

        with self.assertRaises(TencentPipelineReadinessError) as ctx:
            ensure_tencent_pipeline_ready(probe_runner=fake_probe)
        self.assertIn("Missing Tencent shape pipeline modules", str(ctx.exception))

    @patch("imageezgen3d.tencent_hunyuan_pipeline.resolve_tencent_symbol")
    def test_bindings_ready_when_symbols_resolve(
        self,
        resolve_symbol: object,
    ) -> None:
        resolve_symbol.side_effect = lambda module, attr, **kwargs: _fake_binding(
            f"{module}.{attr}"
        )
        bindings = resolve_tencent_pipeline_bindings(probe_runner=_fake_available_probe)
        self.assertTrue(bindings["bindings_ready"])
        self.assertEqual(bindings["missing_bindings"], [])

    @patch("imageezgen3d.tencent_hunyuan_pipeline.resolve_tencent_symbol")
    def test_run_shape_stage_raises_when_bindings_ready(
        self,
        resolve_symbol: object,
    ) -> None:
        resolve_symbol.side_effect = lambda module, attr, **kwargs: _fake_binding(
            f"{module}.{attr}"
        )
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            checkpoint = root / "model.fp16.ckpt"
            checkpoint.write_bytes(b"ckpt")
            image = root / "input.png"
            Image.new("RGB", (8, 8), color=(10, 20, 30)).save(image)
            context = TencentStageContext(
                run_dir=root,
                processed_image=image,
                weight_root=root,
                shape_checkpoint=checkpoint,
            )
            with self.assertRaisesRegex(NotImplementedError, "__call__ is not wired"):
                run_tencent_shape_stage(
                    context=context,
                    probe_runner=_fake_available_probe,
                )

    def test_shape_forward_plan_matches_upstream_contract(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            checkpoint = root / "hunyuan3d-dit-v2-1" / "model.fp16.ckpt"
            checkpoint.parent.mkdir(parents=True)
            checkpoint.write_bytes(b"ckpt")
            image = root / "input.png"
            Image.new("RGB", (8, 8), color=(10, 20, 30)).save(image)
            context = TencentStageContext(
                run_dir=root,
                processed_image=image,
                weight_root=root,
                shape_checkpoint=checkpoint,
            )
            plan = build_tencent_shape_forward_plan(context)
            contract = describe_tencent_forward_contract()["shape"]
            self.assertEqual(plan.load_method, contract["load_method"])
            self.assertEqual(plan.subfolder, contract["subfolder"])
            self.assertEqual(plan.output_mesh, root / "tencent_shape_mesh.obj")

    def test_texture_forward_plan_uses_shape_mesh_path(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            checkpoint = root / "model.fp16.ckpt"
            checkpoint.write_bytes(b"ckpt")
            image = root / "input.png"
            shape_mesh = root / "shape.obj"
            shape_mesh.write_text("o mesh\n", encoding="utf-8")
            Image.new("RGB", (8, 8), color=(10, 20, 30)).save(image)
            context = TencentStageContext(
                run_dir=root,
                processed_image=image,
                weight_root=root,
                shape_checkpoint=checkpoint,
            )
            plan = build_tencent_texture_forward_plan(
                context,
                shape_mesh_path=shape_mesh,
            )
            self.assertEqual(plan.shape_mesh, shape_mesh)
            self.assertEqual(plan.output_mesh, root / "tencent_textured_mesh.obj")

    @patch("imageezgen3d.tencent_hunyuan_pipeline.resolve_tencent_symbol")
    def test_run_texture_stage_raises_when_bindings_ready(
        self,
        resolve_symbol: object,
    ) -> None:
        resolve_symbol.side_effect = lambda module, attr, **kwargs: _fake_binding(
            f"{module}.{attr}"
        )
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            checkpoint = root / "model.fp16.ckpt"
            checkpoint.write_bytes(b"ckpt")
            image = root / "input.png"
            Image.new("RGB", (8, 8), color=(10, 20, 30)).save(image)
            context = TencentStageContext(
                run_dir=root,
                processed_image=image,
                weight_root=root,
                shape_checkpoint=checkpoint,
            )
            with self.assertRaisesRegex(NotImplementedError, "__call__ is not wired"):
                run_tencent_texture_stage(
                    context=context,
                    probe_runner=_fake_available_probe,
                )

    def test_format_report_includes_bindings(self) -> None:
        report = probe_tencent_pipeline_modules()
        text = format_tencent_pipeline_report(report)
        self.assertIn("hunyuan_tencent_pipeline_probe_ok=True", text)
        self.assertIn("bindings_ready=", text)
        self.assertIn("forward_contract=", text)

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
        self.assertIn("bindings_ready=", result.stdout)

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
        self.assertIn("bindings_ready", payload)
        self.assertIn("forward_contract", payload)

    @patch("imageezgen3d.tencent_hunyuan_runner.ensure_tencent_pipeline_ready")
    def test_runner_reports_missing_pipeline_modules(
        self,
        ensure_ready: object,
    ) -> None:
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
