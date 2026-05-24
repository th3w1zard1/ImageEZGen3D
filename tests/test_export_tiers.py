from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from imageezgen3d.export_tiers import (
    build_export_sidecar,
    resolve_decimation_target,
)
from imageezgen3d.exporters import export_all, make_box_mesh, write_export_sidecar


class ExportTierTests(unittest.TestCase):
    def test_resolve_decimation_target_by_quality(self) -> None:
        self.assertEqual(resolve_decimation_target("draft"), 25_000)
        self.assertEqual(resolve_decimation_target("balanced"), 150_000)
        self.assertEqual(resolve_decimation_target("high"), 500_000)
        self.assertEqual(resolve_decimation_target("unknown", default=99), 99)

    def test_build_export_sidecar_marks_budget(self) -> None:
        sidecar = build_export_sidecar(
            quality="draft",
            decimation_target=25_000,
            vertex_count=8,
            face_count=12,
            adapter="cpu-demo",
        )
        self.assertTrue(sidecar["within_decimation_budget"])
        self.assertEqual(sidecar["mesh_topology"]["face_count"], 12)

    def test_export_all_writes_sidecar_file(self) -> None:
        mesh = make_box_mesh(1.0, 1.0, 1.0, (1.0, 1.0, 1.0, 1.0))
        with tempfile.TemporaryDirectory() as directory:
            sidecar = build_export_sidecar(
                quality="balanced",
                decimation_target=150_000,
                vertex_count=len(mesh.vertices),
                face_count=len(mesh.faces),
                adapter="cpu-demo",
            )
            paths = export_all(
                mesh,
                Path(directory),
                stem="mesh",
                export_sidecar=sidecar,
            )
            sidecar_path = paths["export_sidecar"]
            self.assertTrue(sidecar_path.exists())
            payload = json.loads(sidecar_path.read_text(encoding="utf-8"))
            self.assertEqual(payload["export_tier"], "balanced")

    def test_write_export_sidecar_round_trip(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "sample.export.json"
            write_export_sidecar(path, {"export_tier": "high"})
            self.assertEqual(
                json.loads(path.read_text(encoding="utf-8"))["export_tier"],
                "high",
            )


if __name__ == "__main__":
    unittest.main()
