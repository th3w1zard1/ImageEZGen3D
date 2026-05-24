from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from PIL import Image

from imageezgen3d.golden_sample import (
    DEFAULT_SAMPLE_PATH,
    run_golden_sample_attestation,
)


class GoldenSampleTests(unittest.TestCase):
    def test_attestation_succeeds_with_repo_block_sample(self) -> None:
        if not DEFAULT_SAMPLE_PATH.is_file():
            self.skipTest("Block sample asset missing in workspace")

        with tempfile.TemporaryDirectory() as directory:
            attestation = run_golden_sample_attestation(
                output_dir=Path(directory),
            )

        self.assertTrue(attestation.ok, attestation.issues)
        self.assertIsNotNone(attestation.run_id)
        self.assertEqual(attestation.adapter, "cpu-demo")
        self.assertIn("glb", attestation.artifacts)
        self.assertIn("obj", attestation.artifacts)
        self.assertIn("manifest", attestation.artifacts)

    def test_attestation_fails_when_sample_missing(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            attestation = run_golden_sample_attestation(
                sample_path=Path(directory) / "missing.png",
                output_dir=Path(directory) / "out",
            )

        self.assertFalse(attestation.ok)
        self.assertTrue(any("not found" in issue for issue in attestation.issues))

    def test_attestation_fails_when_artifacts_missing(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            sample = Path(directory) / "tiny.png"
            Image.new("RGBA", (64, 64), (10, 20, 30, 255)).save(sample)

            with patch(
                "imageezgen3d.golden_sample.ImageEZOrchestrator.generate",
                return_value={"stage": "done", "run_id": "run-test", "artifacts": {}},
            ):
                attestation = run_golden_sample_attestation(
                    sample_path=sample,
                    output_dir=Path(directory) / "out",
                )

        self.assertFalse(attestation.ok)
        self.assertTrue(
            any("Missing artifact" in issue for issue in attestation.issues)
        )


if __name__ == "__main__":
    unittest.main()
