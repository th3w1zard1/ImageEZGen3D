from __future__ import annotations

import unittest

from imageezgen3d.credits import (
    CreditEstimate,
    apply_credit_estimate_to_parameters,
    credit_chip_label,
    estimate_credits,
    estimate_job_request,
)
from imageezgen3d.jobs.models import JobRequest


class CreditEstimateTests(unittest.TestCase):
    def test_text_preview_meshy6_default(self) -> None:
        estimate = estimate_credits(
            {"input_modality": "text", "lane": "preview", "ai_model": "latest"}
        )
        self.assertEqual(estimate.consumed_credits, 20)

    def test_text_refine_cost(self) -> None:
        estimate = estimate_credits({"input_modality": "text", "lane": "refine"})
        self.assertEqual(estimate.consumed_credits, 10)

    def test_image_with_texture(self) -> None:
        estimate = estimate_credits(
            {
                "input_modality": "image",
                "lane": "refine",
                "enable_pbr": True,
            }
        )
        self.assertEqual(estimate.consumed_credits, 30)

    def test_print_analyze_free(self) -> None:
        estimate = estimate_credits({"input_modality": "print-analyze"})
        self.assertEqual(estimate.consumed_credits, 0)

    def test_unwrap_uv_mesh_op_cost(self) -> None:
        estimate = estimate_credits({"input_modality": "unwrap-uv"})
        self.assertEqual(estimate.consumed_credits, 1)
        self.assertEqual(estimate.task_label, "UV Unwrap")

    def test_boolean_union_mesh_op_cost(self) -> None:
        estimate = estimate_credits({"input_modality": "boolean-union"})
        self.assertEqual(estimate.consumed_credits, 1)
        self.assertEqual(estimate.task_label, "Boolean Union")

    def test_creative_lab_lamp_build(self) -> None:
        estimate = estimate_credits(
            {
                "input_modality": "creative-lab",
                "creative_lab_flow": "lamp",
                "creative_lab_stage": "build",
            }
        )
        self.assertEqual(estimate.consumed_credits, 30)

    def test_apply_to_parameters(self) -> None:
        parameters: dict[str, object] = {"input_modality": "remesh"}
        estimate = apply_credit_estimate_to_parameters(parameters)
        self.assertIsInstance(estimate, CreditEstimate)
        self.assertEqual(parameters["consumed_credits"], 5)
        self.assertEqual(parameters["credit_estimate"]["task_label"], "Remesh")

    def test_job_request_estimate(self) -> None:
        estimate = estimate_job_request(
            JobRequest(input_modality="animate", action_id="Walking_man")
        )
        self.assertEqual(estimate.consumed_credits, 3)

    def test_credit_chip_label(self) -> None:
        label = credit_chip_label({"consumed_credits": 20, "credit_estimate": {"task_label": "Image to 3D (without texture)"}})
        self.assertIn("20 credits", label)
        self.assertIn("Image to 3D", label)


if __name__ == "__main__":
    unittest.main()
