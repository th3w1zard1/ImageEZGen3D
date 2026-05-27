from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from .adapters.hunyuan import HunyuanPlaceholderAdapter
from .hunyuan_manifest_parity import (
    HUNYUAN_SAMPLE_MANIFEST,
    load_hunyuan_sample_manifest,
    validate_hunyuan_manifest_parity,
)

GateStatus = Literal["pass", "open", "fail"]

_REPO_ROOT = Path(__file__).resolve().parents[2]
_LICENSE_AUDIT = _REPO_ROOT / "docs/knowledgebase/license-audit.md"
_WEIGHT_ACCESS = _REPO_ROOT / "docs/knowledgebase/hunyuan-weight-access.md"
_DEPENDENCIES = _REPO_ROOT / "docs/knowledgebase/hunyuan-dependencies.md"
_RESOURCE_FIT = _REPO_ROOT / "docs/knowledgebase/hunyuan-resource-fit.md"
_HUNYUAN_PINS = _REPO_ROOT / "requirements/hunyuan-pins.txt"
_ADMISSION_GATES = _REPO_ROOT / "docs/knowledgebase/hunyuan-admission-gates.md"
_MANIFEST_PARITY = _REPO_ROOT / "docs/knowledgebase/hunyuan-manifest-parity.md"
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


def _g6_sample_manifest_valid() -> bool:
    if not HUNYUAN_SAMPLE_MANIFEST.is_file():
        return False
    try:
        payload = load_hunyuan_sample_manifest()
    except (OSError, ValueError):
        return False
    return not validate_hunyuan_manifest_parity(payload)


def evaluate_admission_gates() -> tuple[GateResult, ...]:
    license_text = _read_text(_LICENSE_AUDIT)
    hosted_text = _read_text(_HOSTED_VALIDATION)
    hunyuan_source = _read_text(_HUNYUAN_ADAPTER)
    requirements_text = _read_text(_REQUIREMENTS)

    weight_text = _read_text(_WEIGHT_ACCESS)
    g1_status: GateStatus = (
        "pass"
        if "G1_STATUS: PASS" in license_text
        and "Hunyuan3D-2.1 audit record" in license_text
        else "open"
    )
    g2_status: GateStatus = (
        "pass"
        if "G2_STATUS: PASS" in weight_text
        and "dry-run" in weight_text.lower()
        else "open"
    )
    deps_text = _read_text(_DEPENDENCIES)
    g3_status: GateStatus = (
        "pass"
        if "G3_STATUS: PASS" in deps_text
        and _HUNYUAN_PINS.is_file()
        and "hunyuan-audit" in deps_text
        else "open"
    )
    g3_evidence = (
        f"hunyuan-dependencies.md present: {_DEPENDENCIES.is_file()}",
        f"requirements/hunyuan-pins.txt present: {_HUNYUAN_PINS.is_file()}",
        "G3_STATUS: PASS"
        if g3_status == "pass"
        else "G3 dependency audit record missing or pins file absent",
    )
    if g3_status == "pass" and "hunyuan" in requirements_text.lower():
        g3_evidence = (
            *g3_evidence,
            "requirements.txt mentions hunyuan — ensure only optional extra, not default install",
        )

    g4_status: GateStatus = (
        "pass"
        if "@spaces.GPU" in hunyuan_source or "spaces.GPU" in hunyuan_source
        else "open"
    )
    resource_text = _read_text(_RESOURCE_FIT)
    g5_status: GateStatus = (
        "pass"
        if "G5_STATUS: PASS" in resource_text
        and "29" in resource_text
        and "14.9" in resource_text
        else "open"
    )
    manifest_parity_text = _read_text(_MANIFEST_PARITY)
    g6_status: GateStatus = (
        "pass"
        if "G6_STATUS: PASS" in manifest_parity_text
        and _g6_sample_manifest_valid()
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
                "G1_STATUS: PASS" if g1_status == "pass" else "G1 audit record missing in license-audit.md",
            ),
        ),
        GateResult(
            "G2",
            "Weight access",
            g2_status,
            (
                f"hunyuan-weight-access.md present: {_WEIGHT_ACCESS.is_file()}",
                "G2_STATUS: PASS"
                if g2_status == "pass"
                else "G2 weight-access record missing in hunyuan-weight-access.md",
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
                "Hunyuan adapter uses spaces.GPU scaffold"
                if g4_status == "pass"
                else "Hunyuan adapter must use @spaces.GPU before enablement",
            ),
        ),
        GateResult(
            "G5",
            "Resource fit",
            g5_status,
            (
                f"hunyuan-resource-fit.md present: {_RESOURCE_FIT.is_file()}",
                "G5_STATUS: PASS"
                if g5_status == "pass"
                else "G5 resource budget not documented",
            ),
        ),
        GateResult(
            "G6",
            "Manifest parity",
            g6_status,
            (
                f"hunyuan-manifest-parity.md present: {_MANIFEST_PARITY.is_file()}",
                f"sample manifest present: {HUNYUAN_SAMPLE_MANIFEST.is_file()}",
                "G6_STATUS: PASS (sample contract)"
                if g6_status == "pass"
                else "Hunyuan sample manifest missing or invalid",
            ),
        ),
        GateResult(
            "G7",
            "Hosted E2E",
            g7_status,
            (
                "No hosted run with real Hunyuan adapter in validation doc",
                "cpu-demo fallback runs documented instead",
                "G7 preflight: scripts/hunyuan_g7_preflight.py (readiness + optional live probe)",
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
