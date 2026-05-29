from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .hunyuan_gpu_forward_e2e_attestation import (
    RECORD_KIND,
    verify_gpu_forward_e2e_record,
    verify_gpu_forward_e2e_record_file,
)

DEFAULT_EVIDENCE_RECORD = Path("gpu-forward-e2e.json")


@dataclass(frozen=True)
class WorkstationEvidencePreflightResult:
    record_path: Path
    record_present: bool
    record_verify_ok: bool
    workstation_evidence_ok: bool
    with_exports: bool | None
    attempt_status: str | None
    issues: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "record_kind": RECORD_KIND,
            "record_path": str(self.record_path),
            "record_present": self.record_present,
            "record_verify_ok": self.record_verify_ok,
            "workstation_evidence_ok": self.workstation_evidence_ok,
            "with_exports": self.with_exports,
            "attempt_status": self.attempt_status,
            "issues": list(self.issues),
        }


def evaluate_workstation_evidence_preflight(
    record_path: Path | None = None,
) -> WorkstationEvidencePreflightResult:
    """Check optional local gpu-forward-e2e.json without enabling the adapter."""
    path = (record_path or DEFAULT_EVIDENCE_RECORD).resolve()
    if not path.is_file():
        return WorkstationEvidencePreflightResult(
            record_path=path,
            record_present=False,
            record_verify_ok=True,
            workstation_evidence_ok=False,
            with_exports=None,
            attempt_status=None,
            issues=(
                "No local workstation GPU forward evidence record "
                f"(expected optional file: {path})",
            ),
        )

    verify_issues = verify_gpu_forward_e2e_record_file(path)
    if verify_issues:
        return WorkstationEvidencePreflightResult(
            record_path=path,
            record_present=True,
            record_verify_ok=False,
            workstation_evidence_ok=False,
            with_exports=None,
            attempt_status=None,
            issues=tuple(verify_issues),
        )

    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        return WorkstationEvidencePreflightResult(
            record_path=path,
            record_present=True,
            record_verify_ok=False,
            workstation_evidence_ok=False,
            with_exports=None,
            attempt_status=None,
            issues=("record payload must be a JSON object",),
        )

    attestation_issues = verify_gpu_forward_e2e_record(payload)
    evidence_ok = payload.get("ok") is True
    with_exports = payload.get("with_exports")
    attempt_status = payload.get("attempt_status")

    issues: list[str] = list(attestation_issues)
    if not evidence_ok:
        issues.append(
            "workstation_evidence_ok=false "
            f"(attempt_status={attempt_status!r}, ok={payload.get('ok')!r})"
        )
    elif with_exports is not True:
        issues.append(
            "workstation evidence requires with_exports=true for G6 export parity"
        )

    return WorkstationEvidencePreflightResult(
        record_path=path,
        record_present=True,
        record_verify_ok=True,
        workstation_evidence_ok=evidence_ok and with_exports is True and not issues,
        with_exports=with_exports if isinstance(with_exports, bool) else None,
        attempt_status=str(attempt_status) if attempt_status is not None else None,
        issues=tuple(issues),
    )


def workstation_evidence_preflight_exit_code(
    result: WorkstationEvidencePreflightResult | None = None,
) -> int:
    snapshot = result if result is not None else evaluate_workstation_evidence_preflight()
    if snapshot.record_present and not snapshot.record_verify_ok:
        return 1
    return 0


def format_workstation_evidence_preflight_report(
    result: WorkstationEvidencePreflightResult,
) -> str:
    lines = [
        "hunyuan_workstation_evidence_preflight_ok=True",
        f"record_present={result.record_present}",
        f"record_verify_ok={result.record_verify_ok}",
        f"workstation_evidence_ok={result.workstation_evidence_ok}",
    ]
    if result.attempt_status is not None:
        lines.append(f"attempt_status={result.attempt_status}")
    if result.with_exports is not None:
        lines.append(f"with_exports={result.with_exports}")
    lines.append(f"record_path={result.record_path}")
    for issue in result.issues:
        lines.append(f"issue={issue}")
    return "\n".join(lines) + "\n"
