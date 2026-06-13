from __future__ import annotations

import unittest

from imageezgen3d.config import load_config
from imageezgen3d.gradio_artifact_layout import (
    create_component_name,
    generate_download_index,
    generate_output_indices,
    resolve_gradio_download_keys,
    resolve_ui_delivery_keys,
)


class GradioArtifactLayoutTests(unittest.TestCase):
    def test_default_config_includes_delivery_formats(self) -> None:
        formats = load_config().exports.formats
        delivery = resolve_ui_delivery_keys(formats)
        self.assertIn("fbx", delivery)
        self.assertIn("usdz", delivery)
        self.assertIn("3mf", delivery)

    def test_blend_not_in_download_keys(self) -> None:
        keys = resolve_gradio_download_keys(
            ("glb", "obj", "fbx", "usdz", "3mf", "blend")
        )
        self.assertNotIn("blend", keys)

    def test_create_component_name_for_3mf(self) -> None:
        self.assertEqual(create_component_name("3mf"), "threemf_file")

    def test_generate_indices_include_backend_rail_after_tail(self) -> None:
        formats = load_config().exports.formats
        indices = generate_output_indices(formats)
        download_count = len(resolve_gradio_download_keys(formats))
        self.assertEqual(indices["manifest"], 3)
        self.assertEqual(indices["create_history_summary"], 3 + download_count + 5)
        self.assertEqual(indices["assets_gallery"], 3 + download_count + 6)

    def test_generate_download_index_matches_fbx_slot(self) -> None:
        formats = load_config().exports.formats
        self.assertEqual(
            generate_download_index("fbx", formats),
            generate_output_indices(formats)["fbx"],
        )


if __name__ == "__main__":
    unittest.main()
