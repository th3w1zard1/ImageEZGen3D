from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .hunyuan_g9_workstation_bundle_record import (
    DEFAULT_G9_BUNDLE_RECORD,
    verify_g9_workstation_bundle_record,
)
from .hunyuan_g7_preflight import (
    DEFAULT_G7_LIVE_PROBE_RECORD,
    validate_hunyuan_g7_live_probe_record,
)
from .hunyuan_neural_enablement_record import (
    DEFAULT_NEURAL_ENABLEMENT_RECORD,
    verify_neural_enablement_record,
)

_ENABLEMENT_PREFLIGHT_JSON = "hunyuan-enablement-preflight.json"


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


def verify_neural_enablement_artifact_parity(
    *,
    neural_payload: dict[str, Any],
    g9_bundle_payload: dict[str, Any] | None = None,
) -> list[str]:
    """Return issues when neural and G9 workstation JSON artifacts diverge."""
    issues: list[str] = []
    issues.extend(verify_neural_enablement_record(neural_payload))

    preflight = neural_payload.get("preflight")
    if isinstance(preflight, dict):
        nested_g7 = preflight.get("g7_enablement")
        if isinstance(nested_g7, dict):
            if neural_payload.get("g7_enablement_ready") != nested_g7.get(
                "g7_enablement_ready"
            ):
                issues.append(
                    "g7_enablement_ready mismatch between neural record top-level "
                    "and preflight.g7_enablement"
                )
            nested_ws = nested_g7.get("workstation_evidence_ready")
            if g9_bundle_payload is not None:
                g9_ws = g9_bundle_payload.get("workstation_evidence_ready")
                if g9_ws != nested_ws:
                    issues.append(
                        "workstation_evidence_ready mismatch between "
                        "g9-workstation-bundle.json and "
                        "neural-enablement-preflight.json"
                    )

    if g9_bundle_payload is not None:
        issues.extend(verify_g9_workstation_bundle_record(g9_bundle_payload))
        if neural_payload.get("g7_enablement_ready") is True:
            if g9_bundle_payload.get("workstation_evidence_ready") is not True:
                issues.append(
                    "neural g7_enablement_ready=true requires "
                    "g9 workstation_evidence_ready=true"
                )

    return issues


def verify_enablement_neural_artifact_parity(
    *,
    enablement_payload: dict[str, Any],
    neural_payload: dict[str, Any],
) -> list[str]:
    """Return issues when admission enablement and neural JSON artifacts diverge."""
    issues: list[str] = []
    enablement_g7 = enablement_payload.get("g7_readiness")
    preflight = neural_payload.get("preflight")
    if not isinstance(preflight, dict):
        issues.append("neural record missing preflight object")
        return issues

    nested_g7 = preflight.get("g7_enablement")
    if not isinstance(nested_g7, dict):
        issues.append("neural preflight missing g7_enablement object")
        return issues

    neural_g7 = nested_g7.get("g7_readiness")
    if enablement_g7 != neural_g7:
        issues.append(
            "g7_readiness mismatch between hunyuan-enablement-preflight.json "
            "and neural-enablement-preflight.json"
        )
    return issues


def verify_g7_live_probe_neural_artifact_parity(
    *,
    live_probe_payload: dict[str, Any],
    neural_payload: dict[str, Any],
) -> list[str]:
    """Return issues when G7 live-probe and neural JSON artifacts diverge."""
    issues: list[str] = []
    issues.extend(validate_hunyuan_g7_live_probe_record(live_probe_payload))

    live_readiness = live_probe_payload.get("readiness")
    preflight = neural_payload.get("preflight")
    if not isinstance(preflight, dict):
        issues.append("neural record missing preflight object")
        return issues

    nested_g7 = preflight.get("g7_enablement")
    if not isinstance(nested_g7, dict):
        issues.append("neural preflight missing g7_enablement object")
        return issues

    neural_g7 = nested_g7.get("g7_readiness")
    if live_readiness != neural_g7:
        issues.append(
            "g7_readiness mismatch between hunyuan-g7-live-probe.json "
            "and neural-enablement-preflight.json"
        )
    return issues


def verify_neural_enablement_artifact_files(record_dir: Path) -> list[str]:
    directory = record_dir.resolve()
    neural_path = directory / DEFAULT_NEURAL_ENABLEMENT_RECORD
    g9_path = directory / DEFAULT_G9_BUNDLE_RECORD
    enablement_path = directory / _ENABLEMENT_PREFLIGHT_JSON

    issues: list[str] = []
    neural_payload = _load_json(neural_path)
    if neural_payload is None:
        issues.append(f"missing file: {neural_path}")
        return issues
    if isinstance(neural_payload.get("__parse_error__"), str):
        issues.append(
            f"invalid JSON in {neural_path}: {neural_payload['__parse_error__']}"
        )
        return issues

    g9_payload = _load_json(g9_path)
    if g9_payload is None:
        issues.append(f"missing file: {g9_path}")
        return issues
    if isinstance(g9_payload.get("__parse_error__"), str):
        issues.append(f"invalid JSON in {g9_path}: {g9_payload['__parse_error__']}")
        return issues

    enablement_payload = _load_json(enablement_path)
    if enablement_payload is None:
        issues.append(f"missing file: {enablement_path}")
        return issues
    if isinstance(enablement_payload.get("__parse_error__"), str):
        issues.append(
            f"invalid JSON in {enablement_path}: {enablement_payload['__parse_error__']}"
        )
        return issues

    issues.extend(
        verify_neural_enablement_artifact_parity(
            neural_payload=neural_payload,
            g9_bundle_payload=g9_payload,
        )
    )
    issues.extend(
        verify_enablement_neural_artifact_parity(
            enablement_payload=enablement_payload,
            neural_payload=neural_payload,
        )
    )

    live_probe_path = directory / DEFAULT_G7_LIVE_PROBE_RECORD
    if live_probe_path.is_file():
        live_probe_payload = _load_json(live_probe_path)
        if live_probe_payload is None:
            issues.append(f"missing file: {live_probe_path}")
        elif isinstance(live_probe_payload.get("__parse_error__"), str):
            issues.append(
                f"invalid JSON in {live_probe_path}: "
                f"{live_probe_payload['__parse_error__']}"
            )
        else:
            issues.extend(
                verify_g7_live_probe_neural_artifact_parity(
                    live_probe_payload=live_probe_payload,
                    neural_payload=neural_payload,
                )
            )

    return issues
