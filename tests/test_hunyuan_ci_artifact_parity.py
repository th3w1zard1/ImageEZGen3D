from __future__ import annotations

import unittest

from imageezgen3d.hosted_validation import HOSTED_VALIDATION_PATH, read_repo_text
from imageezgen3d.hunyuan_admission import evaluate_admission_gates
from imageezgen3d.hunyuan_enablement_preflight import evaluate_enablement_preflight
from imageezgen3d.hunyuan_g7_preflight import evaluate_g7_readiness
from imageezgen3d.hunyuan_g8_preflight import evaluate_g8_enablement_status


class HunyuanCiArtifactParityTests(unittest.TestCase):
    def test_g7_readiness_matches_between_preflight_and_admission_gates(self) -> None:
        gates = evaluate_admission_gates()
        preflight = evaluate_enablement_preflight()
        self.assertEqual(
            evaluate_g7_readiness(gates).to_dict(),
            preflight.g7_readiness.to_dict(),
        )

    def test_g8_enablement_matches_between_audit_logic_and_preflight(self) -> None:
        gates = evaluate_admission_gates()
        preflight = evaluate_enablement_preflight()
        g8_gate = next(gate for gate in gates if gate.gate_id == "G8")
        audit_g8 = evaluate_g8_enablement_status(
            read_repo_text(HOSTED_VALIDATION_PATH),
            g8_gate_status=g8_gate.status,
        )
        self.assertEqual(audit_g8.to_dict(), preflight.g8_enablement.to_dict())


if __name__ == "__main__":
    unittest.main()
