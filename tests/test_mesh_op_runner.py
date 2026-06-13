from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from imageezgen3d.exporters import make_box_mesh, write_glb
from imageezgen3d.jobs.mesh_op_runner import run_mesh_op_job
from imageezgen3d.jobs.models import JobRequest
from imageezgen3d.mesh_ops.backends import boolean_engine, xatlas_available
from imageezgen3d.storage import RunStore


class MeshOpRunnerTests(unittest.TestCase):
    def test_unsupported_modality_raises(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            store = RunStore(directory)
            input_glb = Path(directory) / "input.glb"
            write_glb(
                make_box_mesh(1.0, 0.74, 1.35, (0.12, 0.58, 0.55, 1.0)),
                input_glb,
            )
            request = JobRequest(
                input_modality="not-a-real-op",
                mesh_input_path=str(input_glb),
            )
            with self.assertRaisesRegex(ValueError, "Unsupported mesh operation"):
                run_mesh_op_job(store, request)

    @unittest.skipUnless(xatlas_available(), "xatlas backend not installed")
    def test_unwrap_uv_mesh_op_writes_glb(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            store = RunStore(directory)
            input_glb = Path(directory) / "input.glb"
            write_glb(
                make_box_mesh(1.0, 0.74, 1.35, (0.12, 0.58, 0.55, 1.0)),
                input_glb,
            )
            request = JobRequest(
                input_modality="unwrap-uv",
                mesh_input_path=str(input_glb),
            )
            result = run_mesh_op_job(store, request)
            self.assertEqual(result["parameters"]["input_modality"], "unwrap-uv")
            self.assertIn("glb", result["artifacts"])

    def test_boolean_union_requires_second_mesh(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            store = RunStore(directory)
            input_glb = Path(directory) / "input.glb"
            write_glb(
                make_box_mesh(1.0, 0.74, 1.35, (0.12, 0.58, 0.55, 1.0)),
                input_glb,
            )
            request = JobRequest(
                input_modality="boolean-union",
                mesh_input_path=str(input_glb),
            )
            with self.assertRaisesRegex(ValueError, "second_mesh_path"):
                run_mesh_op_job(store, request)

    @unittest.skipUnless(boolean_engine() is not None, "boolean engine not installed")
    def test_boolean_union_mesh_op_writes_glb(self) -> None:
        import trimesh

        with tempfile.TemporaryDirectory() as directory:
            store = RunStore(directory)
            first_mesh = trimesh.creation.box(extents=(2.0, 2.0, 2.0))
            second_mesh = trimesh.creation.box(extents=(2.0, 2.0, 2.0))
            second_mesh.apply_translation((1.0, 0.0, 0.0))
            first_glb = Path(directory) / "first.glb"
            second_glb = Path(directory) / "second.glb"
            first_mesh.export(str(first_glb))
            second_mesh.export(str(second_glb))
            request = JobRequest(
                input_modality="boolean-union",
                mesh_input_path=str(first_glb),
                second_mesh_path=str(second_glb),
            )
            result = run_mesh_op_job(store, request)
            self.assertEqual(result["parameters"]["input_modality"], "boolean-union")
            self.assertIn("glb", result["artifacts"])
            report = result["parameters"]["mesh_op_report"]
            self.assertEqual(report["operation"], "union")


if __name__ == "__main__":
    unittest.main()
