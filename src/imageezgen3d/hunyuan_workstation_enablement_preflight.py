from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .hunyuan_gpu_forward_workstation_bundle import (
    GpuForwardWorkstationBundleResult,
    run_gpu_forward_workstation_bundle,
)
from .hunyuan_workstation_evidence_preflight import (
    WorkstationEvidencePreflightResult,
    evaluate_workstation_evidence_preflight,
)

DEFAULT_RECORD_NAME = "gpu-forward-e2e.json"


@dataclass(frozen=True)
class WorkstationEnablementPreflightResult:
    bundle_ok: bool
    workstation_evidence_ok: bool
    enablement_workstation_ready: bool
    bundle: GpuForwardWorkstationBundleResult
    evidence: WorkstationEvidencePreflightResult

    def to_dict(self) -> dict[str, Any]:
        return {
            "bundle_ok": self.bundle_ok,
            "workstation_evidence_ok": self.workstation_evidence_ok,
            "enablement_workstation_ready": self.enablement_workstation_ready,
            "bundle": self.bundle.to_dict(),
            "evidence": self.evidence.to_dict(),
        }


def run_workstation_enablement_preflight(
    *,
    record_dir: Path | None = None,
    record_name: str = DEFAULT_RECORD_NAME,
    skip_weight_warm: bool = False,
) -> WorkstationEnablementPreflightResult:
    """Run workstation bundle then evidence preflight on the written record."""
    bundle = run_gpu_forward_workstation_bundle(
        record_dir=record_dir,
        record_name=record_name,
        skip_weight_warm=skip_weight_warm,
    )
    evidence_path = (
        bundle.record_path
        if bundle.record_path is not None
        else (record_dir or Path(".")) / record_name
    )
    evidence = evaluate_workstation_evidence_preflight(evidence_path)
    enablement_ready = (
        bundle.bundle_ok
        and evidence.record_verify_ok
        and evidence.workstation_evidence_ok
    )
    return WorkstationEnablementPreflightResult(
        bundle_ok=bundle.bundle_ok,
        workstation_evidence_ok=evidence.workstation_evidence_ok,
        enablement_workstation_ready=enablement_ready,
        bundle=bundle,
        evidence=evidence,
    )


def workstation_enablement_preflight_exit_code(
    result: WorkstationEnablementPreflightResult | None = None,
) -> int:
    snapshot = (
        result if result is not None else run_workstation_enablement_preflight()
    )
    if not snapshot.bundle.bundle_ok:
        return 1
    if snapshot.evidence.record_present and not snapshot.evidence.record_verify_ok:
        return 1
    return 0


def format_workstation_enablement_preflight_report(
    result: WorkstationEnablementPreflightResult,
) -> str:
    lines = [
        "hunyuan_workstation_enablement_preflight_ok=True",
        f"bundle_ok={result.bundle_ok}",
        f"workstation_evidence_ok={result.workstation_evidence_ok}",
        f"enablement_workstation_ready={result.enablement_workstation_ready}",
        f"workstation_ready={result.bundle.workstation_ready}",
        f"evidence_ok={result.bundle.evidence_ok}",
        f"attempt_status={result.bundle.attestation.attempt_status}",
    ]
    if result.bundle.probe_blockers:
        lines.append(f"probe_blockers={','.join(result.bundle.probe_blockers)}")
    if result.bundle.record_path is not None:
        lines.append(f"record_path={result.bundle.record_path}")
    for issue in result.evidence.issues:
        lines.append(f"evidence_issue={issue}")
    return "\n".join(lines) + "\n"


def enablement_preflight_json(result: WorkstationEnablementPreflightResult) -> str:
    return json.dumps(result.to_dict(), indent=2, sort_keys=True) + "\n"
