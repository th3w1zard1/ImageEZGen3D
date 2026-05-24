from __future__ import annotations

import unittest

from imageezgen3d.adapters.hunyuan import HunyuanPlaceholderAdapter
from imageezgen3d.config import AppConfig
from imageezgen3d.orchestrator import ImageEZOrchestrator


class HunyuanAdmissionTests(unittest.TestCase):
    def test_placeholder_adapter_is_not_configured(self) -> None:
        adapter = HunyuanPlaceholderAdapter()
        self.assertFalse(adapter.capabilities.configured)
        self.assertEqual(adapter.capabilities.name, "hunyuan-zerogpu")

    def test_generate_error_references_admission_gate_doc(self) -> None:
        adapter = HunyuanPlaceholderAdapter()
        with self.assertRaisesRegex(
            RuntimeError, "hunyuan-admission-gates.md"
        ):
            adapter.generate(
                request=type(
                    "Req",
                    (),
                    {
                        "run_dir": None,
                        "primary_image": None,
                        "quality": "draft",
                        "seed": 1,
                    },
                )()
            )

    def test_orchestrator_excludes_unconfigured_hunyuan_from_choices(self) -> None:
        orchestrator = ImageEZOrchestrator(AppConfig())
        self.assertEqual(orchestrator.adapter_choices(), ["auto", "cpu-demo"])
        with self.assertRaisesRegex(ValueError, "not enabled yet"):
            orchestrator.select_adapter("hunyuan-zerogpu")


if __name__ == "__main__":
    unittest.main()
