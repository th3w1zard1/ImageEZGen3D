from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .hunyuan_workstation_enablement_record import (
    WorkstationEnablementAttestation,
    verify_workstation_enablement_record,
)

RECORD_KIND = "hunyuan_g9_workstation_bundle"
DEFAULT_G9_BUNDLE_RECORD = Path("g9-workstation-bundle.json")


@dataclass(frozen=True)
class G9WorkstationBundleAttestation:
    ok: bool
    g9_workstation_bundle_ok: bool
    preflight_bundle_ok: bool
    workstation_record_verify_ok: bool
    workstation_evidence_ready: bool
    issues: tuple[str, ...]
    enablement: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return {
            "record_kind": RECORD_KIND,
            "ok": self.ok,
            "g9_workstation_bundle_ok": self.g9_workstation_bundle_ok,
            "preflight_bundle_ok": self.preflight_bundle_ok,
            "workstation_record_verify_ok": self.workstation_record_verify_ok,
            "workstation_evidence_ready": self.workstation_evidence_ready,
            "issues": list(self.issues),
            "enablement": self.enablement,
        }


def attestation_from_enablement(
    *,
    preflight_bundle_ok: bool,
    workstation_record_verify_ok: bool,
    g9_workstation_bundle_ok: bool,
    workstation_evidence_ready: bool,
    issues: tuple[str, ...],
    attestation: WorkstationEnablementAttestation,
) -> G9WorkstationBundleAttestation:
    return G9WorkstationBundleAttestation(
        ok=workstation_evidence_ready and g9_workstation_bundle_ok,
        g9_workstation_bundle_ok=g9_workstation_bundle_ok,
        preflight_bundle_ok=preflight_bundle_ok,
        workstation_record_verify_ok=workstation_record_verify_ok,
        workstation_evidence_ready=workstation_evidence_ready,
        issues=issues,
        enablement=attestation.to_dict(),
    )


def attestation_json(attestation: G9WorkstationBundleAttestation) -> str:
    return json.dumps(attestation.to_dict(), indent=2, sort_keys=True) + "\n"


def write_g9_workstation_bundle_record(
    path: Path,
    attestation: G9WorkstationBundleAttestation,
) -> Path:
    destination = path.resolve()
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(attestation_json(attestation), encoding="utf-8")
    return destination


def verify_g9_workstation_bundle_record(payload: dict[str, Any]) -> list[str]:
    issues: list[str] = []
    if payload.get("record_kind") != RECORD_KIND:
        issues.append(
            f"record_kind must be {RECORD_KIND!r}, got {payload.get('record_kind')!r}"
        )
    for key in (
        "ok",
        "g9_workstation_bundle_ok",
        "preflight_bundle_ok",
        "workstation_record_verify_ok",
        "workstation_evidence_ready",
        "issues",
        "enablement",
    ):
        if key not in payload:
            issues.append(f"Missing required key: {key}")

    enablement = payload.get("enablement")
    if isinstance(enablement, dict):
        issues.extend(verify_workstation_enablement_record(enablement))
    elif "enablement" in payload:
        issues.append("enablement must be a JSON object")

    if payload.get("g9_workstation_bundle_ok") is True:
        for key in ("preflight_bundle_ok", "workstation_record_verify_ok"):
            if payload.get(key) is not True:
                issues.append(f"g9_workstation_bundle_ok=true requires {key}=true")

    if payload.get("workstation_evidence_ready") is True:
        if payload.get("g9_workstation_bundle_ok") is not True:
            issues.append(
                "workstation_evidence_ready=true requires g9_workstation_bundle_ok=true"
            )
        if isinstance(enablement, dict) and enablement.get("ok") is not True:
            issues.append(
                "workstation_evidence_ready=true requires enablement.ok=true"
            )

    if payload.get("ok") is True:
        for key in (
            "g9_workstation_bundle_ok",
            "preflight_bundle_ok",
            "workstation_record_verify_ok",
            "workstation_evidence_ready",
        ):
            if payload.get(key) is not True:
                issues.append(f"ok=true requires {key}=true")
        if isinstance(enablement, dict) and enablement.get("ok") is not True:
            issues.append("ok=true requires enablement.ok=true")
    return issues


def verify_g9_workstation_bundle_record_file(path: Path) -> list[str]:
    if not path.is_file():
        return [f"missing file: {path}"]
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"invalid JSON: {exc}"]
    if not isinstance(payload, dict):
        return ["record payload must be a JSON object"]
    return verify_g9_workstation_bundle_record(payload)


def verify_g9_workstation_bundle_fixture_files(fixtures_dir: Path) -> list[str]:
    issues: list[str] = []
    paths = sorted(fixtures_dir.glob("g9-workstation-bundle-*.json"))
    if not paths:
        return [f"no g9-workstation-bundle fixtures under {fixtures_dir}"]
    for path in paths:
        issues.extend(verify_g9_workstation_bundle_record_file(path))
    return issues
