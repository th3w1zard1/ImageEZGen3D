from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from imageezgen3d.exporters import make_box_mesh, write_glb
from imageezgen3d.jobs.mesh_op_runner import run_mesh_op_job
from imageezgen3d.jobs.models import JobRequest
from imageezgen3d.mesh_ops.backends import xatlas_available
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


if __name__ == "__main__":
    unittest.main()
