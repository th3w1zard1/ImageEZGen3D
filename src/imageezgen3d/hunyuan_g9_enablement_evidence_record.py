from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

RECORD_KIND = "hunyuan_g9_enablement_evidence"
DEFAULT_G9_ENABLEMENT_EVIDENCE_RECORD = Path("g9-enablement-evidence.json")


@dataclass(frozen=True)
class G9EnablementEvidenceAttestation:
    ok: bool
    g9_enablement_evidence_ready: bool
    g9_enablement_preflight_ok: bool
    neural_enablement_ready: bool
    neural_enablement_preflight_ok: bool
    hosted_neural_required: bool
    hosted_neural_ok: bool | None
    issues: tuple[str, ...]
    preflight: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return {
            "record_kind": RECORD_KIND,
            "ok": self.ok,
            "g9_enablement_evidence_ready": self.g9_enablement_evidence_ready,
            "g9_enablement_preflight_ok": self.g9_enablement_preflight_ok,
            "neural_enablement_ready": self.neural_enablement_ready,
            "neural_enablement_preflight_ok": self.neural_enablement_preflight_ok,
            "hosted_neural_required": self.hosted_neural_required,
            "hosted_neural_ok": self.hosted_neural_ok,
            "issues": list(self.issues),
            "preflight": self.preflight,
        }


def attestation_json(attestation: G9EnablementEvidenceAttestation) -> str:
    return json.dumps(attestation.to_dict(), indent=2, sort_keys=True) + "\n"


def write_g9_enablement_evidence_record(
    path: Path,
    attestation: G9EnablementEvidenceAttestation,
) -> Path:
    destination = path.resolve()
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(attestation_json(attestation), encoding="utf-8")
    return destination


def verify_g9_enablement_evidence_record(payload: dict[str, Any]) -> list[str]:
    issues: list[str] = []
    if payload.get("record_kind") != RECORD_KIND:
        issues.append(
            f"record_kind must be {RECORD_KIND!r}, got {payload.get('record_kind')!r}"
        )
    for key in (
        "ok",
        "g9_enablement_evidence_ready",
        "g9_enablement_preflight_ok",
        "neural_enablement_ready",
        "neural_enablement_preflight_ok",
        "hosted_neural_required",
        "hosted_neural_ok",
        "issues",
        "preflight",
    ):
        if key not in payload:
            issues.append(f"Missing required key: {key}")

    preflight = payload.get("preflight")
    if not isinstance(preflight, dict) and "preflight" in payload:
        issues.append("preflight must be a JSON object")

    if payload.get("g9_enablement_evidence_ready") is True:
        for key in (
            "g9_enablement_preflight_ok",
            "neural_enablement_ready",
            "neural_enablement_preflight_ok",
        ):
            if payload.get(key) is not True:
                issues.append(
                    f"g9_enablement_evidence_ready=true requires {key}=true"
                )
        if payload.get("hosted_neural_required") is True:
            if payload.get("hosted_neural_ok") is not True:
                issues.append(
                    "g9_enablement_evidence_ready=true requires hosted_neural_ok=true "
                    "when hosted_neural_required=true"
                )

    if payload.get("ok") is True:
        if payload.get("g9_enablement_evidence_ready") is not True:
            issues.append("ok=true requires g9_enablement_evidence_ready=true")
        if payload.get("g9_enablement_preflight_ok") is not True:
            issues.append("ok=true requires g9_enablement_preflight_ok=true")

    return issues


def verify_g9_enablement_evidence_record_file(path: Path) -> list[str]:
    if not path.is_file():
        return [f"missing file: {path}"]
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"invalid JSON: {exc}"]
    if not isinstance(payload, dict):
        return ["record payload must be a JSON object"]
    return verify_g9_enablement_evidence_record(payload)


def verify_g9_enablement_evidence_fixture_files(fixtures_dir: Path) -> list[str]:
    issues: list[str] = []
    paths = sorted(fixtures_dir.glob("g9-enablement-evidence-*.json"))
    if not paths:
        return [f"no g9-enablement-evidence fixtures under {fixtures_dir}"]
    for path in paths:
        issues.extend(verify_g9_enablement_evidence_record_file(path))
    return issues
