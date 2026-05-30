from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .hunyuan_g7_preflight import validate_g7_hosted_generate_status

RECORD_KIND = "hunyuan_g7_hosted_neural"
DEFAULT_G7_HOSTED_NEURAL_RECORD = Path("hunyuan-g7-hosted-neural.json")
_HUNYUAN_ADAPTER = "hunyuan-zerogpu"


@dataclass(frozen=True)
class G7HostedNeuralAttestation:
    ok: bool
    g7_status_valid: bool
    run_id: str | None
    status_markdown: str
    sample: str | None
    space_url: str | None
    adapter: str
    issues: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "record_kind": RECORD_KIND,
            "ok": self.ok,
            "g7_status_valid": self.g7_status_valid,
            "run_id": self.run_id,
            "status_markdown": self.status_markdown,
            "sample": self.sample,
            "space_url": self.space_url,
            "adapter": self.adapter,
            "issues": list(self.issues),
        }


def attestation_from_status_markdown(
    status_markdown: str,
    *,
    sample: str | None = None,
    space_url: str | None = None,
) -> G7HostedNeuralAttestation:
    g7_ok, g7_issues, run_id = validate_g7_hosted_generate_status(status_markdown)
    issues = tuple(g7_issues)
    ok = g7_ok and run_id is not None
    attestation_issues = issues
    if g7_ok and run_id is None:
        attestation_issues = (*issues, "missing run id after G7 status validation")
    return G7HostedNeuralAttestation(
        ok=ok,
        g7_status_valid=g7_ok,
        run_id=run_id,
        status_markdown=status_markdown,
        sample=sample,
        space_url=space_url,
        adapter=_HUNYUAN_ADAPTER,
        issues=attestation_issues,
    )


def attestation_json(attestation: G7HostedNeuralAttestation) -> str:
    return json.dumps(attestation.to_dict(), indent=2, sort_keys=True) + "\n"


def write_g7_hosted_neural_record(
    path: Path,
    attestation: G7HostedNeuralAttestation,
) -> Path:
    destination = path.resolve()
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(attestation_json(attestation), encoding="utf-8")
    return destination


def verify_g7_hosted_neural_record(payload: dict[str, Any]) -> list[str]:
    issues: list[str] = []
    if payload.get("record_kind") != RECORD_KIND:
        issues.append(
            f"record_kind must be {RECORD_KIND!r}, got {payload.get('record_kind')!r}"
        )
    for key in (
        "ok",
        "g7_status_valid",
        "run_id",
        "status_markdown",
        "adapter",
        "issues",
    ):
        if key not in payload:
            issues.append(f"Missing required key: {key}")

    status_markdown = payload.get("status_markdown")
    if not isinstance(status_markdown, str) or not status_markdown.strip():
        issues.append("status_markdown must be a non-empty string")
        return issues

    g7_ok, g7_issues, run_id = validate_g7_hosted_generate_status(status_markdown)
    if payload.get("g7_status_valid") is not g7_ok:
        issues.append("g7_status_valid mismatch with validate_g7_hosted_generate_status")
    if payload.get("run_id") != run_id:
        issues.append("run_id mismatch with validate_g7_hosted_generate_status")
    stored_issues = payload.get("issues")
    if not isinstance(stored_issues, list):
        issues.append("issues must be a list")
    elif stored_issues != g7_issues:
        issues.append("issues mismatch with validate_g7_hosted_generate_status")

    if payload.get("ok") is True:
        if payload.get("g7_status_valid") is not True:
            issues.append("ok=true requires g7_status_valid=true")
        if not payload.get("run_id"):
            issues.append("ok=true requires run_id")
        if payload.get("adapter") != _HUNYUAN_ADAPTER:
            issues.append(f"ok=true requires adapter={_HUNYUAN_ADAPTER!r}")

    if payload.get("ok") is True and not g7_ok:
        issues.append("ok=true but status markdown fails G7 validation")

    return issues


def verify_g7_hosted_neural_record_file(path: Path) -> list[str]:
    if not path.is_file():
        return [f"missing file: {path}"]
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"invalid JSON: {exc}"]
    if not isinstance(payload, dict):
        return ["record payload must be a JSON object"]
    return verify_g7_hosted_neural_record(payload)


def verify_g7_hosted_neural_fixture_files(fixtures_dir: Path) -> list[str]:
    issues: list[str] = []
    paths = sorted(fixtures_dir.glob("hunyuan-g7-hosted-neural-*.json"))
    if not paths:
        return [f"no hunyuan-g7-hosted-neural fixtures under {fixtures_dir}"]
    for path in paths:
        issues.extend(verify_g7_hosted_neural_record_file(path))
    return issues
