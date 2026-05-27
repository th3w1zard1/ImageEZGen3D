from __future__ import annotations

import json
import unittest

from imageezgen3d.hunyuan_manifest_parity import (
    HUNYUAN_SAMPLE_MANIFEST,
    load_hunyuan_sample_manifest,
    validate_hunyuan_manifest_parity,
)


class HunyuanManifestParityTests(unittest.TestCase):
    def test_sample_fixture_file_exists(self) -> None:
        self.assertTrue(HUNYUAN_SAMPLE_MANIFEST.is_file())

    def test_sample_manifest_passes_parity_validator(self) -> None:
        payload = load_hunyuan_sample_manifest()
        issues = validate_hunyuan_manifest_parity(payload)
        self.assertEqual(issues, [], issues)

    def test_validator_rejects_missing_export_sidecar(self) -> None:
        payload = load_hunyuan_sample_manifest()
        artifacts = dict(payload["artifacts"])
        del artifacts["export_sidecar"]
        payload = {**payload, "artifacts": artifacts}
        issues = validate_hunyuan_manifest_parity(payload)
        self.assertTrue(any("export_sidecar" in issue for issue in issues))

    def test_validator_rejects_cpu_fallback_fields(self) -> None:
        payload = load_hunyuan_sample_manifest()
        parameters = dict(payload["parameters"])
        parameters["fallback_reason"] = "cpu fallback"
        payload = {**payload, "parameters": parameters}
        issues = validate_hunyuan_manifest_parity(payload)
        self.assertTrue(any("fallback_reason" in issue for issue in issues))

    def test_sample_json_is_valid(self) -> None:
        json.loads(HUNYUAN_SAMPLE_MANIFEST.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
