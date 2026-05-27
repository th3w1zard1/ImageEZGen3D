from __future__ import annotations

import unittest

from imageezgen3d.hunyuan_admission import evaluate_admission_gates
from imageezgen3d.hunyuan_admission_audit import build_admission_audit_payload
from imageezgen3d.hunyuan_enablement_preflight import evaluate_enablement_preflight


class HunyuanCiArtifactParityTests(unittest.TestCase):
    def test_admission_audit_payload_includes_g7_and_g8_blocks(self) -> None:
        payload = build_admission_audit_payload()
        self.assertIn("g7_readiness", payload)
        self.assertIn("g8_enablement", payload)
        self.assertIn("gates", payload)
        self.assertFalse(payload["adapter_configured"])

    def test_g7_readiness_matches_between_preflight_and_audit_payload(self) -> None:
        gates = evaluate_admission_gates()
        preflight = evaluate_enablement_preflight()
        payload = build_admission_audit_payload(gates)
        self.assertEqual(payload["g7_readiness"], preflight.g7_readiness.to_dict())

    def test_g8_enablement_matches_between_audit_payload_and_preflight(self) -> None:
        gates = evaluate_admission_gates()
        preflight = evaluate_enablement_preflight()
        payload = build_admission_audit_payload(gates)
        self.assertEqual(payload["g8_enablement"], preflight.g8_enablement.to_dict())


if __name__ == "__main__":
    unittest.main()
