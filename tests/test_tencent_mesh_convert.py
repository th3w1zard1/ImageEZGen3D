from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from imageezgen3d.exporters import SimpleMesh, write_obj
from imageezgen3d.tencent_mesh_convert import (
    simple_mesh_from_obj,
    simple_mesh_from_trimesh_like,
)


class _TrimeshStub:
    def __init__(self) -> None:
        self.vertices = ((0.0, 0.0, 0.0), (1.0, 0.0, 0.0), (0.0, 1.0, 0.0))
        self.faces = ((0, 1, 2),)


class TencentMeshConvertTests(unittest.TestCase):
    def test_simple_mesh_from_trimesh_like(self) -> None:
        mesh = simple_mesh_from_trimesh_like(_TrimeshStub())
        self.assertEqual(len(mesh.vertices), 3)
        self.assertEqual(len(mesh.faces), 1)

    def test_simple_mesh_from_obj_round_trip(self) -> None:
        source = SimpleMesh(
            vertices=((0.0, 0.0, 0.0), (1.0, 0.0, 0.0), (0.0, 1.0, 0.0)),
            faces=((0, 1, 2),),
            color=(0.5, 0.5, 0.5, 1.0),
        )
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "mesh.obj"
            write_obj(source, path)
            loaded = simple_mesh_from_obj(path)
        self.assertEqual(loaded.vertices, source.vertices)
        self.assertEqual(loaded.faces, source.faces)


if __name__ == "__main__":
    unittest.main()
