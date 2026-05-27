from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .adapters.hunyuan import HunyuanPlaceholderAdapter
from .hunyuan_admission import GateResult, evaluate_admission_gates
from .hunyuan_g7_preflight import G7ReadinessResult, evaluate_g7_readiness
from .hunyuan_g8_preflight import G8EnablementStatus, g8_enablement_for_gates

_ENABLEMENT_CLOSE_GATES = ("G7", "G8", "G9")


@dataclass(frozen=True)
class EnablementPreflightResult:
    """Snapshot before flipping Hunyuan adapter to configured=True."""

    adapter_configured: bool
    g7_readiness: G7ReadinessResult
    g8_enablement: G8EnablementStatus
    g7_readiness_ready: bool
    g8_enablement_documented: bool
    prerequisites_met: bool
    enablement_complete: bool
    blocking_enablement: tuple[str, ...]
    issues: tuple[str, ...]
    gates: tuple[GateResult, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "adapter_configured": self.adapter_configured,
            "g7_readiness": self.g7_readiness.to_dict(),
            "g8_enablement": self.g8_enablement.to_dict(),
            "g7_readiness_ready": self.g7_readiness_ready,
            "g8_enablement_documented": self.g8_enablement_documented,
            "prerequisites_met": self.prerequisites_met,
            "enablement_complete": self.enablement_complete,
            "blocking_enablement": list(self.blocking_enablement),
            "issues": list(self.issues),
            "gates": [
                {
                    "id": gate.gate_id,
                    "title": gate.title,
                    "status": gate.status,
                }
                for gate in self.gates
            ],
        }


def evaluate_enablement_preflight() -> EnablementPreflightResult:
    gates = evaluate_admission_gates()
    configured = HunyuanPlaceholderAdapter().capabilities.configured
    g7 = evaluate_g7_readiness(gates)

    g8_status = g8_enablement_for_gates(gates)
    g8_doc = g8_status.documented
    by_id = {gate.gate_id: gate for gate in gates}
    blocking: list[str] = []
    for gate_id in _ENABLEMENT_CLOSE_GATES:
        gate = by_id.get(gate_id)
        if gate is None:
            blocking.append(f"{gate_id} missing from admission audit")
        elif gate.status != "pass":
            blocking.append(f"{gate_id} [{gate.status.upper()}] {gate.title}")

    issues = list(g7.issues)
    prerequisites_met = g7.ready
    enablement_complete = configured and not blocking and prerequisites_met

    if configured and blocking:
        issues.append(
            "Adapter is configured but gates remain open: "
            + ", ".join(blocking)
        )

    return EnablementPreflightResult(
        adapter_configured=configured,
        g7_readiness=g7,
        g8_enablement=g8_status,
        g7_readiness_ready=g7.ready,
        g8_enablement_documented=g8_doc,
        prerequisites_met=prerequisites_met,
        enablement_complete=enablement_complete,
        blocking_enablement=tuple(blocking),
        issues=tuple(issues),
        gates=gates,
    )


def enablement_preflight_exit_code(
    result: EnablementPreflightResult | None = None,
) -> int:
    """Exit 0 when G1–G6 ready and adapter safely disabled; 1 on regression or unsafe config."""
    snapshot = result if result is not None else evaluate_enablement_preflight()
    if not snapshot.prerequisites_met:
        return 1
    if snapshot.adapter_configured and snapshot.blocking_enablement:
        return 1
    return 0


def format_enablement_preflight_report(result: EnablementPreflightResult) -> str:
    lines = [
        "Hunyuan enablement preflight (does not enable adapter)",
        f"adapter_configured={result.adapter_configured}",
        f"g7_readiness_ready={result.g7_readiness_ready}",
        f"g8_enablement_documented={result.g8_enablement_documented}",
        f"g8_interim_open={result.g8_enablement.interim_open}",
        f"prerequisites_met={result.prerequisites_met}",
        f"enablement_complete={result.enablement_complete}",
        "",
    ]
    if result.blocking_enablement:
        lines.append("Blocking enablement (G7–G9):")
        for item in result.blocking_enablement:
            lines.append(f"  - {item}")
        lines.append("")
    for issue in result.issues:
        lines.append(f"issue={issue}")
    for gate in result.gates:
        lines.append(f"gate={gate.gate_id}:{gate.status}:{gate.title}")
    return "\n".join(lines) + "\n"
