from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from imageezgen3d.config import load_config


class ConfigTests(unittest.TestCase):
    def test_load_defaults_when_missing(self) -> None:
        config = load_config(Path("missing.yaml"))
        self.assertEqual(config.app.title, "ImageEZGen3D")
        self.assertEqual(config.app.adapter, "auto")
        self.assertTrue(config.runtime.prefer_zerogpu)
        self.assertIn("glb", config.exports.formats)

    def test_load_pyproject_toml(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "pyproject.toml"
            path.write_text(
                "[tool.imageezgen3d.app]\n"
                "title = 'Demo'\n"
                "output_dir = 'out'\n"
                "adapter = 'auto'\n"
                "[tool.imageezgen3d.exports]\n"
                "formats = ['glb', 'obj']\n",
                encoding="utf-8",
            )
            config = load_config(path)
            self.assertEqual(config.app.title, "Demo")
            self.assertEqual(config.app.output_dir, Path("out"))
            self.assertEqual(config.exports.formats, ("glb", "obj"))


if __name__ == "__main__":
    unittest.main()
