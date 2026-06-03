from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from imageezgen3d.hunyuan_neural_enablement_artifact_parity import (
    verify_admission_g9_enablement_evidence_bundle_evidence_artifact_parity,
    verify_enablement_neural_artifact_parity,
    verify_g7_hosted_neural_enablement_artifact_parity,
    verify_g7_live_probe_neural_artifact_parity,
    verify_g9_enablement_evidence_admission_artifact_parity,
    verify_g9_enablement_evidence_neural_artifact_parity,
    verify_neural_enablement_artifact_files,
    verify_neural_enablement_artifact_parity,
)

FIXTURES = Path(__file__).resolve().parent / "fixtures"


def _ready_neural_payload() -> dict:
    payload = json.loads(
        (FIXTURES / "neural-enablement-preflight-skipped.json").read_text(encoding="utf-8")
    )
    payload["ok"] = True
    payload["neural_enablement_ready"] = True
    payload["neural_enablement_preflight_ok"] = True
    payload["neural_forward_ready"] = True
    payload["g7_enablement_ready"] = True
    payload["issues"] = []
    preflight = payload["preflight"]
    preflight["neural_enablement_ready"] = True
    preflight["neural_enablement_preflight_ok"] = True
    preflight["neural_forward_ready"] = True
    preflight["g7_enablement_ready"] = True
    preflight["issues"] = []
    preflight["configured_inference"]["neural_forward_ready"] = True
    preflight["configured_inference"]["expected_outcome"] = "neural_forward_attempt"
    nested_g7 = preflight["g7_enablement"]
    nested_g7["g7_enablement_ready"] = True
    nested_g7["workstation_evidence_ready"] = True
    nested_g7["g9_preflight"]["workstation_evidence_ready"] = True
    return payload


def _ready_evidence_payload(*, neural_payload: dict) -> dict:
    return {
        "record_kind": "hunyuan_g9_enablement_evidence",
        "ok": True,
        "g9_enablement_evidence_ready": True,
        "g9_enablement_preflight_ok": True,
        "neural_enablement_ready": neural_payload["neural_enablement_ready"],
        "neural_enablement_preflight_ok": neural_payload["neural_enablement_preflight_ok"],
        "hosted_neural_required": False,
        "hosted_neural_ok": None,
        "issues": [],
        "preflight": {},
    }


class HunyuanNeuralEnablementArtifactParityTests(unittest.TestCase):
    def test_verify_passes_for_matching_fixtures(self) -> None:
        neural_payload = json.loads(
            (FIXTURES / "neural-enablement-preflight-skipped.json").read_text(
                encoding="utf-8"
            )
        )
        g9_payload = json.loads(
            (FIXTURES / "g9-workstation-bundle-skipped.json").read_text(encoding="utf-8")
        )
        issues = verify_neural_enablement_artifact_parity(
            neural_payload=neural_payload,
            g9_bundle_payload=g9_payload,
        )
        self.assertEqual(issues, [])

    def test_verify_fails_on_workstation_evidence_mismatch(self) -> None:
        neural_payload = json.loads(
            (FIXTURES / "neural-enablement-preflight-skipped.json").read_text(
                encoding="utf-8"
            )
        )
        g9_payload = json.loads(
            (FIXTURES / "g9-workstation-bundle-ready.json").read_text(encoding="utf-8")
        )
        issues = verify_neural_enablement_artifact_parity(
            neural_payload=neural_payload,
            g9_bundle_payload=g9_payload,
        )
        self.assertTrue(
            any("workstation_evidence_ready mismatch" in issue for issue in issues)
        )

    def test_verify_files_from_record_dir(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            record_dir = Path(directory)
            neural_payload = json.loads(
                (FIXTURES / "neural-enablement-preflight-skipped.json").read_text(
                    encoding="utf-8"
                )
            )
            (record_dir / "neural-enablement-preflight.json").write_text(
                json.dumps(neural_payload),
                encoding="utf-8",
            )
            (record_dir / "g9-workstation-bundle.json").write_text(
                (FIXTURES / "g9-workstation-bundle-skipped.json").read_text(
                    encoding="utf-8"
                ),
                encoding="utf-8",
            )
            enablement_payload = {
                "g7_readiness": neural_payload["preflight"]["g7_enablement"][
                    "g7_readiness"
                ],
                "prerequisites_met": True,
            }
            (record_dir / "hunyuan-enablement-preflight.json").write_text(
                json.dumps(enablement_payload),
                encoding="utf-8",
            )
            issues = verify_neural_enablement_artifact_files(record_dir)
            self.assertEqual(issues, [])

    def test_verify_enablement_neural_g7_mismatch(self) -> None:
        neural_payload = json.loads(
            (FIXTURES / "neural-enablement-preflight-skipped.json").read_text(
                encoding="utf-8"
            )
        )
        enablement_payload = {
            "g7_readiness": {"ready": True, "issues": [], "gates": []},
        }
        issues = verify_enablement_neural_artifact_parity(
            enablement_payload=enablement_payload,
            neural_payload=neural_payload,
        )
        self.assertTrue(any("g7_readiness mismatch" in issue for issue in issues))

    def test_verify_g7_live_probe_neural_passes_for_matching_fixtures(self) -> None:
        neural_payload = json.loads(
            (FIXTURES / "neural-enablement-preflight-skipped.json").read_text(
                encoding="utf-8"
            )
        )
        live_probe_payload = json.loads(
            (FIXTURES / "hunyuan-g7-live-probe-skipped.json").read_text(encoding="utf-8")
        )
        issues = verify_g7_live_probe_neural_artifact_parity(
            live_probe_payload=live_probe_payload,
            neural_payload=neural_payload,
        )
        self.assertEqual(issues, [])

    def test_verify_g7_live_probe_neural_g7_mismatch(self) -> None:
        neural_payload = json.loads(
            (FIXTURES / "neural-enablement-preflight-skipped.json").read_text(
                encoding="utf-8"
            )
        )
        live_probe_payload = json.loads(
            (FIXTURES / "hunyuan-g7-live-probe-skipped.json").read_text(encoding="utf-8")
        )
        live_probe_payload["readiness"] = {"ready": False, "issues": ["x"], "gates": []}
        issues = verify_g7_live_probe_neural_artifact_parity(
            live_probe_payload=live_probe_payload,
            neural_payload=neural_payload,
        )
        self.assertTrue(any("g7_readiness mismatch" in issue for issue in issues))

    def test_verify_files_includes_optional_live_probe(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            record_dir = Path(directory)
            neural_payload = json.loads(
                (FIXTURES / "neural-enablement-preflight-skipped.json").read_text(
                    encoding="utf-8"
                )
            )
            (record_dir / "neural-enablement-preflight.json").write_text(
                json.dumps(neural_payload),
                encoding="utf-8",
            )
            (record_dir / "g9-workstation-bundle.json").write_text(
                (FIXTURES / "g9-workstation-bundle-skipped.json").read_text(
                    encoding="utf-8"
                ),
                encoding="utf-8",
            )
            (record_dir / "hunyuan-enablement-preflight.json").write_text(
                json.dumps(
                    {
                        "g7_readiness": neural_payload["preflight"]["g7_enablement"][
                            "g7_readiness"
                        ],
                    }
                ),
                encoding="utf-8",
            )
            (record_dir / "hunyuan-g7-live-probe.json").write_text(
                (FIXTURES / "hunyuan-g7-live-probe-skipped.json").read_text(
                    encoding="utf-8"
                ),
                encoding="utf-8",
            )
            issues = verify_neural_enablement_artifact_files(record_dir)
            self.assertEqual(issues, [])

    def test_verify_hosted_neural_enablement_passes_when_ready(self) -> None:
        hosted_payload = json.loads(
            (FIXTURES / "hunyuan-g7-hosted-neural-pass.json").read_text(encoding="utf-8")
        )
        neural_payload = _ready_neural_payload()
        issues = verify_g7_hosted_neural_enablement_artifact_parity(
            hosted_neural_payload=hosted_payload,
            neural_payload=neural_payload,
        )
        self.assertEqual(issues, [])

    def test_verify_hosted_neural_enablement_fails_when_neural_not_ready(
        self,
    ) -> None:
        hosted_payload = json.loads(
            (FIXTURES / "hunyuan-g7-hosted-neural-pass.json").read_text(encoding="utf-8")
        )
        neural_payload = json.loads(
            (FIXTURES / "neural-enablement-preflight-skipped.json").read_text(
                encoding="utf-8"
            )
        )
        issues = verify_g7_hosted_neural_enablement_artifact_parity(
            hosted_neural_payload=hosted_payload,
            neural_payload=neural_payload,
        )
        self.assertTrue(
            any("neural_enablement_ready=true" in issue for issue in issues)
        )

    def test_verify_files_includes_optional_hosted_neural(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            record_dir = Path(directory)
            neural_payload = _ready_neural_payload()
            (record_dir / "neural-enablement-preflight.json").write_text(
                json.dumps(neural_payload),
                encoding="utf-8",
            )
            (record_dir / "g9-workstation-bundle.json").write_text(
                (FIXTURES / "g9-workstation-bundle-ready.json").read_text(
                    encoding="utf-8"
                ),
                encoding="utf-8",
            )
            (record_dir / "hunyuan-enablement-preflight.json").write_text(
                json.dumps(
                    {
                        "g7_readiness": neural_payload["preflight"]["g7_enablement"][
                            "g7_readiness"
                        ],
                    }
                ),
                encoding="utf-8",
            )
            (record_dir / "hunyuan-g7-hosted-neural.json").write_text(
                (FIXTURES / "hunyuan-g7-hosted-neural-pass.json").read_text(
                    encoding="utf-8"
                ),
                encoding="utf-8",
            )
            issues = verify_neural_enablement_artifact_files(record_dir)
            self.assertEqual(issues, [])

    def test_verify_g9_evidence_neural_passes_when_ready(self) -> None:
        neural_payload = _ready_neural_payload()
        evidence_payload = _ready_evidence_payload(neural_payload=neural_payload)
        issues = verify_g9_enablement_evidence_neural_artifact_parity(
            evidence_payload=evidence_payload,
            neural_payload=neural_payload,
        )
        self.assertEqual(issues, [])

    def test_verify_g9_evidence_neural_fails_when_neural_not_ready(self) -> None:
        evidence_payload = _ready_evidence_payload(
            neural_payload=_ready_neural_payload()
        )
        neural_payload = json.loads(
            (FIXTURES / "neural-enablement-preflight-skipped.json").read_text(
                encoding="utf-8"
            )
        )
        issues = verify_g9_enablement_evidence_neural_artifact_parity(
            evidence_payload=evidence_payload,
            neural_payload=neural_payload,
        )
        self.assertTrue(
            any("neural_enablement_ready=true" in issue for issue in issues)
        )

    def test_verify_files_includes_optional_g9_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            record_dir = Path(directory)
            neural_payload = _ready_neural_payload()
            (record_dir / "neural-enablement-preflight.json").write_text(
                json.dumps(neural_payload),
                encoding="utf-8",
            )
            (record_dir / "g9-workstation-bundle.json").write_text(
                (FIXTURES / "g9-workstation-bundle-ready.json").read_text(
                    encoding="utf-8"
                ),
                encoding="utf-8",
            )
            (record_dir / "hunyuan-enablement-preflight.json").write_text(
                json.dumps(
                    {
                        "g7_readiness": neural_payload["preflight"]["g7_enablement"][
                            "g7_readiness"
                        ],
                    }
                ),
                encoding="utf-8",
            )
            (record_dir / "g9-enablement-evidence.json").write_text(
                json.dumps(_ready_evidence_payload(neural_payload=neural_payload)),
                encoding="utf-8",
            )
            issues = verify_neural_enablement_artifact_files(record_dir)
            self.assertEqual(issues, [])

    def test_verify_g9_evidence_admission_passes_when_adapter_disabled(self) -> None:
        neural_payload = _ready_neural_payload()
        evidence_payload = _ready_evidence_payload(neural_payload=neural_payload)
        audit_payload = {
            "adapter_configured": False,
            "g7_readiness": neural_payload["preflight"]["g7_enablement"]["g7_readiness"],
            "g8_enablement": {},
        }
        preflight_payload = {
            "g7_readiness": audit_payload["g7_readiness"],
            "g8_enablement": {},
        }
        issues = verify_g9_enablement_evidence_admission_artifact_parity(
            evidence_payload=evidence_payload,
            audit_payload=audit_payload,
            admission_preflight_payload=preflight_payload,
        )
        self.assertEqual(issues, [])

    def test_verify_g9_evidence_admission_fails_when_adapter_configured(self) -> None:
        evidence_payload = _ready_evidence_payload(neural_payload=_ready_neural_payload())
        issues = verify_g9_enablement_evidence_admission_artifact_parity(
            evidence_payload=evidence_payload,
            audit_payload={"adapter_configured": True},
        )
        self.assertTrue(any("adapter_configured=true" in issue for issue in issues))

    def test_verify_admission_g9_bundle_evidence_passes_when_nested_matches(self) -> None:
        evidence_payload = json.loads(
            (FIXTURES / "g9-enablement-evidence-skipped.json").read_text(encoding="utf-8")
        )
        bundle_payload = json.loads(
            (
                FIXTURES / "admission-g9-enablement-evidence-bundle-skipped.json"
            ).read_text(encoding="utf-8")
        )
        bundle_payload["evidence"] = evidence_payload
        bundle_payload["g9_enablement_evidence_ready"] = evidence_payload[
            "g9_enablement_evidence_ready"
        ]
        bundle_payload["g9_enablement_preflight_ok"] = evidence_payload[
            "g9_enablement_preflight_ok"
        ]
        issues = verify_admission_g9_enablement_evidence_bundle_evidence_artifact_parity(
            bundle_payload=bundle_payload,
            evidence_payload=evidence_payload,
        )
        self.assertEqual(issues, [])

    def test_verify_admission_g9_bundle_evidence_fails_when_nested_differs(self) -> None:
        evidence_payload = json.loads(
            (FIXTURES / "g9-enablement-evidence-skipped.json").read_text(encoding="utf-8")
        )
        bundle_payload = json.loads(
            (
                FIXTURES / "admission-g9-enablement-evidence-bundle-skipped.json"
            ).read_text(encoding="utf-8")
        )
        mismatched_evidence = dict(evidence_payload)
        mismatched_evidence["g9_enablement_evidence_ready"] = True
        bundle_payload["evidence"] = mismatched_evidence
        issues = verify_admission_g9_enablement_evidence_bundle_evidence_artifact_parity(
            bundle_payload=bundle_payload,
            evidence_payload=evidence_payload,
        )
        self.assertTrue(
            any("evidence mismatch between admission-g9-enablement-evidence-bundle.json" in issue for issue in issues)
        )

    def test_verify_files_includes_optional_g9_evidence_and_audit(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            record_dir = Path(directory)
            neural_payload = _ready_neural_payload()
            (record_dir / "neural-enablement-preflight.json").write_text(
                json.dumps(neural_payload),
                encoding="utf-8",
            )
            (record_dir / "g9-workstation-bundle.json").write_text(
                (FIXTURES / "g9-workstation-bundle-ready.json").read_text(
                    encoding="utf-8"
                ),
                encoding="utf-8",
            )
            g7_readiness = neural_payload["preflight"]["g7_enablement"]["g7_readiness"]
            (record_dir / "hunyuan-enablement-preflight.json").write_text(
                json.dumps({"g7_readiness": g7_readiness, "g8_enablement": {}}),
                encoding="utf-8",
            )
            (record_dir / "g9-enablement-evidence.json").write_text(
                json.dumps(_ready_evidence_payload(neural_payload=neural_payload)),
                encoding="utf-8",
            )
            (record_dir / "hunyuan-admission-audit.json").write_text(
                json.dumps(
                    {
                        "adapter_configured": False,
                        "g7_readiness": g7_readiness,
                        "g8_enablement": {},
                    }
                ),
                encoding="utf-8",
            )
            evidence_payload = _ready_evidence_payload(neural_payload=neural_payload)
            bundle_payload = {
                "record_kind": "hunyuan_admission_g9_enablement_evidence_bundle",
                "ok": evidence_payload["ok"],
                "admission_preflight_ok": True,
                "admission_g9_enablement_evidence_ok": True,
                "g9_enablement_evidence_ready": evidence_payload["g9_enablement_evidence_ready"],
                "g9_enablement_preflight_ok": evidence_payload["g9_enablement_preflight_ok"],
                "parity_ok": True,
                "issues": evidence_payload["issues"],
                "evidence": evidence_payload,
            }
            (record_dir / "admission-g9-enablement-evidence-bundle.json").write_text(
                json.dumps(bundle_payload),
                encoding="utf-8",
            )
            issues = verify_neural_enablement_artifact_files(record_dir)
            self.assertEqual(issues, [])

    def test_verify_artifact_parity_script(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            record_dir = Path(directory)
            neural_payload = json.loads(
                (FIXTURES / "neural-enablement-preflight-skipped.json").read_text(
                    encoding="utf-8"
                )
            )
            (record_dir / "neural-enablement-preflight.json").write_text(
                json.dumps(neural_payload),
                encoding="utf-8",
            )
            (record_dir / "g9-workstation-bundle.json").write_text(
                (FIXTURES / "g9-workstation-bundle-skipped.json").read_text(
                    encoding="utf-8"
                ),
                encoding="utf-8",
            )
            (record_dir / "hunyuan-enablement-preflight.json").write_text(
                json.dumps(
                    {
                        "g7_readiness": neural_payload["preflight"]["g7_enablement"][
                            "g7_readiness"
                        ],
                    }
                ),
                encoding="utf-8",
            )
            result = subprocess.run(
                [
                    sys.executable,
                    "scripts/verify_neural_enablement_artifact_parity.py",
                    "--record-dir",
                    str(record_dir),
                ],
                check=False,
                capture_output=True,
                text=True,
                env={**__import__("os").environ, "PYTHONPATH": "src"},
            )
            self.assertEqual(result.returncode, 0, msg=result.stderr or result.stdout)


if __name__ == "__main__":
    unittest.main()
