from __future__ import annotations

import unittest
from pathlib import Path


class WorkflowContractTests(unittest.TestCase):
    def test_hosted_golden_smoke_uses_preflight_bundle(self) -> None:
        source = Path(".github/workflows/hosted-golden-smoke.yml").read_text(
            encoding="utf-8"
        )
        self.assertIn("hunyuan_preflight_bundle.py", source)
        self.assertIn("hunyuan_preflight_bundle.py --json", source)
        self.assertIn("hunyuan-admission-audit.json", source)
        self.assertIn("hunyuan-enablement-preflight.json", source)

    def test_ci_workflow_runs_admission_audit_job(self) -> None:
        source = Path(".github/workflows/ci.yml").read_text(encoding="utf-8")
        self.assertIn("hunyuan-admission-audit:", source)
        self.assertIn("hunyuan_preflight_bundle.py", source)
        self.assertNotIn("hunyuan_preflight_bundle.py --json", source)
        self.assertIn("hunyuan_g7_preflight.py", source)

    def test_hosted_golden_smoke_workflow_runs_g7_preflight(self) -> None:
        source = Path(".github/workflows/hosted-golden-smoke.yml").read_text(
            encoding="utf-8"
        )
        self.assertIn("hunyuan_g7_preflight.py", source)

    def test_hosted_golden_smoke_workflow_records_json_artifact(self) -> None:
        source = Path(".github/workflows/hosted-golden-smoke.yml").read_text(
            encoding="utf-8"
        )
        self.assertIn("hosted_golden_smoke.py", source)
        self.assertIn("--json", source)
        self.assertIn("hosted-golden-smoke.json", source)
        self.assertIn("verify_hosted_golden_smoke_record.py", source)

    def test_hosted_golden_smoke_workflow_verifies_export_tier_record(self) -> None:
        source = Path(".github/workflows/hosted-golden-smoke.yml").read_text(
            encoding="utf-8"
        )
        self.assertIn("hosted_export_tier_smoke.py", source)
        self.assertIn("hosted-export-tier-smoke.json", source)
        self.assertIn("verify_hosted_export_tier_smoke_record.py", source)


if __name__ == "__main__":
    unittest.main()
