from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

_PRICING_NOTE = (
    "Informational estimate aligned with docs/reference/meshy/pricing.md; "
    "no billing or balance deduction is performed locally."
)

_CREATIVE_LAB_BUILD: dict[str, int] = {
    "keychain": 20,
    "fridge-magnet": 20,
    "figure": 20,
    "lamp": 30,
}
_CREATIVE_LAB_PROTOTYPE = 6


@dataclass(frozen=True)
class CreditEstimate:
    consumed_credits: int
    task_label: str
    pricing_tier: str = "standard"
    note: str = _PRICING_NOTE

    def to_dict(self) -> dict[str, Any]:
        return {
            "consumed_credits": self.consumed_credits,
            "task_label": self.task_label,
            "pricing_tier": self.pricing_tier,
            "note": self.note,
        }


def estimate_credits(parameters: Mapping[str, Any]) -> CreditEstimate:
    modality = str(
        parameters.get("input_modality")
        or parameters.get("task_type")
        or "image"
    ).strip().lower()
    lane = str(parameters.get("lane") or "draft").strip().lower()
    enable_pbr = parameters.get("enable_pbr") is True
    model_type = str(parameters.get("model_type") or "standard").strip().lower()
    ai_model = str(parameters.get("ai_model") or "latest").strip().lower()
    meshy6 = model_type == "lowpoly" or ai_model in ("meshy-6", "latest")

    if modality in ("text", "text-to-3d"):
        if lane == "refine":
            return CreditEstimate(10, "Text to 3D (Refine)", "texture")
        credits = 20 if meshy6 else 5
        return CreditEstimate(credits, "Text to 3D (Preview)", "meshy-6" if meshy6 else "legacy")

    if modality in ("image", "image-to-3d", "multi-image-to-3d"):
        with_texture = enable_pbr or lane == "refine"
        if meshy6:
            credits = 30 if with_texture else 20
            tier = "meshy-6"
        else:
            credits = 15 if with_texture else 5
            tier = "legacy"
        label = "Image to 3D"
        if modality == "multi-image-to-3d":
            label = "Multi Image to 3D"
        suffix = " (with texture)" if with_texture else " (without texture)"
        return CreditEstimate(credits, label + suffix, tier)

    if modality == "retexture":
        return CreditEstimate(10, "Retexture", "texture")

    if modality == "text-to-image":
        return CreditEstimate(3, "Text to Image", "nano-banana")

    if modality == "image-to-image":
        return CreditEstimate(3, "Image to Image", "nano-banana")

    if modality in ("rig", "rigging"):
        return CreditEstimate(5, "Auto-Rigging", "rigging")

    if modality in ("animate", "animation", "animations"):
        return CreditEstimate(3, "Animation", "animation")

    if modality == "remesh":
        return CreditEstimate(5, "Remesh", "mesh-op")

    if modality == "convert":
        return CreditEstimate(1, "Convert", "mesh-op")

    if modality == "resize":
        return CreditEstimate(1, "Resize", "mesh-op")

    if modality == "unwrap-uv":
        return CreditEstimate(1, "UV Unwrap", "mesh-op")

    if modality in ("boolean-union", "boolean-difference", "boolean-intersection"):
        label = {
            "boolean-union": "Boolean Union",
            "boolean-difference": "Boolean Difference",
            "boolean-intersection": "Boolean Intersection",
        }[modality]
        return CreditEstimate(1, label, "mesh-op")

    if modality in ("print-analyze", "analyze-printability"):
        return CreditEstimate(0, "Analyze Printability", "print-free")

    if modality in ("print-repair", "repair-printability"):
        return CreditEstimate(10, "Repair Printability", "print-repair")

    if modality == "creative-lab" or str(parameters.get("task_type", "")).startswith(
        "creative-lab:"
    ):
        flow = str(parameters.get("creative_lab_flow") or "figure").strip().lower()
        stage = str(parameters.get("creative_lab_stage") or "build").strip().lower()
        if stage == "prototype":
            return CreditEstimate(
                _CREATIVE_LAB_PROTOTYPE,
                f"Creative Lab — {flow.replace('-', ' ').title()} (Prototype)",
                "creative-lab",
            )
        build_cost = _CREATIVE_LAB_BUILD.get(flow, 20)
        return CreditEstimate(
            build_cost,
            f"Creative Lab — {flow.replace('-', ' ').title()} (Build)",
            "creative-lab",
        )

    return CreditEstimate(20, "Image to 3D (Preview)", "default")


def estimate_job_request(request: Any) -> CreditEstimate:
    return estimate_credits(
        {
            "input_modality": getattr(request, "input_modality", "image"),
            "lane": getattr(request, "lane", None),
            "enable_pbr": getattr(request, "enable_pbr", None),
            "task_type": getattr(request, "task_type", None),
            "creative_lab_flow": getattr(request, "creative_lab_flow", None),
            "creative_lab_stage": getattr(request, "creative_lab_stage", None),
        }
    )


def apply_credit_estimate_to_parameters(parameters: dict[str, Any]) -> CreditEstimate:
    estimate = estimate_credits(parameters)
    parameters["consumed_credits"] = estimate.consumed_credits
    parameters["credit_estimate"] = estimate.to_dict()
    return estimate


def credit_chip_label(parameters: Mapping[str, Any]) -> str:
    credits = parameters.get("consumed_credits")
    if credits is None:
        estimate = parameters.get("credit_estimate")
        if isinstance(estimate, dict):
            credits = estimate.get("consumed_credits")
    if credits is None:
        credits = estimate_credits(parameters).consumed_credits
    label = parameters.get("credit_estimate", {})
    task = ""
    if isinstance(label, dict):
        task = str(label.get("task_label") or "")
    if task:
        return f"{credits} credits · {task}"
    return f"{credits} credits"


def informational_balance_starting() -> int:
    """Synthetic starting balance for Meshy-shaped /balance responses."""
    return 10_000
