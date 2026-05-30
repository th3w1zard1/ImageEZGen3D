from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

RECORD_KIND = "hunyuan_neural_enablement"
DEFAULT_NEURAL_ENABLEMENT_RECORD = Path("neural-enablement-preflight.json")


@dataclass(frozen=True)
class NeuralEnablementAttestation:
    ok: bool
    neural_enablement_ready: bool
    neural_enablement_preflight_ok: bool
    g7_enablement_ready: bool
    neural_forward_ready: bool
    issues: tuple[str, ...]
    preflight: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return {
            "record_kind": RECORD_KIND,
            "ok": self.ok,
            "neural_enablement_ready": self.neural_enablement_ready,
            "neural_enablement_preflight_ok": self.neural_enablement_preflight_ok,
            "g7_enablement_ready": self.g7_enablement_ready,
            "neural_forward_ready": self.neural_forward_ready,
            "issues": list(self.issues),
            "preflight": self.preflight,
        }


def attestation_json(attestation: NeuralEnablementAttestation) -> str:
    return json.dumps(attestation.to_dict(), indent=2, sort_keys=True) + "\n"


def write_neural_enablement_record(
    path: Path,
    attestation: NeuralEnablementAttestation,
) -> Path:
    destination = path.resolve()
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(attestation_json(attestation), encoding="utf-8")
    return destination


def verify_neural_enablement_record(payload: dict[str, Any]) -> list[str]:
    issues: list[str] = []
    if payload.get("record_kind") != RECORD_KIND:
        issues.append(
            f"record_kind must be {RECORD_KIND!r}, got {payload.get('record_kind')!r}"
        )
    for key in (
        "ok",
        "neural_enablement_ready",
        "neural_enablement_preflight_ok",
        "g7_enablement_ready",
        "neural_forward_ready",
        "issues",
        "preflight",
    ):
        if key not in payload:
            issues.append(f"Missing required key: {key}")

    preflight = payload.get("preflight")
    if not isinstance(preflight, dict) and "preflight" in payload:
        issues.append("preflight must be a JSON object")

    if payload.get("neural_enablement_ready") is True:
        for key in (
            "neural_enablement_preflight_ok",
            "g7_enablement_ready",
            "neural_forward_ready",
        ):
            if payload.get(key) is not True:
                issues.append(
                    f"neural_enablement_ready=true requires {key}=true"
                )

    if payload.get("ok") is True:
        if payload.get("neural_enablement_ready") is not True:
            issues.append("ok=true requires neural_enablement_ready=true")
        if payload.get("neural_enablement_preflight_ok") is not True:
            issues.append("ok=true requires neural_enablement_preflight_ok=true")

    return issues


def verify_neural_enablement_record_file(path: Path) -> list[str]:
    if not path.is_file():
        return [f"missing file: {path}"]
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"invalid JSON: {exc}"]
    if not isinstance(payload, dict):
        return ["record payload must be a JSON object"]
    return verify_neural_enablement_record(payload)


def verify_neural_enablement_fixture_files(fixtures_dir: Path) -> list[str]:
    issues: list[str] = []
    paths = sorted(fixtures_dir.glob("neural-enablement-preflight-*.json"))
    if not paths:
        return [f"no neural-enablement-preflight fixtures under {fixtures_dir}"]
    for path in paths:
        issues.extend(verify_neural_enablement_record_file(path))
    return issues
