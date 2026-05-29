from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .hunyuan_workstation_enablement_preflight import (
    WorkstationEnablementPreflightResult,
    run_workstation_enablement_preflight,
)

RECORD_KIND = "hunyuan_workstation_enablement"
DEFAULT_ENABLEMENT_RECORD = Path("workstation-enablement-preflight.json")


@dataclass(frozen=True)
class WorkstationEnablementAttestation:
    ok: bool
    enablement_workstation_ready: bool
    bundle_ok: bool
    workstation_evidence_ok: bool
    workstation_ready: bool
    attempt_status: str | None
    issues: tuple[str, ...]
    bundle: dict[str, Any]
    evidence: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return {
            "record_kind": RECORD_KIND,
            "ok": self.ok,
            "enablement_workstation_ready": self.enablement_workstation_ready,
            "bundle_ok": self.bundle_ok,
            "workstation_evidence_ok": self.workstation_evidence_ok,
            "workstation_ready": self.workstation_ready,
            "attempt_status": self.attempt_status,
            "issues": list(self.issues),
            "bundle": self.bundle,
            "evidence": self.evidence,
        }


def attestation_from_enablement_result(
    result: WorkstationEnablementPreflightResult,
) -> WorkstationEnablementAttestation:
    issues: list[str] = []
    if not result.enablement_workstation_ready:
        issues.append(
            "enablement_workstation_ready=false "
            f"(bundle_ok={result.bundle_ok}, "
            f"workstation_evidence_ok={result.workstation_evidence_ok})"
        )
    for issue in result.evidence.issues:
        if issue not in issues:
            issues.append(issue)

    return WorkstationEnablementAttestation(
        ok=result.enablement_workstation_ready,
        enablement_workstation_ready=result.enablement_workstation_ready,
        bundle_ok=result.bundle_ok,
        workstation_evidence_ok=result.workstation_evidence_ok,
        workstation_ready=result.bundle.workstation_ready,
        attempt_status=result.bundle.attestation.attempt_status,
        issues=tuple(issues),
        bundle=result.bundle.to_dict(),
        evidence=result.evidence.to_dict(),
    )


def run_workstation_enablement_attestation(
    *,
    record_dir: Path | None = None,
    skip_weight_warm: bool = False,
) -> WorkstationEnablementAttestation:
    result = run_workstation_enablement_preflight(
        record_dir=record_dir,
        skip_weight_warm=skip_weight_warm,
    )
    return attestation_from_enablement_result(result)


def attestation_json(attestation: WorkstationEnablementAttestation) -> str:
    return json.dumps(attestation.to_dict(), indent=2, sort_keys=True) + "\n"


def write_enablement_attestation_record(
    path: Path,
    attestation: WorkstationEnablementAttestation,
) -> Path:
    destination = path.resolve()
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(attestation_json(attestation), encoding="utf-8")
    return destination


def verify_workstation_enablement_record(payload: dict[str, Any]) -> list[str]:
    issues: list[str] = []
    if payload.get("record_kind") != RECORD_KIND:
        issues.append(
            f"record_kind must be {RECORD_KIND!r}, got {payload.get('record_kind')!r}"
        )
    for key in (
        "ok",
        "enablement_workstation_ready",
        "bundle_ok",
        "workstation_evidence_ok",
        "workstation_ready",
        "issues",
        "bundle",
        "evidence",
    ):
        if key not in payload:
            issues.append(f"Missing required key: {key}")

    if payload.get("ok") is True:
        for key in (
            "enablement_workstation_ready",
            "bundle_ok",
            "workstation_evidence_ok",
            "workstation_ready",
        ):
            if payload.get(key) is not True:
                issues.append(f"ok=true requires {key}=true")
        if payload.get("attempt_status") != "succeeded":
            issues.append(
                f"ok=true requires attempt_status='succeeded', "
                f"got {payload.get('attempt_status')!r}"
            )
        evidence = payload.get("evidence")
        if isinstance(evidence, dict):
            if evidence.get("workstation_evidence_ok") is not True:
                issues.append("ok=true requires evidence.workstation_evidence_ok=true")
            if evidence.get("with_exports") is not True:
                issues.append("ok=true requires evidence.with_exports=true")
        bundle = payload.get("bundle")
        if isinstance(bundle, dict):
            attestation = bundle.get("attestation")
            if isinstance(attestation, dict) and attestation.get("ok") is not True:
                issues.append("ok=true requires bundle.attestation.ok=true")
    return issues


def verify_workstation_enablement_record_file(path: Path) -> list[str]:
    if not path.is_file():
        return [f"missing file: {path}"]
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"invalid JSON: {exc}"]
    if not isinstance(payload, dict):
        return ["record payload must be a JSON object"]
    return verify_workstation_enablement_record(payload)


def verify_workstation_enablement_fixture_files(fixtures_dir: Path) -> list[str]:
    issues: list[str] = []
    paths = sorted(fixtures_dir.glob("workstation-enablement-*.json"))
    if not paths:
        return [f"no workstation-enablement fixtures under {fixtures_dir}"]
    for path in paths:
        issues.extend(verify_workstation_enablement_record_file(path))
    return issues
