from __future__ import annotations

from typing import Any

from .adapters.hunyuan import HunyuanPlaceholderAdapter
from .hosted_validation import HOSTED_VALIDATION_PATH, read_repo_text
from .hunyuan_admission import GateResult, evaluate_admission_gates
from .hunyuan_g7_preflight import evaluate_g7_readiness
from .hunyuan_g8_preflight import evaluate_g8_enablement_status


def build_admission_audit_payload(
    gates: tuple[GateResult, ...] | None = None,
) -> dict[str, Any]:
    """Machine-readable Hunyuan admission audit snapshot for CI artifacts."""
    results = gates if gates is not None else evaluate_admission_gates()
    readiness = evaluate_g7_readiness(results)
    g8_gate = next((gate for gate in results if gate.gate_id == "G8"), None)
    g8_enablement = evaluate_g8_enablement_status(
        read_repo_text(HOSTED_VALIDATION_PATH),
        g8_gate_status=g8_gate.status if g8_gate is not None else None,
    )
    return {
        "adapter_configured": HunyuanPlaceholderAdapter().capabilities.configured,
        "g7_readiness": readiness.to_dict(),
        "g8_enablement": g8_enablement.to_dict(),
        "gates": [
            {
                "id": gate.gate_id,
                "title": gate.title,
                "status": gate.status,
                "evidence": list(gate.evidence),
            }
            for gate in results
        ],
    }
