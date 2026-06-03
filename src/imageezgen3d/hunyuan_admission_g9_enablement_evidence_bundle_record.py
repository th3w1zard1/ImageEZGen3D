from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .hunyuan_g9_enablement_evidence_record import verify_g9_enablement_evidence_record

RECORD_KIND = "hunyuan_admission_g9_enablement_evidence_bundle"
DEFAULT_ADMISSION_G9_ENABLEMENT_EVIDENCE_BUNDLE_RECORD = Path(
    "admission-g9-enablement-evidence-bundle.json"
)


@dataclass(frozen=True)
class AdmissionG9EnablementEvidenceBundleAttestation:
    ok: bool
    admission_g9_enablement_evidence_ok: bool
    admission_preflight_ok: bool
    g9_enablement_evidence_ready: bool
    g9_enablement_preflight_ok: bool
    parity_ok: bool
    issues: tuple[str, ...]
    evidence: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return {
            "record_kind": RECORD_KIND,
            "ok": self.ok,
            "admission_g9_enablement_evidence_ok": self.admission_g9_enablement_evidence_ok,
            "admission_preflight_ok": self.admission_preflight_ok,
            "g9_enablement_evidence_ready": self.g9_enablement_evidence_ready,
            "g9_enablement_preflight_ok": self.g9_enablement_preflight_ok,
            "parity_ok": self.parity_ok,
            "issues": list(self.issues),
            "evidence": self.evidence,
        }


def attestation_from_bundle(
    *,
    admission_preflight_ok: bool,
    admission_g9_enablement_evidence_ok: bool,
    g9_enablement_evidence_ready: bool,
    g9_enablement_preflight_ok: bool,
    parity_ok: bool,
    issues: tuple[str, ...],
    evidence_payload: dict[str, Any],
) -> AdmissionG9EnablementEvidenceBundleAttestation:
    bundle_ok = admission_g9_enablement_evidence_ok and parity_ok
    ok = bundle_ok and g9_enablement_evidence_ready
    return AdmissionG9EnablementEvidenceBundleAttestation(
        ok=ok,
        admission_g9_enablement_evidence_ok=admission_g9_enablement_evidence_ok,
        admission_preflight_ok=admission_preflight_ok,
        g9_enablement_evidence_ready=g9_enablement_evidence_ready,
        g9_enablement_preflight_ok=g9_enablement_preflight_ok,
        parity_ok=parity_ok,
        issues=issues,
        evidence=evidence_payload,
    )


def attestation_json(attestation: AdmissionG9EnablementEvidenceBundleAttestation) -> str:
    return json.dumps(attestation.to_dict(), indent=2, sort_keys=True) + "\n"


def write_admission_g9_enablement_evidence_bundle_record(
    path: Path,
    attestation: AdmissionG9EnablementEvidenceBundleAttestation,
) -> Path:
    destination = path.resolve()
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(attestation_json(attestation), encoding="utf-8")
    return destination


def verify_admission_g9_enablement_evidence_bundle_record(
    payload: dict[str, Any],
) -> list[str]:
    issues: list[str] = []
    if payload.get("record_kind") != RECORD_KIND:
        issues.append(
            f"record_kind must be {RECORD_KIND!r}, got {payload.get('record_kind')!r}"
        )
    for key in (
        "ok",
        "admission_g9_enablement_evidence_ok",
        "admission_preflight_ok",
        "g9_enablement_evidence_ready",
        "g9_enablement_preflight_ok",
        "parity_ok",
        "issues",
        "evidence",
    ):
        if key not in payload:
            issues.append(f"Missing required key: {key}")

    evidence = payload.get("evidence")
    if isinstance(evidence, dict):
        issues.extend(verify_g9_enablement_evidence_record(evidence))
    elif "evidence" in payload:
        issues.append("evidence must be a JSON object")

    if payload.get("admission_g9_enablement_evidence_ok") is True:
        for key in ("admission_preflight_ok", "g9_enablement_preflight_ok", "parity_ok"):
            if payload.get(key) is not True:
                issues.append(
                    f"admission_g9_enablement_evidence_ok=true requires {key}=true"
                )

    if payload.get("g9_enablement_evidence_ready") is True:
        if payload.get("admission_g9_enablement_evidence_ok") is not True:
            issues.append(
                "g9_enablement_evidence_ready=true requires "
                "admission_g9_enablement_evidence_ok=true"
            )
        if isinstance(evidence, dict) and evidence.get("g9_enablement_evidence_ready") is not True:
            issues.append(
                "g9_enablement_evidence_ready=true requires evidence."
                "g9_enablement_evidence_ready=true"
            )

    if payload.get("ok") is True:
        for key in (
            "admission_g9_enablement_evidence_ok",
            "admission_preflight_ok",
            "g9_enablement_evidence_ready",
            "g9_enablement_preflight_ok",
            "parity_ok",
        ):
            if payload.get(key) is not True:
                issues.append(f"ok=true requires {key}=true")
        if isinstance(evidence, dict) and evidence.get("ok") is not True:
            issues.append("ok=true requires evidence.ok=true")
    return issues


def verify_admission_g9_enablement_evidence_bundle_record_file(path: Path) -> list[str]:
    if not path.is_file():
        return [f"missing file: {path}"]
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"invalid JSON: {exc}"]
    if not isinstance(payload, dict):
        return ["record payload must be a JSON object"]
    return verify_admission_g9_enablement_evidence_bundle_record(payload)


def verify_admission_g9_enablement_evidence_bundle_fixture_files(
    fixtures_dir: Path,
) -> list[str]:
    issues: list[str] = []
    paths = sorted(fixtures_dir.glob("admission-g9-enablement-evidence-bundle-*.json"))
    if not paths:
        return [
            "no admission-g9-enablement-evidence-bundle fixtures under "
            f"{fixtures_dir}"
        ]
    for path in paths:
        issues.extend(verify_admission_g9_enablement_evidence_bundle_record_file(path))
    return issues
