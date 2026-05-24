from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from imageezgen3d.hosted_golden_smoke import (
    validate_hosted_generate_status,
    validate_run_manifest,
)


def _status_for_quality(quality: str, run_id: str = "20260524-000000-00000000") -> str:
    budgets = {
        "draft": "25,000",
        "balanced": "150,000",
        "high": "500,000",
    }
    return "\n".join(
        [
            f"Run `{run_id}` complete.",
            f"- **Export budget:** up to {budgets[quality]} faces (quality-tier preset)",
            "- **Backend used:** Local CPU Preview",
            "manifest and glb available",
        ]
    )


class HostedExportTierSmokeTests(unittest.TestCase):
    def test_validate_status_accepts_balanced_budget(self) -> None:
        ok, issues, _ = validate_hosted_generate_status(
            _status_for_quality("balanced"),
            quality="balanced",
        )
        self.assertTrue(ok, issues)

    def test_validate_run_manifest_draft(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "manifest.json"
            path.write_text(
                json.dumps(
                    {
                        "artifacts": {
                            "export_sidecar": "/tmp/sidecar.export.json",
                            "glb": "/tmp/mesh.glb",
                        },
                        "parameters": {
                            "decimation_target": 25_000,
                            "raw_exported": False,
                            "decimation_applied": False,
                        },
                    }
                ),
                encoding="utf-8",
            )
            issues = validate_run_manifest(path, quality="draft", expect_raw=False)
            self.assertEqual(issues, [])

    def test_validate_run_manifest_balanced_requires_raw(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "manifest.json"
            path.write_text(
                json.dumps(
                    {
                        "artifacts": {
                            "export_sidecar": "/tmp/sidecar.export.json",
                            "raw_glb": "/tmp/mesh.raw.glb",
                            "glb": "/tmp/mesh.glb",
                        },
                        "parameters": {
                            "decimation_target": 150_000,
                            "raw_exported": True,
                            "decimation_applied": True,
                        },
                    }
                ),
                encoding="utf-8",
            )
            issues = validate_run_manifest(path, quality="balanced", expect_raw=True)
            self.assertEqual(issues, [])


if __name__ == "__main__":
    unittest.main()
