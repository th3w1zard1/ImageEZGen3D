from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from imageezgen3d.mesh_ops import (
    MeshOpsBackendError,
    MeshOpsError,
    analyze_printability,
    backend_summary,
    boolean_mesh,
    convert_mesh,
    remesh_mesh,
    repair_printability,
    resize_mesh,
    unwrap_uv,
)
from imageezgen3d.mesh_ops.backends import (
    boolean_engine,
    xatlas_available,
)


def _box(path: Path, extents=(1.0, 2.0, 3.0)) -> Path:
    import trimesh

    trimesh.creation.box(extents=extents).export(str(path))
    return path


def _open_box(path: Path) -> Path:
    """Box with one face pair removed — not watertight, has a hole."""
    import numpy as np
    import trimesh

    box = trimesh.creation.box(extents=(1.0, 1.0, 1.0))
    mask = np.ones(len(box.faces), dtype=bool)
    mask[:2] = False
    box.update_faces(mask)
    box.export(str(path))
    return path


class ConvertTests(unittest.TestCase):
    def test_convert_glb_to_obj(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            src = _box(tmp_path / "box.glb")
            report = convert_mesh(src, tmp_path / "box.obj")
            self.assertEqual(report.output_format, "obj")
            self.assertEqual(report.writer, "trimesh")
            self.assertTrue((tmp_path / "box.obj").is_file())
            self.assertGreater(report.metrics["face_count"], 0)

    def test_convert_to_delivery_format(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            src = _box(tmp_path / "box.glb")
            report = convert_mesh(src, tmp_path / "box.fbx")
            self.assertEqual(report.writer, "delivery_exports")
            self.assertTrue((tmp_path / "box.fbx").is_file())
            self.assertIn("geometry-only", report.notes)

    def test_convert_blend_reports_backend_gap(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            src = _box(tmp_path / "box.glb")
            with self.assertRaises(MeshOpsBackendError):
                convert_mesh(src, tmp_path / "box.blend")

    def test_missing_input_raises(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            with self.assertRaises(MeshOpsError):
                convert_mesh(tmp_path / "missing.glb", tmp_path / "out.obj")


class ResizeTests(unittest.TestCase):
    def test_resize_height(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            src = _box(tmp_path / "box.glb", extents=(1.0, 2.0, 3.0))
            report = resize_mesh(
                src, tmp_path / "resized.glb", resize_height=4.0
            )
            self.assertEqual(report.mode, "height")
            self.assertAlmostEqual(report.extents_after[1], 4.0, places=4)
            self.assertAlmostEqual(report.scale_factor, 2.0, places=6)

    def test_resize_longest_side(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            src = _box(tmp_path / "box.glb", extents=(1.0, 2.0, 3.0))
            report = resize_mesh(
                src, tmp_path / "resized.glb", resize_longest_side=6.0
            )
            self.assertEqual(report.mode, "longest_side")
            self.assertAlmostEqual(max(report.extents_after), 6.0, places=4)

    def test_auto_size_heuristic_notes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            src = _box(tmp_path / "box.glb")
            report = resize_mesh(src, tmp_path / "resized.glb", auto_size=True)
            self.assertEqual(report.mode, "auto")
            self.assertIn("heuristic", report.notes)
            self.assertAlmostEqual(max(report.extents_after), 1.0, places=4)

    def test_modes_are_mutually_exclusive(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            src = _box(tmp_path / "box.glb")
            with self.assertRaisesRegex(MeshOpsError, "mutually exclusive"):
                resize_mesh(
                    src,
                    tmp_path / "out.glb",
                    resize_height=1.0,
                    resize_longest_side=2.0,
                )

    def test_mode_required(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            src = _box(tmp_path / "box.glb")
            with self.assertRaisesRegex(MeshOpsError, "Exactly one resize mode"):
                resize_mesh(src, tmp_path / "out.glb")

    def test_origin_bottom_rests_on_ground(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            src = _box(tmp_path / "box.glb")
            out = tmp_path / "resized.glb"
            resize_mesh(src, out, resize_height=2.0, origin_at="bottom")
            from imageezgen3d.mesh_ops import load_mesh

            mesh = load_mesh(out)
            self.assertAlmostEqual(float(mesh.bounds[0][1]), 0.0, places=4)


class RemeshTests(unittest.TestCase):
    def test_remesh_decimates_to_target(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            import trimesh

            sphere = trimesh.creation.icosphere(subdivisions=4)
            src = tmp_path / "sphere.glb"
            sphere.export(str(src))
            report = remesh_mesh(
                src, tmp_path / "remeshed.glb", target_polycount=500
            )
            self.assertTrue(report.decimation_applied)
            self.assertLessEqual(report.faces_after, 520)

    def test_remesh_subdivides_when_target_above_count(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            src = _box(tmp_path / "box.glb")
            report = remesh_mesh(
                src, tmp_path / "remeshed.glb", target_polycount=400
            )
            self.assertGreater(report.subdivision_rounds, 0)
            self.assertGreater(report.faces_after, report.faces_before)

    def test_quad_topology_reports_fallback_without_bpy(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            src = _box(tmp_path / "box.glb")
            report = remesh_mesh(
                src, tmp_path / "remeshed.glb", target_polycount=100,
                topology="quad",
            )
            if not backend_summary()["bpy"]:
                self.assertEqual(report.topology_applied, "triangle")
                self.assertIn("bpy", report.notes)

    def test_invalid_topology_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            src = _box(tmp_path / "box.glb")
            with self.assertRaisesRegex(MeshOpsError, "Invalid topology"):
                remesh_mesh(src, tmp_path / "out.glb", topology="ngon")


class PrintabilityTests(unittest.TestCase):
    def test_analyze_watertight_box(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            src = _box(tmp_path / "box.glb")
            report = analyze_printability(src)
            self.assertTrue(report.is_watertight)
            self.assertGreater(report.volume, 0)
            self.assertEqual(report.non_manifold_edges, 0)
            self.assertEqual(report.holes, 0)
            self.assertEqual(report.error_count, 0)

    def test_analyze_open_box_reports_hole(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            src = _open_box(tmp_path / "open_box.glb")
            report = analyze_printability(src)
            self.assertFalse(report.is_watertight)
            self.assertGreaterEqual(report.holes, 1)
            self.assertGreaterEqual(report.error_count, 1)

    def test_repair_open_box_restores_watertightness(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            src = _open_box(tmp_path / "open_box.glb")
            report = repair_printability(src, tmp_path / "repaired.glb")
            self.assertFalse(report.before.is_watertight)
            self.assertTrue(report.after.is_watertight)
            self.assertIn("fill_holes", "".join(report.actions))
            self.assertTrue((tmp_path / "repaired.glb").is_file())


class BooleanTests(unittest.TestCase):
    def test_boolean_requires_engine_or_runs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            first = _box(tmp_path / "a.glb", extents=(2.0, 2.0, 2.0))
            import trimesh

            second_mesh = trimesh.creation.box(extents=(2.0, 2.0, 2.0))
            second_mesh.apply_translation((1.0, 0.0, 0.0))
            second = tmp_path / "b.glb"
            second_mesh.export(str(second))
            if boolean_engine() is None:
                with self.assertRaises(MeshOpsBackendError):
                    boolean_mesh(
                        first, second, tmp_path / "out.glb", operation="union"
                    )
            else:
                report = boolean_mesh(
                    first, second, tmp_path / "out.glb", operation="union"
                )
                self.assertGreater(report.metrics["face_count"], 0)
                self.assertTrue((tmp_path / "out.glb").is_file())

    def test_invalid_operation_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            first = _box(tmp_path / "a.glb")
            second = _box(tmp_path / "b.glb")
            with self.assertRaisesRegex(MeshOpsError, "Invalid boolean operation"):
                boolean_mesh(first, second, tmp_path / "out.glb", operation="xor")


class UnwrapTests(unittest.TestCase):
    def test_unwrap_requires_backend_or_runs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            src = _box(tmp_path / "box.glb")
            if not xatlas_available():
                with self.assertRaises(MeshOpsBackendError):
                    unwrap_uv(src, tmp_path / "unwrapped.obj")
            else:
                report = unwrap_uv(src, tmp_path / "unwrapped.obj")
                self.assertEqual(report.backend, "xatlas")
                self.assertGreater(report.uv_vertex_count, 0)
                self.assertTrue((tmp_path / "unwrapped.obj").is_file())

    def test_unwrap_output_format_validated(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            src = _box(tmp_path / "box.glb")
            with self.assertRaises(MeshOpsError):
                unwrap_uv(src, tmp_path / "unwrapped.stl")


class BackendSummaryTests(unittest.TestCase):
    def test_backend_summary_keys(self) -> None:
        summary = backend_summary()
        for key in (
            "trimesh",
            "bpy",
            "xatlas",
            "manifold3d",
            "blender_executable",
            "boolean_engine",
        ):
            self.assertIn(key, summary)
        self.assertTrue(summary["trimesh"])


if __name__ == "__main__":
    unittest.main()
