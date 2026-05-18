from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from imageezgen3d.hf_cli import hf_cli_status, stage_space_payload


class HfCliTests(unittest.TestCase):
    def test_recommended_commands_include_upload(self) -> None:
        status = hf_cli_status("user/space")
        joined = "\n".join(status.recommended_commands)
        self.assertIn("hf auth whoami", joined)
        self.assertIn(
            "hf repo create user/space --repo-type space --space-sdk gradio --exist-ok",
            joined,
        )
        self.assertIn("hf upload user/space", joined)
        self.assertIn("--exclude='.venv/**'", joined)
        self.assertIn("--exclude='src/imageezgen3d.egg-info/**'", joined)

    def test_stage_space_payload_copies_runtime_files_only(self) -> None:
        with (
            tempfile.TemporaryDirectory() as root_dir,
            tempfile.TemporaryDirectory() as out_dir,
        ):
            root = Path(root_dir)
            (root / "assets" / "examples").mkdir(parents=True)
            (root / "src" / "imageezgen3d").mkdir(parents=True)
            (root / "src" / "imageezgen3d.egg-info").mkdir(parents=True)
            (root / "outputs").mkdir()

            (root / "README.md").write_text(
                "---\ncolorFrom: green\n---\n", encoding="utf-8"
            )
            (root / "app.py").write_text("print('ok')\n", encoding="utf-8")
            (root / "pyproject.toml").write_text(
                "[project]\nname='demo'\n", encoding="utf-8"
            )
            (root / "requirements.txt").write_text("-e .[app]\n", encoding="utf-8")
            (root / "runtime.txt").write_text("python-3.12\n", encoding="utf-8")
            (root / "assets" / "examples" / "sample.txt").write_text(
                "sample\n", encoding="utf-8"
            )
            (root / "src" / "imageezgen3d" / "__init__.py").write_text(
                "\n", encoding="utf-8"
            )
            (root / "src" / "imageezgen3d.egg-info" / "PKG-INFO").write_text(
                "junk\n", encoding="utf-8"
            )
            (root / "outputs" / "manifest.json").write_text("{}\n", encoding="utf-8")

            stage_space_payload(Path(out_dir), workspace_root=root)

            self.assertTrue((Path(out_dir) / "README.md").exists())
            self.assertTrue((Path(out_dir) / "app.py").exists())
            self.assertTrue(
                (Path(out_dir) / "src" / "imageezgen3d" / "__init__.py").exists()
            )
            self.assertTrue(
                (Path(out_dir) / "assets" / "examples" / "sample.txt").exists()
            )
            self.assertFalse((Path(out_dir) / "outputs").exists())
            self.assertFalse((Path(out_dir) / "src" / "imageezgen3d.egg-info").exists())


if __name__ == "__main__":
    unittest.main()
