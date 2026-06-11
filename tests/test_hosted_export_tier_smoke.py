from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from imageezgen3d.hosted_golden_smoke import (
    HostedGoldenSmokeResult,
    validate_hosted_export_tier_smoke_record,
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
    def test_validate_export_tier_smoke_record_accepts_two_checks(self) -> None:
        draft = HostedGoldenSmokeResult(
            ok=True,
            run_id="20260524-000000-00000001",
            space_url="https://example.hf.space/",
            adapter_hint="cpu-demo",
            quality="draft",
            issues=(),
            g7_false_neural_guard_ok=True,
        )
        balanced = HostedGoldenSmokeResult(
            ok=True,
            run_id="20260524-000000-00000002",
            space_url="https://example.hf.space/",
            adapter_hint="cpu-demo",
            quality="balanced",
            issues=(),
            g7_false_neural_guard_ok=True,
        )
        payload = {"checks": [draft.to_dict(), balanced.to_dict()]}
        self.assertEqual(validate_hosted_export_tier_smoke_record(payload), [])

    def test_validate_export_tier_smoke_record_rejects_missing_g7_field(
        self,
    ) -> None:
        payload = {
            "checks": [
                {
                    "ok": True,
                    "run_id": None,
                    "space_url": "https://example.hf.space/",
                    "adapter_hint": None,
                    "quality": "draft",
                    "issues": [],
                },
                {
                    "ok": True,
                    "run_id": None,
                    "space_url": "https://example.hf.space/",
                    "adapter_hint": None,
                    "quality": "balanced",
                    "issues": [],
                },
            ]
        }
        issues = validate_hosted_export_tier_smoke_record(payload)
        self.assertTrue(
            any("g7_false_neural_guard_ok" in issue for issue in issues),
        )

    def test_verify_export_tier_smoke_record_cli_subprocess(self) -> None:
        draft = HostedGoldenSmokeResult(
            ok=True,
            run_id="20260524-000000-00000001",
            space_url="https://example.hf.space/",
            adapter_hint="cpu-demo",
            quality="draft",
            issues=(),
            g7_false_neural_guard_ok=True,
        )
        balanced = HostedGoldenSmokeResult(
            ok=True,
            run_id="20260524-000000-00000002",
            space_url="https://example.hf.space/",
            adapter_hint="cpu-demo",
            quality="balanced",
            issues=(),
            g7_false_neural_guard_ok=True,
        )
        env = {**os.environ, "PYTHONPATH": "src"}
        with tempfile.TemporaryDirectory() as directory:
            valid_path = Path(directory) / "valid.json"
            valid_path.write_text(
                json.dumps({"checks": [draft.to_dict(), balanced.to_dict()]}),
                encoding="utf-8",
            )
            invalid_path = Path(directory) / "invalid.json"
            invalid_path.write_text(
                json.dumps(
                    {
                        "checks": [
                            draft.to_dict(),
                            {
                                "ok": True,
                                "run_id": None,
                                "space_url": "https://example.hf.space/",
                                "adapter_hint": None,
                                "quality": "balanced",
                                "issues": [],
                            },
                        ]
                    }
                ),
                encoding="utf-8",
            )
            ok_proc = subprocess.run(
                [
                    sys.executable,
                    "scripts/verify_hosted_export_tier_smoke_record.py",
                    str(valid_path),
                ],
                check=False,
                env=env,
                capture_output=True,
                text=True,
            )
            bad_proc = subprocess.run(
                [
                    sys.executable,
                    "scripts/verify_hosted_export_tier_smoke_record.py",
                    str(invalid_path),
                ],
                check=False,
                env=env,
                capture_output=True,
                text=True,
            )
        self.assertEqual(ok_proc.returncode, 0, msg=ok_proc.stderr or ok_proc.stdout)
        self.assertEqual(bad_proc.returncode, 1, msg=bad_proc.stderr or bad_proc.stdout)
        self.assertIn("g7_false_neural_guard_ok", bad_proc.stderr)

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

    def test_validate_run_manifest_balanced_requires_quadric_sidecar(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            manifest_path = Path(directory) / "manifest.json"
            sidecar_path = Path(directory) / "mesh.export.json"
            manifest_path.write_text(
                json.dumps(
                    {
                        "artifacts": {
                            "export_sidecar": str(sidecar_path),
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
            sidecar_path.write_text(
                json.dumps(
                    {
                        "decimation": {
                            "decimation_method": "quadric",
                            "decimation_applied": True,
                        }
                    }
                ),
                encoding="utf-8",
            )
            issues = validate_run_manifest(
                manifest_path,
                quality="balanced",
                expect_raw=True,
                sidecar_path=sidecar_path,
            )
            self.assertEqual(issues, [])

    def test_validate_run_manifest_rejects_non_quadric_sidecar(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            manifest_path = Path(directory) / "manifest.json"
            sidecar_path = Path(directory) / "mesh.export.json"
            manifest_path.write_text(
                json.dumps(
                    {
                        "artifacts": {"export_sidecar": str(sidecar_path)},
                        "parameters": {
                            "decimation_target": 150_000,
                            "raw_exported": True,
                            "decimation_applied": True,
                        },
                    }
                ),
                encoding="utf-8",
            )
            sidecar_path.write_text(
                json.dumps(
                    {"decimation": {"decimation_method": "largest_face_mvp"}}
                ),
                encoding="utf-8",
            )
            issues = validate_run_manifest(
                manifest_path,
                quality="balanced",
                expect_raw=True,
                sidecar_path=sidecar_path,
            )
            self.assertTrue(any("quadric" in issue for issue in issues))

    def test_validate_run_manifest_checks_delivery_formats(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            manifest_path = Path(directory) / "manifest.json"
            sidecar_path = Path(directory) / "mesh.export.json"
            fbx_path = Path(directory) / "mesh.fbx"
            fbx_path.write_text("FBXVersion: 7400\n" + ("x" * 200), encoding="utf-8")
            sidecar_path.write_text(
                json.dumps(
                    {
                        "delivery_formats": {
                            "fbx": {"exported": True, "available": True},
                            "usdz": {"exported": False, "available": False},
                        }
                    }
                ),
                encoding="utf-8",
            )
            manifest_path.write_text(
                json.dumps(
                    {
                        "artifacts": {
                            "export_sidecar": str(sidecar_path),
                            "glb": str(Path(directory) / "mesh.glb"),
                            "fbx": str(fbx_path),
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
            issues = validate_run_manifest(
                manifest_path,
                quality="draft",
                expect_raw=False,
                sidecar_path=sidecar_path,
            )
            self.assertEqual(issues, [])

    def test_validate_run_manifest_requires_fbx_when_delivery_formats_present(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as directory:
            manifest_path = Path(directory) / "manifest.json"
            sidecar_path = Path(directory) / "mesh.export.json"
            sidecar_path.write_text(
                json.dumps(
                    {
                        "delivery_formats": {
                            "fbx": {"exported": True, "available": True},
                            "usdz": {"exported": False, "available": False},
                        }
                    }
                ),
                encoding="utf-8",
            )
            manifest_path.write_text(
                json.dumps(
                    {
                        "artifacts": {
                            "export_sidecar": str(sidecar_path),
                            "glb": str(Path(directory) / "mesh.glb"),
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
            issues = validate_run_manifest(
                manifest_path,
                quality="draft",
                expect_raw=False,
                sidecar_path=sidecar_path,
            )
            self.assertTrue(any("missing fbx" in issue.lower() for issue in issues))

    def test_validate_run_manifest_requires_usdz_when_available(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            manifest_path = Path(directory) / "manifest.json"
            sidecar_path = Path(directory) / "mesh.export.json"
            fbx_path = Path(directory) / "mesh.fbx"
            fbx_path.write_text("FBXVersion: 7400" * 20, encoding="utf-8")
            sidecar_path.write_text(
                json.dumps(
                    {
                        "delivery_formats": {
                            "fbx": {"exported": True, "available": True},
                            "usdz": {"exported": True, "available": True},
                        }
                    }
                ),
                encoding="utf-8",
            )
            manifest_path.write_text(
                json.dumps(
                    {
                        "artifacts": {
                            "export_sidecar": str(sidecar_path),
                            "glb": str(Path(directory) / "mesh.glb"),
                            "fbx": str(fbx_path),
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
            issues = validate_run_manifest(
                manifest_path,
                quality="draft",
                expect_raw=False,
                sidecar_path=sidecar_path,
            )
            self.assertTrue(any("missing usdz" in issue.lower() for issue in issues))


if __name__ == "__main__":
    unittest.main()
