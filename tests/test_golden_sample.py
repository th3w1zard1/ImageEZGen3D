from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from PIL import Image

from imageezgen3d.delivery_exports import usd_core_available
from imageezgen3d.golden_sample import (
    DEFAULT_SAMPLE_PATH,
    resolve_golden_required_artifact_keys,
    run_golden_sample_attestation,
    write_attestation_record,
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
        self.assertIn("export_sidecar", attestation.artifacts)
        self.assertIn("fbx", attestation.artifacts)
        if usd_core_available():
            self.assertIn("usdz", attestation.artifacts)

    def test_resolve_golden_required_artifact_keys_includes_fbx(self) -> None:
        keys = resolve_golden_required_artifact_keys()
        self.assertIn("fbx", keys)
        if usd_core_available():
            self.assertIn("usdz", keys)
        else:
            self.assertNotIn("usdz", keys)

    def test_attestation_fails_when_sample_missing(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            attestation = run_golden_sample_attestation(
                sample_path=Path(directory) / "missing.png",
                output_dir=Path(directory) / "out",
            )

        self.assertFalse(attestation.ok)
        self.assertTrue(any("not found" in issue for issue in attestation.issues))

    def test_write_attestation_record_persists_json(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "golden-attestation.json"
            attestation = run_golden_sample_attestation(
                sample_path=Path(directory) / "missing.png",
                output_dir=Path(directory) / "out",
            )
            write_attestation_record(path, attestation)

            payload = json.loads(path.read_text(encoding="utf-8"))
            self.assertFalse(payload["ok"])
            self.assertTrue(payload["issues"])

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
        self.assertTrue(
            any("fbx" in issue for issue in attestation.issues)
        )


if __name__ == "__main__":
    unittest.main()
