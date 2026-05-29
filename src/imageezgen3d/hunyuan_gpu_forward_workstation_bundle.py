from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .hunyuan_gpu_forward_e2e_attestation import (
    GpuForwardE2eAttestation,
    run_gpu_forward_e2e_attestation,
    verify_gpu_forward_e2e_record_file,
    write_attestation_record,
)
from .hunyuan_gpu_forward_smoke import evaluate_gpu_forward_workstation_readiness

DEFAULT_RECORD_NAME = "gpu-forward-e2e.json"


@dataclass(frozen=True)
class GpuForwardWorkstationBundleResult:
    bundle_ok: bool
    workstation_ready: bool
    evidence_ok: bool
    probe_blockers: tuple[str, ...]
    attestation: GpuForwardE2eAttestation
    record_path: Path | None
    verify_issues: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "bundle_ok": self.bundle_ok,
            "workstation_ready": self.workstation_ready,
            "evidence_ok": self.evidence_ok,
            "probe_blockers": list(self.probe_blockers),
            "attestation": self.attestation.to_dict(),
            "record_path": str(self.record_path) if self.record_path else None,
            "verify_issues": list(self.verify_issues),
        }


def run_gpu_forward_workstation_bundle(
    *,
    record_dir: Path | None = None,
    record_name: str = DEFAULT_RECORD_NAME,
    skip_weight_warm: bool = False,
) -> GpuForwardWorkstationBundleResult:
    """Probe workstation gates, run exports E2E attestation, and verify the record."""
    probe = evaluate_gpu_forward_workstation_readiness(skip_weight_warm=skip_weight_warm)
    attestation = run_gpu_forward_e2e_attestation(
        skip_weight_warm=skip_weight_warm,
        with_exports=True,
    )

    record_path: Path | None = None
    verify_issues: list[str] = []
    if record_dir is not None:
        record_dir.mkdir(parents=True, exist_ok=True)
        record_path = write_attestation_record(
            record_dir / record_name,
            attestation,
        )
        verify_issues = verify_gpu_forward_e2e_record_file(record_path)

    bundle_ok = not verify_issues
    return GpuForwardWorkstationBundleResult(
        bundle_ok=bundle_ok,
        workstation_ready=bool(probe["workstation_ready"]),
        evidence_ok=attestation.ok,
        probe_blockers=tuple(str(item) for item in probe.get("blockers") or []),
        attestation=attestation,
        record_path=record_path,
        verify_issues=tuple(verify_issues),
    )


def format_workstation_bundle_report(result: GpuForwardWorkstationBundleResult) -> str:
    lines = [
        "hunyuan_gpu_forward_workstation_bundle_ok=True",
        f"bundle_ok={result.bundle_ok}",
        f"workstation_ready={result.workstation_ready}",
        f"evidence_ok={result.evidence_ok}",
        f"attempt_status={result.attestation.attempt_status}",
        f"with_exports={result.attestation.with_exports}",
    ]
    if result.probe_blockers:
        lines.append(f"probe_blockers={','.join(result.probe_blockers)}")
    if result.record_path is not None:
        lines.append(f"record_path={result.record_path}")
    for issue in result.verify_issues:
        lines.append(f"verify_issue={issue}")
    return "\n".join(lines) + "\n"


def bundle_json(result: GpuForwardWorkstationBundleResult) -> str:
    return json.dumps(result.to_dict(), indent=2, sort_keys=True) + "\n"


def verify_gpu_forward_e2e_fixture_files(fixtures_dir: Path) -> list[str]:
    issues: list[str] = []
    paths = sorted(fixtures_dir.glob("gpu-forward-e2e-*.json"))
    if not paths:
        return [f"no gpu-forward-e2e fixtures under {fixtures_dir}"]
    for path in paths:
        issues.extend(verify_gpu_forward_e2e_record_file(path))
    return issues
