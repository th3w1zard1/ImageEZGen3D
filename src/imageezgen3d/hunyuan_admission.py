from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from .adapters.hunyuan import HunyuanPlaceholderAdapter

GateStatus = Literal["pass", "open", "fail"]

_REPO_ROOT = Path(__file__).resolve().parents[2]
_LICENSE_AUDIT = _REPO_ROOT / "docs/knowledgebase/license-audit.md"
_ADMISSION_GATES = _REPO_ROOT / "docs/knowledgebase/hunyuan-admission-gates.md"
_HOSTED_VALIDATION = (
    _REPO_ROOT / "docs/knowledgebase/40-operational-risk/hosted-validation-2026-05-23.md"
)
_ZEROGPU_RUNTIME = _REPO_ROOT / "docs/knowledgebase/zerogpu-runtime.md"
_HUNYUAN_ADAPTER = _REPO_ROOT / "src/imageezgen3d/adapters/hunyuan.py"
_REQUIREMENTS = _REPO_ROOT / "requirements.txt"


@dataclass(frozen=True)
class GateResult:
    gate_id: str
    title: str
    status: GateStatus
    evidence: tuple[str, ...]


def _read_text(path: Path) -> str:
    if not path.is_file():
        return ""
    return path.read_text(encoding="utf-8")


def _adapter_configured() -> bool:
    return HunyuanPlaceholderAdapter().capabilities.configured


def evaluate_admission_gates() -> tuple[GateResult, ...]:
    license_text = _read_text(_LICENSE_AUDIT)
    hosted_text = _read_text(_HOSTED_VALIDATION)
    hunyuan_source = _read_text(_HUNYUAN_ADAPTER)
    requirements_text = _read_text(_REQUIREMENTS)

    g1_status: GateStatus = (
        "open"
        if "Blocked until explicit audit" in license_text
        or "Blocked until" in license_text
        else "pass"
    )
    g2_status: GateStatus = "open"
    g3_status: GateStatus = "open"
    g3_evidence = (
        "requirements.txt has no Hunyuan wheel pins (expected while blocked)",
    )
    if "hunyuan" in requirements_text.lower():
        g3_evidence = (
            "Hunyuan-related dependency present in requirements.txt without audit closure",
        )

    g4_status: GateStatus = (
        "pass"
        if "@spaces.GPU" in hunyuan_source or "spaces.GPU" in hunyuan_source
        else "open"
    )
    g5_status: GateStatus = "open"
    g6_status: GateStatus = (
        "pass"
        if "export_sidecar" in hosted_text and "manifest" in hosted_text
        else "open"
    )
    g7_status: GateStatus = "open"
    g8_status: GateStatus = (
        "pass"
        if "fallback" in hosted_text.lower()
        and "preview disclaimer" in hosted_text.lower()
        else "open"
    )
    configured = _adapter_configured()
    open_gates = sum(
        1
        for status in (
            g1_status,
            g2_status,
            g3_status,
            g4_status,
            g5_status,
            g6_status,
            g7_status,
            g8_status,
        )
        if status != "pass"
    )
    g9_status: GateStatus = (
        "fail"
        if configured and open_gates > 0
        else "pass"
        if not configured
        else "open"
    )

    return (
        GateResult(
            "G1",
            "Legal review",
            g1_status,
            (
                f"license-audit.md present: {_LICENSE_AUDIT.is_file()}",
                "Hunyuan row must move from Blocked to Allowed with revision pins",
            ),
        ),
        GateResult(
            "G2",
            "Weight access",
            g2_status,
            (
                "Document HF gated download + Space secrets plan",
                "hf_cli.py lists dry-run commands; no stored download log in repo",
            ),
        ),
        GateResult(
            "G3",
            "Dependency audit",
            g3_status,
            g3_evidence,
        ),
        GateResult(
            "G4",
            "ZeroGPU wiring",
            g4_status,
            (
                f"zerogpu-runtime.md present: {_ZEROGPU_RUNTIME.is_file()}",
                "Hunyuan adapter must use @spaces.GPU before enablement",
            ),
        ),
        GateResult(
            "G5",
            "Resource fit",
            g5_status,
            ("Benchmark on target Space hardware class not recorded",),
        ),
        GateResult(
            "G6",
            "Manifest parity",
            g6_status,
            (
                "CPU demo manifest/sidecar path validated in hosted-validation doc",
                "Hunyuan sample manifest not attached",
            ),
        ),
        GateResult(
            "G7",
            "Hosted E2E",
            g7_status,
            (
                "No hosted run with real Hunyuan adapter in validation doc",
                "cpu-demo fallback runs documented instead",
            ),
        ),
        GateResult(
            "G8",
            "UX honesty",
            g8_status,
            (
                "Hosted validation references fallback + preview disclaimer",
                "Re-verify after any enablement flip",
            ),
        ),
        GateResult(
            "G9",
            "Enablement PR",
            g9_status,
            (
                f"HunyuanPlaceholderAdapter.configured={configured}",
                "Must remain False until G1–G8 closed with written evidence",
            ),
        ),
    )


def audit_exit_code(gates: tuple[GateResult, ...] | None = None) -> int:
    """Exit 0 when adapter disabled; exit 1 if enabled while gates remain open."""
    results = gates if gates is not None else evaluate_admission_gates()
    if not _adapter_configured():
        return 0
    blocking = [gate for gate in results if gate.status != "pass"]
    return 1 if blocking else 0


def format_admission_report(gates: tuple[GateResult, ...]) -> str:
    lines = [
        "Hunyuan admission gate audit (repo-grounded; does not enable adapter)",
        f"adapter_configured={_adapter_configured()}",
        "",
    ]
    for gate in gates:
        lines.append(f"{gate.gate_id} [{gate.status.upper()}] {gate.title}")
        for item in gate.evidence:
            lines.append(f"  - {item}")
        lines.append("")
    open_count = sum(1 for gate in gates if gate.status == "open")
    fail_count = sum(1 for gate in gates if gate.status == "fail")
    lines.append(
        f"summary: pass={sum(1 for g in gates if g.status == 'pass')} "
        f"open={open_count} fail={fail_count}"
    )
    lines.append(f"admission_doc={_ADMISSION_GATES}")
    return "\n".join(lines).rstrip() + "\n"
