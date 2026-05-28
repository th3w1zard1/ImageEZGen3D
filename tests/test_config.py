from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from imageezgen3d.config import load_config


class ConfigTests(unittest.TestCase):
    def test_load_defaults_when_missing(self) -> None:
        with patch.dict(os.environ, {}, clear=True):
            config = load_config(Path("missing.yaml"))
        self.assertEqual(config.app.title, "ImageEZGen3D")
        self.assertEqual(config.app.adapter, "auto")
        self.assertTrue(config.runtime.prefer_zerogpu)
        self.assertFalse(config.hunyuan.configured)
        self.assertFalse(config.text_neural.configured)
        self.assertIn("glb", config.exports.formats)

    def test_hunyuan_configured_env_override(self) -> None:
        with patch.dict(os.environ, {"IMAGEEZ_HUNYUAN_CONFIGURED": "true"}, clear=True):
            config = load_config(Path("missing.yaml"))
        self.assertTrue(config.hunyuan.configured)

    def test_text_neural_configured_env_override(self) -> None:
        with patch.dict(
            os.environ, {"IMAGEEZ_TEXT_NEURAL_CONFIGURED": "true"}, clear=True
        ):
            config = load_config(Path("missing.yaml"))
        self.assertTrue(config.text_neural.configured)

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
            with patch.dict(os.environ, {}, clear=True):
                config = load_config(path)
            self.assertEqual(config.app.title, "Demo")
            self.assertEqual(config.app.output_dir, Path("out"))
            self.assertEqual(config.exports.formats, ("glb", "obj"))

    def test_requirements_are_self_contained_for_space_builds(self) -> None:
        requirements = Path("requirements.txt").read_text(encoding="utf-8").splitlines()
        lines = [line.strip() for line in requirements if line.strip() and not line.startswith("#")]
        self.assertIn("gradio>=4.44,<7", lines)
        self.assertIn("Pillow>=10.0", lines)
        self.assertIn("numpy>=1.26", lines)
        self.assertNotIn("-e .[app]", lines)

    def test_gradio_server_port_overrides_launch_port(self) -> None:
        with patch.dict(os.environ, {"GRADIO_SERVER_PORT": "7860"}, clear=True):
            config = load_config(Path("missing.yaml"))
        self.assertEqual(config.launch.port, 7860)

    def test_port_env_overrides_gradio_server_port(self) -> None:
        with patch.dict(
            os.environ, {"PORT": "8080", "GRADIO_SERVER_PORT": "7860"}, clear=True
        ):
            config = load_config(Path("missing.yaml"))
        self.assertEqual(config.launch.port, 8080)

    def test_space_runtime_defaults_launch_port_to_7860(self) -> None:
        with patch.dict(os.environ, {"SPACE_ID": "th3w1zard1/ImageEZGen3D"}, clear=True):
            config = load_config(Path("missing.yaml"))
        self.assertEqual(config.launch.port, 7860)

    def test_resolve_output_dir_uses_data_on_space_when_writable(self) -> None:
        from imageezgen3d.config import resolve_output_dir

        with tempfile.TemporaryDirectory() as directory:
            data_root = Path(directory)
            with patch.dict(os.environ, {}, clear=True):
                resolved = resolve_output_dir(
                    configured="outputs",
                    data_root=data_root,
                    space_runtime=True,
                )
            self.assertEqual(resolved, data_root / "outputs")

    def test_resolve_output_dir_honors_explicit_env(self) -> None:
        from imageezgen3d.config import resolve_output_dir

        with patch.dict(os.environ, {"IMAGEEZ_OUTPUT_DIR": "/tmp/runs"}, clear=True):
            resolved = resolve_output_dir(space_runtime=True)
        self.assertEqual(resolved, Path("/tmp/runs"))

    def test_load_config_uses_resolve_output_dir(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            data_root = Path(directory) / "outputs"
            with patch(
                "imageezgen3d.config.resolve_output_dir",
                return_value=data_root,
            ):
                config = load_config(Path("missing.yaml"))
            self.assertEqual(config.app.output_dir, data_root)


if __name__ == "__main__":
    unittest.main()
