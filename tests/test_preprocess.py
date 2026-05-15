from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from PIL import Image

from imageezgen3d.preprocess import normalize_image, save_input_bundle, validate_image


class PreprocessTests(unittest.TestCase):
    def test_validate_image_reports_dimensions(self) -> None:
        image = Image.new("RGBA", (512, 384), (100, 150, 200, 255))
        report = validate_image(image)
        self.assertEqual(report.width, 512)
        self.assertEqual(report.height, 384)
        self.assertGreaterEqual(report.score, 0)

    def test_normalize_image_square_rgb(self) -> None:
        image = Image.new("RGBA", (320, 640), (20, 30, 40, 180))
        normalized = normalize_image(image, size=256)
        self.assertEqual(normalized.size, (256, 256))
        self.assertEqual(normalized.mode, "RGB")

    def test_save_input_bundle(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            image = Image.new("RGBA", (512, 512), (100, 20, 40, 255))
            report = save_input_bundle(
                image, root / "in.png", root / "out.png", root / "report.json"
            )
            self.assertTrue((root / "in.png").exists())
            self.assertTrue((root / "out.png").exists())
            self.assertTrue((root / "report.json").exists())
            self.assertEqual(report.width, 512)


if __name__ == "__main__":
    unittest.main()
