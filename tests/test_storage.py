from __future__ import annotations

import tempfile
import unittest
import zipfile
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

    def test_list_runs_returns_recent_manifest_summaries(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            store = RunStore(directory)
            run_dir, manifest = store.create_run()
            atomic_write_text(run_dir / "exports" / "draft.glb", "glb")
            atomic_write_text(run_dir / "exports" / "draft.obj", "obj")
            manifest.stage = "done"
            manifest.validation = {"score": 93}
            manifest.parameters = {
                "selected_adapter": "cpu-demo",
                "quality": "balanced",
                "starter_flow": "multi-view-quality",
                "starter_flow_label": "Multi-View Quality",
                "project_brief": "Keep the handle silhouette intact.",
            }
            manifest.artifacts = {
                "manifest": str(run_dir / "manifest.json"),
                "glb": str(run_dir / "exports" / "draft.glb"),
                "obj": str(run_dir / "exports" / "draft.obj"),
            }
            store.save_manifest(run_dir, manifest)

            runs = store.list_runs()

            self.assertEqual(len(runs), 1)
            self.assertEqual(runs[0]["run_id"], manifest.run_id)
            self.assertEqual(runs[0]["adapter"], "cpu-demo")
            self.assertEqual(runs[0]["quality"], "balanced")
            self.assertEqual(runs[0]["score"], 93)
            self.assertEqual(runs[0]["starter_flow"], "Multi-View Quality")
            self.assertEqual(
                runs[0]["project_brief"], "Keep the handle silhouette intact."
            )
            self.assertEqual(
                runs[0]["glb"], str((run_dir / "exports" / "draft.glb").resolve())
            )

    def test_record_artifact_requires_existing_file(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            store = RunStore(directory)
            run_dir, manifest = store.create_run()

            with self.assertRaises(FileNotFoundError):
                store.record_artifact(
                    manifest, "glb", run_dir / "exports" / "missing.glb"
                )

    def test_artifact_value_returns_none_for_missing_file(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            store = RunStore(directory)

            self.assertIsNone(store.artifact_value(Path(directory) / "missing.glb"))

    def test_read_manifest_loads_saved_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            store = RunStore(directory)
            run_dir, manifest = store.create_run()
            manifest.stage = "done"
            store.save_manifest(run_dir, manifest)

            payload = store.read_manifest(manifest.run_id)

            self.assertEqual(payload["run_id"], manifest.run_id)
            self.assertEqual(payload["stage"], "done")

    def test_archive_run_writes_zip_with_run_files(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            store = RunStore(directory)
            run_dir, manifest = store.create_run()
            atomic_write_text(run_dir / "exports" / "mesh.obj", "mesh\n")
            store.save_manifest(run_dir, manifest)

            archive_path = store.archive_run(manifest.run_id)

            self.assertTrue(archive_path.exists())
            with zipfile.ZipFile(archive_path) as bundle:
                names = sorted(bundle.namelist())
            self.assertIn("manifest.json", names)
            self.assertIn("exports/mesh.obj", names)


if __name__ == "__main__":
    unittest.main()
