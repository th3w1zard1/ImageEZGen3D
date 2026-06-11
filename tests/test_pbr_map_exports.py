from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from PIL import Image

from imageezgen3d.adapters.cpu_demo import CpuDemoAdapter
from imageezgen3d.adapters.base import GenerationRequest
from imageezgen3d.export_tiers import build_export_sidecar
from imageezgen3d.pbr_map_exports import (
    PBR_MANIFEST_KEYS,
    REFERENCE_PBR_NOTES,
    pbr_manifest_artifacts,
    resolve_base_color_image,
    write_reference_pbr_maps,
)


class PbrMapExportTests(unittest.TestCase):
    def test_write_reference_pbr_maps_writes_png_quad(self) -> None:
        image = Image.new("RGB", (256, 128), (20, 40, 200))
        with tempfile.TemporaryDirectory() as directory:
            export_dir = Path(directory) / "exports"
            written, sidecar_paths = write_reference_pbr_maps(
                export_dir,
                base_color_image=image,
            )
            self.assertEqual(set(written), set(sidecar_paths))
            for slot, path in written.items():
                self.assertTrue(path.is_file(), slot)
                self.assertEqual(path.read_bytes()[:8], b"\x89PNG\r\n\x1a\n")
                self.assertIn(f"exports/pbr/{path.name}", sidecar_paths[slot])
            manifest_keys = set(pbr_manifest_artifacts(written))
            self.assertEqual(
                manifest_keys,
                set(PBR_MANIFEST_KEYS.values()),
            )

    def test_resolve_base_color_image_from_mesh_color(self) -> None:
        image = resolve_base_color_image((0.25, 0.5, 0.75, 1.0))
        self.assertEqual(image.size, (512, 512))
        self.assertEqual(image.getpixel((0, 0)), (63, 127, 191))

    def test_cpu_demo_sidecar_marks_pbr_available(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            run_dir = Path(directory)
            input_path = run_dir / "input.png"
            Image.new("RGB", (128, 128), (200, 100, 50)).save(input_path)
            processed = run_dir / "processed.png"
            Image.new("RGB", (128, 128), (200, 100, 50)).save(processed)
            request = GenerationRequest(
                run_dir=run_dir,
                processed_image=processed,
                view_images={},
                quality="draft",
                seed=1,
            )
            result = CpuDemoAdapter().generate(request)
            sidecar = json.loads(
                Path(result.artifacts["export_sidecar"]).read_text(encoding="utf-8")
            )
            self.assertTrue(sidecar["pbr_delivery"]["pbr_available"])
            self.assertEqual(sidecar["pbr_delivery"]["notes"], REFERENCE_PBR_NOTES)
            self.assertTrue(
                Path(result.artifacts["pbr_base_color"]).is_file()
            )
            self.assertEqual(
                sidecar["pbr_delivery"]["maps"]["base_color"],
                "exports/pbr/base_color.png",
            )

    def test_build_export_sidecar_accepts_custom_pbr_notes(self) -> None:
        sidecar = build_export_sidecar(
            quality="draft",
            decimation_target=25_000,
            vertex_count=8,
            face_count=12,
            adapter="cpu-demo",
            pbr_available=True,
            pbr_map_paths={"base_color": "exports/pbr/base_color.png"},
            pbr_notes=REFERENCE_PBR_NOTES,
        )
        self.assertEqual(
            sidecar["pbr_delivery"]["notes"],
            REFERENCE_PBR_NOTES,
        )


if __name__ == "__main__":
    unittest.main()
