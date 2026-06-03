from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .hunyuan_g7_hosted_neural_record import (
    DEFAULT_G7_HOSTED_NEURAL_RECORD,
    verify_g7_hosted_neural_record_file,
)
from .hunyuan_g9_enablement_evidence_record import (
    DEFAULT_G9_ENABLEMENT_EVIDENCE_RECORD,
    G9EnablementEvidenceAttestation,
    verify_g9_enablement_evidence_record_file,
    write_g9_enablement_evidence_record,
)
from .hunyuan_neural_enablement_artifact_parity import (
    verify_neural_enablement_artifact_files,
)
from .hunyuan_neural_enablement_preflight_bundle import (
    NeuralEnablementPreflightBundleResult,
    run_neural_enablement_preflight_bundle,
)


@dataclass(frozen=True)
class G9EnablementEvidenceBundleResult:
    g9_enablement_preflight_ok: bool
    g9_enablement_evidence_ready: bool
    neural_enablement_ready: bool
    neural_enablement_preflight_ok: bool
    hosted_neural_required: bool
    hosted_neural_ok: bool | None
    record_dir: Path
    neural_enablement: NeuralEnablementPreflightBundleResult
    issues: tuple[str, ...]
    record_path: Path
    record_verify_ok: bool
    parity_ok: bool

    def to_dict(self) -> dict[str, Any]:
        return {
            "g9_enablement_preflight_ok": self.g9_enablement_preflight_ok,
            "g9_enablement_evidence_ready": self.g9_enablement_evidence_ready,
            "neural_enablement_ready": self.neural_enablement_ready,
            "neural_enablement_preflight_ok": self.neural_enablement_preflight_ok,
            "hosted_neural_required": self.hosted_neural_required,
            "hosted_neural_ok": self.hosted_neural_ok,
            "record_dir": str(self.record_dir),
            "record_path": str(self.record_path),
            "record_verify_ok": self.record_verify_ok,
            "parity_ok": self.parity_ok,
            "neural_enablement": self.neural_enablement.to_dict(),
            "issues": list(self.issues),
        }


def _resolve_hosted_neural_ok(
    *,
    directory: Path,
    neural_result: NeuralEnablementPreflightBundleResult,
    require_hosted_neural: bool,
) -> tuple[bool | None, list[str]]:
    issues: list[str] = []
    if neural_result.hosted_neural_requested:
        return neural_result.hosted_neural_ok, issues

    hosted_path = directory / DEFAULT_G7_HOSTED_NEURAL_RECORD
    if not hosted_path.is_file():
        if require_hosted_neural:
            issues.append(f"missing hosted neural record: {hosted_path}")
        return None, issues

    verify_issues = verify_g7_hosted_neural_record_file(hosted_path)
    if verify_issues:
        issues.extend(verify_issues)
        return False, issues

    payload = json.loads(hosted_path.read_text(encoding="utf-8"))
    return bool(payload.get("ok")), issues


def attestation_from_evidence_bundle(
    result: G9EnablementEvidenceBundleResult,
) -> G9EnablementEvidenceAttestation:
    return G9EnablementEvidenceAttestation(
        ok=result.g9_enablement_evidence_ready and result.g9_enablement_preflight_ok,
        g9_enablement_evidence_ready=result.g9_enablement_evidence_ready,
        g9_enablement_preflight_ok=result.g9_enablement_preflight_ok,
        neural_enablement_ready=result.neural_enablement_ready,
        neural_enablement_preflight_ok=result.neural_enablement_preflight_ok,
        hosted_neural_required=result.hosted_neural_required,
        hosted_neural_ok=result.hosted_neural_ok,
        issues=result.issues,
        preflight=result.to_dict(),
    )


def run_g9_enablement_evidence_bundle(
    *,
    record_dir: Path | None = None,
    skip_weight_warm: bool = False,
    live_probe: bool = False,
    space_url: str | None = None,
    sample_path: Path | None = None,
    hosted_neural: bool = False,
    hosted_neural_status_file: Path | None = None,
    hosted_neural_status_text: str | None = None,
    hosted_neural_sample: str | None = None,
    hosted_neural_space_url: str | None = None,
    require_hosted_neural: bool = False,
) -> G9EnablementEvidenceBundleResult:
    directory = (record_dir or Path(".")).resolve()
    neural_result = run_neural_enablement_preflight_bundle(
        record_dir=directory,
        skip_weight_warm=skip_weight_warm,
        live_probe=live_probe,
        space_url=space_url,
        sample_path=sample_path,
        hosted_neural=hosted_neural,
        hosted_neural_status_file=hosted_neural_status_file,
        hosted_neural_status_text=hosted_neural_status_text,
        hosted_neural_sample=hosted_neural_sample,
        hosted_neural_space_url=hosted_neural_space_url,
    )

    issues: list[str] = list(neural_result.issues)
    if not neural_result.neural_enablement_preflight_ok:
        issues.append("hunyuan_neural_enablement_preflight_bundle failed")

    hosted_neural_ok, hosted_issues = _resolve_hosted_neural_ok(
        directory=directory,
        neural_result=neural_result,
        require_hosted_neural=require_hosted_neural or hosted_neural,
    )
    issues.extend(hosted_issues)

    hosted_required = require_hosted_neural or hosted_neural
    if hosted_required and hosted_neural_ok is not True:
        issues.append("hosted_neural_not_ready")

    evidence_ready = (
        neural_result.neural_enablement_ready
        and neural_result.neural_enablement_preflight_ok
        and (not hosted_required or hosted_neural_ok is True)
    )
    preflight_ok = neural_result.neural_enablement_preflight_ok and not hosted_issues
    record_path = directory / DEFAULT_G9_ENABLEMENT_EVIDENCE_RECORD

    base_result = G9EnablementEvidenceBundleResult(
        g9_enablement_preflight_ok=preflight_ok,
        g9_enablement_evidence_ready=evidence_ready,
        neural_enablement_ready=neural_result.neural_enablement_ready,
        neural_enablement_preflight_ok=neural_result.neural_enablement_preflight_ok,
        hosted_neural_required=hosted_required,
        hosted_neural_ok=hosted_neural_ok,
        record_dir=directory,
        neural_enablement=neural_result,
        issues=tuple(issues),
        record_path=record_path,
        record_verify_ok=True,
        parity_ok=True,
    )
    write_g9_enablement_evidence_record(
        record_path,
        attestation_from_evidence_bundle(base_result),
    )

    verify_issues = verify_g9_enablement_evidence_record_file(record_path)
    if verify_issues:
        issues = list(base_result.issues) + verify_issues

    parity_issues = verify_neural_enablement_artifact_files(directory)
    if parity_issues:
        issues = list(issues) + parity_issues

    preflight_ok_final = preflight_ok and not verify_issues and not parity_issues
    evidence_ready_final = evidence_ready and not verify_issues and not parity_issues

    final_result = G9EnablementEvidenceBundleResult(
        g9_enablement_preflight_ok=preflight_ok_final,
        g9_enablement_evidence_ready=evidence_ready_final,
        neural_enablement_ready=neural_result.neural_enablement_ready,
        neural_enablement_preflight_ok=neural_result.neural_enablement_preflight_ok,
        hosted_neural_required=hosted_required,
        hosted_neural_ok=hosted_neural_ok,
        record_dir=directory,
        neural_enablement=neural_result,
        issues=tuple(issues),
        record_path=record_path,
        record_verify_ok=not verify_issues,
        parity_ok=not parity_issues,
    )
    write_g9_enablement_evidence_record(
        record_path,
        attestation_from_evidence_bundle(final_result),
    )
    return final_result


def format_g9_enablement_evidence_bundle_report(
    result: G9EnablementEvidenceBundleResult,
) -> str:
    lines = [
        "hunyuan_g9_enablement_evidence_bundle_ok=True",
        f"g9_enablement_preflight_ok={result.g9_enablement_preflight_ok}",
        f"g9_enablement_evidence_ready={result.g9_enablement_evidence_ready}",
        f"neural_enablement_ready={result.neural_enablement_ready}",
        f"neural_enablement_preflight_ok={result.neural_enablement_preflight_ok}",
        f"hosted_neural_required={result.hosted_neural_required}",
        f"hosted_neural_ok={result.hosted_neural_ok}",
        f"record_dir={result.record_dir}",
        f"record_path={result.record_path}",
        f"record_verify_ok={result.record_verify_ok}",
        f"parity_ok={result.parity_ok}",
    ]
    for issue in result.issues:
        lines.append(f"issue={issue}")
    return "\n".join(lines) + "\n"


def g9_enablement_evidence_bundle_json(
    result: G9EnablementEvidenceBundleResult,
) -> str:
    return json.dumps(result.to_dict(), indent=2, sort_keys=True) + "\n"
