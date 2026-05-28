from __future__ import annotations

from typing import Any

from .adapters.hunyuan import resolve_hunyuan_configured
from .hunyuan_admission import GateResult, evaluate_admission_gates
from .hunyuan_g7_preflight import evaluate_g7_readiness
from .hunyuan_g8_preflight import g8_enablement_for_gates


def build_admission_audit_payload(
    gates: tuple[GateResult, ...] | None = None,
) -> dict[str, Any]:
    """Machine-readable Hunyuan admission audit snapshot for CI artifacts."""
    results = gates if gates is not None else evaluate_admission_gates()
    readiness = evaluate_g7_readiness(results)
    g8_enablement = g8_enablement_for_gates(results)
    return {
        "adapter_configured": resolve_hunyuan_configured(),
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
