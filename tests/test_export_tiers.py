from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from imageezgen3d.export_tiers import (
    apply_pbr_stage_from_sidecar,
    build_export_sidecar,
    build_pbr_delivery_block,
    resolve_decimation_target,
)
from imageezgen3d.generation_pipeline import PipelineStageTracker
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
            self.assertIn("pbr_delivery", payload)
            self.assertFalse(payload["pbr_delivery"]["pbr_available"])

    def test_build_pbr_delivery_block_factor_only(self) -> None:
        block = build_pbr_delivery_block(adapter="cpu-demo")
        self.assertFalse(block["pbr_available"])
        self.assertEqual(block["workflow"], "metallic-roughness")
        self.assertEqual(
            set(block["maps"].keys()),
            {"base_color", "normal", "metallic_roughness", "ao"},
        )
        self.assertTrue(all(value is None for value in block["maps"].values()))
        self.assertIn("Factor-only", block["notes"])

    def test_build_pbr_delivery_block_requires_map_paths_when_available(self) -> None:
        block = build_pbr_delivery_block(
            adapter="future-paint",
            pbr_available=True,
            map_paths={"base_color": "maps/base.png"},
        )
        self.assertTrue(block["pbr_available"])
        self.assertEqual(block["maps"]["base_color"], "maps/base.png")

    def test_apply_pbr_stage_from_sidecar_skipped_for_factor_only(self) -> None:
        tracker = PipelineStageTracker()
        sidecar = build_export_sidecar(
            quality="draft",
            decimation_target=25_000,
            vertex_count=8,
            face_count=12,
            adapter="cpu-demo",
        )
        apply_pbr_stage_from_sidecar(tracker, sidecar, adapter="cpu-demo")
        stages = {item["name"]: item for item in tracker.to_list()}
        self.assertEqual(stages["pbr"]["status"], "skipped")
        self.assertIn("Factor-only", stages["pbr"]["notes"])

    def test_apply_pbr_stage_from_sidecar_succeeded_with_maps(self) -> None:
        tracker = PipelineStageTracker()
        sidecar = build_export_sidecar(
            quality="high",
            decimation_target=500_000,
            vertex_count=100,
            face_count=200,
            adapter="paint",
            pbr_available=True,
            pbr_map_paths={"base_color": "exports/base.png"},
        )
        apply_pbr_stage_from_sidecar(tracker, sidecar, adapter="paint")
        stages = {item["name"]: item for item in tracker.to_list()}
        self.assertEqual(stages["pbr"]["status"], "succeeded")
        self.assertEqual(stages["pbr"]["adapter"], "paint")

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
