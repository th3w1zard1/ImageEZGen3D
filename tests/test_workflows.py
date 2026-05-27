from __future__ import annotations

import unittest
from pathlib import Path


class WorkflowContractTests(unittest.TestCase):
    def test_hosted_golden_smoke_workflow_runs_admission_audit(self) -> None:
        source = Path(".github/workflows/hosted-golden-smoke.yml").read_text(
            encoding="utf-8"
        )
        self.assertIn("hunyuan_admission_audit.py", source)
        self.assertIn("hunyuan-admission-audit.json", source)

    def test_ci_workflow_runs_admission_audit_job(self) -> None:
        source = Path(".github/workflows/ci.yml").read_text(encoding="utf-8")
        self.assertIn("hunyuan-admission-audit:", source)
        self.assertIn("hunyuan_admission_audit.py", source)
        self.assertIn("hunyuan_g7_preflight.py", source)
        self.assertIn("hunyuan_enablement_preflight.py", source)

    def test_hosted_golden_smoke_workflow_runs_g7_preflight(self) -> None:
        source = Path(".github/workflows/hosted-golden-smoke.yml").read_text(
            encoding="utf-8"
        )
        self.assertIn("hunyuan_g7_preflight.py", source)

    def test_hosted_golden_smoke_records_enablement_preflight(self) -> None:
        source = Path(".github/workflows/hosted-golden-smoke.yml").read_text(
            encoding="utf-8"
        )
        self.assertIn("hunyuan_enablement_preflight.py", source)
        self.assertIn("hunyuan-enablement-preflight.json", source)

    def test_hosted_golden_smoke_verifies_ci_artifact_parity(self) -> None:
        source = Path(".github/workflows/hosted-golden-smoke.yml").read_text(
            encoding="utf-8"
        )
        self.assertIn("verify_hunyuan_ci_artifact_parity.py", source)

    def test_ci_hunyuan_job_verifies_ci_artifact_parity(self) -> None:
        source = Path(".github/workflows/ci.yml").read_text(encoding="utf-8")
        self.assertIn("verify_hunyuan_ci_artifact_parity.py", source)
        self.assertIn("--record hunyuan-admission-audit.json", source)


if __name__ == "__main__":
    unittest.main()
