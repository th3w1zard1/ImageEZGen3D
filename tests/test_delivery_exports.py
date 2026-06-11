from __future__ import annotations

import json
import tempfile
import unittest
import zipfile
from pathlib import Path

from imageezgen3d.delivery_exports import (
    BLEND_UNAVAILABLE_NOTES,
    build_delivery_formats_block,
    usd_core_available,
    validate_delivery_formats_manifest,
    write_3mf,
    write_fbx,
    write_usdz,
)
from imageezgen3d.exporters import export_all, make_box_mesh
from imageezgen3d.export_tiers import build_export_sidecar
from imageezgen3d.mesh_checks import inspect_artifacts


class DeliveryExportTests(unittest.TestCase):
    def test_write_fbx_contains_geometry_block(self) -> None:
        mesh = make_box_mesh(1.0, 1.0, 1.0, (0.2, 0.4, 0.6, 1.0))
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "mesh.fbx"
            write_fbx(mesh, path)
            text = path.read_text(encoding="utf-8")
            self.assertIn("FBXVersion", text)
            self.assertIn("Geometry::", text)
            self.assertGreater(path.stat().st_size, 0)

    @unittest.skipUnless(usd_core_available(), "usd-core not installed")
    def test_write_usdz_produces_zip_package(self) -> None:
        mesh = make_box_mesh(1.0, 1.0, 1.0, (0.2, 0.4, 0.6, 1.0))
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "mesh.usdz"
            write_usdz(mesh, path)
            self.assertEqual(path.read_bytes()[:2], b"PK")

    def test_write_3mf_produces_zip_with_model_part(self) -> None:
        mesh = make_box_mesh(1.0, 1.0, 1.0, (0.2, 0.4, 0.6, 1.0))
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "mesh.3mf"
            write_3mf(mesh, path)
            self.assertEqual(path.read_bytes()[:2], b"PK")
            with zipfile.ZipFile(path) as archive:
                names = archive.namelist()
            self.assertIn("3D/3dmodel.model", names)

    def test_export_all_respects_format_subset(self) -> None:
        mesh = make_box_mesh(1.0, 1.0, 1.0, (1.0, 1.0, 1.0, 1.0))
        with tempfile.TemporaryDirectory() as directory:
            paths = export_all(
                mesh,
                Path(directory),
                stem="mesh",
                formats=("glb", "fbx"),
            )
            self.assertIn("glb", paths)
            self.assertIn("fbx", paths)
            self.assertNotIn("obj", paths)
            self.assertNotIn("ply", paths)

    def test_export_all_sidecar_records_delivery_formats(self) -> None:
        mesh = make_box_mesh(1.0, 1.0, 1.0, (1.0, 1.0, 1.0, 1.0))
        with tempfile.TemporaryDirectory() as directory:
            sidecar = build_export_sidecar(
                quality="draft",
                decimation_target=25_000,
                vertex_count=len(mesh.vertices),
                face_count=len(mesh.faces),
                adapter="cpu-demo",
            )
            paths = export_all(
                mesh,
                Path(directory),
                stem="mesh",
                export_sidecar=sidecar,
                formats=("glb", "obj", "fbx", "usdz"),
            )
            payload = json.loads(paths["export_sidecar"].read_text(encoding="utf-8"))
            self.assertIn("delivery_formats", payload)
            self.assertTrue(payload["delivery_formats"]["fbx"]["exported"])
            usdz_block = payload["delivery_formats"]["usdz"]
            if usd_core_available():
                self.assertTrue(usdz_block["exported"])
            else:
                self.assertFalse(usdz_block["available"])

    def test_inspect_artifacts_records_delivery_bytes(self) -> None:
        mesh = make_box_mesh(1.0, 1.0, 1.0, (1.0, 1.0, 1.0, 1.0))
        with tempfile.TemporaryDirectory() as directory:
            paths = export_all(
                mesh,
                Path(directory),
                stem="mesh",
                formats=("glb", "obj", "fbx"),
            )
            report = inspect_artifacts(paths)
            self.assertIn("fbx_bytes", report.metrics)
            self.assertEqual(report.status, "ok")

    def test_build_delivery_formats_block_marks_missing_usd_core(self) -> None:
        block = build_delivery_formats_block(
            adapter="cpu-demo",
            exported_keys={"glb", "fbx"},
            requested_formats=("glb", "fbx", "usdz"),
        )
        self.assertTrue(block["fbx"]["exported"])
        if usd_core_available():
            self.assertTrue(block["usdz"]["available"])
        else:
            self.assertFalse(block["usdz"]["available"])

    def test_build_delivery_formats_block_marks_blend_unavailable(self) -> None:
        block = build_delivery_formats_block(
            adapter="cpu-demo",
            exported_keys={"glb", "3mf"},
            requested_formats=("glb", "3mf", "blend"),
        )
        self.assertTrue(block["3mf"]["exported"])
        self.assertFalse(block["blend"]["available"])
        self.assertFalse(block["blend"]["exported"])
        self.assertIn("Blender", block["blend"]["notes"])
        self.assertEqual(block["blend"]["notes"], BLEND_UNAVAILABLE_NOTES)

    def test_export_all_writes_3mf_when_requested(self) -> None:
        mesh = make_box_mesh(1.0, 1.0, 1.0, (1.0, 1.0, 1.0, 1.0))
        with tempfile.TemporaryDirectory() as directory:
            paths = export_all(
                mesh,
                Path(directory),
                stem="mesh",
                formats=("glb", "3mf"),
            )
            self.assertIn("3mf", paths)
            self.assertEqual(paths["3mf"].read_bytes()[:2], b"PK")
            self.assertNotIn("blend", paths)

    def test_validate_delivery_formats_manifest_requires_exported_artifact(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fbx_path = Path(directory) / "mesh.fbx"
            fbx_path.write_text("FBXVersion", encoding="utf-8")
            issues = validate_delivery_formats_manifest(
                {"fbx": str(fbx_path)},
                {"delivery_formats": {"fbx": {"exported": True}}},
            )
            self.assertEqual(issues, [])

    def test_validate_delivery_formats_manifest_rejects_missing_file(self) -> None:
        issues = validate_delivery_formats_manifest(
            {"fbx": "/tmp/missing-mesh.fbx"},
            {"delivery_formats": {"fbx": {"exported": True}}},
        )
        self.assertTrue(any("missing on disk" in issue for issue in issues))

    def test_validate_delivery_formats_manifest_ignores_legacy_sidecar(self) -> None:
        self.assertEqual(
            validate_delivery_formats_manifest({"glb": "/tmp/mesh.glb"}, {}),
            [],
        )


if __name__ == "__main__":
    unittest.main()
