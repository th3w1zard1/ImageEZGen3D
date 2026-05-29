from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .hunyuan_ci_artifact_parity import verify_hunyuan_ci_artifact_parity
from .hunyuan_g9_workstation_bundle_record import (
    DEFAULT_G9_BUNDLE_RECORD,
    verify_g9_workstation_bundle_record,
)
from .hunyuan_workstation_enablement_record import DEFAULT_ENABLEMENT_RECORD

_AUDIT_JSON = "hunyuan-admission-audit.json"
_PREFLIGHT_JSON = "hunyuan-enablement-preflight.json"


def _load_json(path: Path) -> dict[str, Any] | None:
    if not path.is_file():
        return None
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return {"__parse_error__": str(exc)}
    if not isinstance(payload, dict):
        return {"__invalid_payload__": "record payload must be a JSON object"}
    return payload


def verify_g9_workstation_artifact_parity(
    *,
    g9_bundle_payload: dict[str, Any],
    enablement_payload: dict[str, Any],
    audit_payload: dict[str, Any] | None = None,
    admission_preflight_payload: dict[str, Any] | None = None,
) -> list[str]:
    """Return issues when G9 workstation JSON artifacts diverge."""
    issues: list[str] = []
    issues.extend(verify_g9_workstation_bundle_record(g9_bundle_payload))

    nested_enablement = g9_bundle_payload.get("enablement")
    if not isinstance(nested_enablement, dict):
        issues.append("g9 bundle missing enablement object")
    elif nested_enablement != enablement_payload:
        issues.append(
            "enablement mismatch between g9-workstation-bundle.json and "
            "workstation-enablement-preflight.json"
        )

    if audit_payload is not None:
        if audit_payload.get("adapter_configured") is True:
            issues.append(
                "adapter_configured=true in admission audit while G9 workstation "
                "parity verify runs (enablement PR safety guard)"
            )
        if admission_preflight_payload is not None:
            issues.extend(
                verify_hunyuan_ci_artifact_parity(audit_payload, admission_preflight_payload)
            )

    return issues


def verify_g9_workstation_artifact_files(record_dir: Path) -> list[str]:
    directory = record_dir.resolve()
    g9_path = directory / DEFAULT_G9_BUNDLE_RECORD
    enablement_path = directory / DEFAULT_ENABLEMENT_RECORD
    audit_path = directory / _AUDIT_JSON
    preflight_path = directory / _PREFLIGHT_JSON

    issues: list[str] = []
    g9_payload = _load_json(g9_path)
    enablement_payload = _load_json(enablement_path)
    if g9_payload is None:
        issues.append(f"missing file: {g9_path}")
        return issues
    if isinstance(g9_payload.get("__parse_error__"), str):
        issues.append(f"invalid JSON in {g9_path}: {g9_payload['__parse_error__']}")
        return issues
    if enablement_payload is None:
        issues.append(f"missing file: {enablement_path}")
        return issues
    if isinstance(enablement_payload.get("__parse_error__"), str):
        issues.append(
            f"invalid JSON in {enablement_path}: {enablement_payload['__parse_error__']}"
        )
        return issues

    audit_payload = _load_json(audit_path)
    preflight_payload = _load_json(preflight_path)
    if audit_payload is not None and isinstance(audit_payload.get("__parse_error__"), str):
        issues.append(f"invalid JSON in {audit_path}: {audit_payload['__parse_error__']}")
        audit_payload = None
    if preflight_payload is not None and isinstance(
        preflight_payload.get("__parse_error__"), str
    ):
        issues.append(
            f"invalid JSON in {preflight_path}: {preflight_payload['__parse_error__']}"
        )
        preflight_payload = None

    issues.extend(
        verify_g9_workstation_artifact_parity(
            g9_bundle_payload=g9_payload,
            enablement_payload=enablement_payload,
            audit_payload=audit_payload,
            admission_preflight_payload=preflight_payload,
        )
    )
    return issues
