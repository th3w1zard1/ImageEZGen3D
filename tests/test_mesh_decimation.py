from __future__ import annotations

import unittest
from unittest.mock import patch

from imageezgen3d.exporters import make_box_mesh
from imageezgen3d.mesh_decimation import decimate_mesh, subdivide_mesh


class MeshDecimationTests(unittest.TestCase):
    def test_subdivide_increases_face_count(self) -> None:
        mesh = make_box_mesh(1.0, 1.0, 1.0, (1.0, 1.0, 1.0, 1.0))
        dense = subdivide_mesh(mesh, levels=2)
        self.assertEqual(len(mesh.faces), 12)
        self.assertEqual(len(dense.faces), 12 * 16)

    def test_decimate_mesh_noop_when_under_budget(self) -> None:
        mesh = make_box_mesh(1.0, 1.0, 1.0, (1.0, 1.0, 1.0, 1.0))
        reduced, meta = decimate_mesh(mesh, 100)
        self.assertFalse(meta["decimation_applied"])
        self.assertEqual(len(reduced.faces), 12)

    def test_decimate_mesh_reduces_over_budget(self) -> None:
        mesh = subdivide_mesh(
            make_box_mesh(1.0, 1.0, 1.0, (1.0, 1.0, 1.0, 1.0)),
            levels=3,
        )
        reduced, meta = decimate_mesh(mesh, 100)
        self.assertTrue(meta["decimation_applied"])
        self.assertLessEqual(len(reduced.faces), 100)
        self.assertLess(meta["faces_after"], meta["faces_before"])
        self.assertIn(meta.get("decimation_method"), ("quadric", "largest_face_mvp"))

    def test_decimate_mesh_uses_quadric_when_trimesh_available(self) -> None:
        try:
            import trimesh  # noqa: F401
        except ImportError:
            self.skipTest("trimesh not installed")

        mesh = subdivide_mesh(
            make_box_mesh(1.0, 1.0, 1.0, (1.0, 1.0, 1.0, 1.0)),
            levels=3,
        )
        _, meta = decimate_mesh(mesh, 100)
        self.assertEqual(meta.get("decimation_method"), "quadric")

    def test_decimate_mesh_falls_back_to_mvp_when_quadric_fails(self) -> None:
        mesh = subdivide_mesh(
            make_box_mesh(1.0, 1.0, 1.0, (1.0, 1.0, 1.0, 1.0)),
            levels=2,
        )
        with patch(
            "imageezgen3d.mesh_decimation._decimate_mesh_quadric",
            side_effect=RuntimeError("quadric unavailable"),
        ):
            reduced, meta = decimate_mesh(mesh, 50)
        self.assertTrue(meta["decimation_applied"])
        self.assertEqual(meta["decimation_method"], "largest_face_mvp")
        self.assertEqual(len(reduced.faces), 50)


if __name__ == "__main__":
    unittest.main()
