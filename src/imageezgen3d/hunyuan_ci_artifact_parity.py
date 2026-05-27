from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def verify_hunyuan_ci_artifact_parity(
    audit_payload: dict[str, Any],
    preflight_payload: dict[str, Any],
) -> list[str]:
    """Return human-readable issues when scheduled CI Hunyuan JSON artifacts diverge."""
    issues: list[str] = []
    audit_g7 = audit_payload.get("g7_readiness")
    preflight_g7 = preflight_payload.get("g7_readiness")
    if audit_g7 != preflight_g7:
        issues.append("g7_readiness mismatch between admission audit and enablement preflight")

    audit_g8 = audit_payload.get("g8_enablement")
    preflight_g8 = preflight_payload.get("g8_enablement")
    if audit_g8 != preflight_g8:
        issues.append("g8_enablement mismatch between admission audit and enablement preflight")

    return issues


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def verify_hunyuan_ci_artifact_files(
    audit_path: Path,
    preflight_path: Path,
) -> list[str]:
    if not audit_path.is_file():
        return [f"Missing admission audit record: {audit_path}"]
    if not preflight_path.is_file():
        return [f"Missing enablement preflight record: {preflight_path}"]
    return verify_hunyuan_ci_artifact_parity(
        load_json(audit_path),
        load_json(preflight_path),
    )
