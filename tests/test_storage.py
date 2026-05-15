from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from imageezgen3d.storage import RunStore, atomic_write_text


class StorageTests(unittest.TestCase):
    def test_create_run_and_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            store = RunStore(directory)
            run_dir, manifest = store.create_run()
            self.assertTrue((run_dir / "manifest.json").exists())
            self.assertEqual(manifest.stage, "created")

    def test_atomic_write_text(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "a" / "file.txt"
            atomic_write_text(path, "hello")
            self.assertEqual(path.read_text(encoding="utf-8"), "hello")

    def test_artifact_path_rejects_traversal(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            store = RunStore(directory)
            run_dir, _ = store.create_run()
            path = store.artifact_path(run_dir, "inputs", "../bad.png")
            self.assertTrue(str(path).endswith("bad.png"))


if __name__ == "__main__":
    unittest.main()
