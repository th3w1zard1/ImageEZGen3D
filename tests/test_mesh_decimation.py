from __future__ import annotations

import unittest

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
        self.assertEqual(len(reduced.faces), 100)
        self.assertLess(meta["faces_after"], meta["faces_before"])


if __name__ == "__main__":
    unittest.main()
