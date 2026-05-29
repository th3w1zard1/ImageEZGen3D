from __future__ import annotations

import json
import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .hunyuan_workstation_enablement_record import (
    DEFAULT_ENABLEMENT_RECORD,
    WorkstationEnablementAttestation,
    run_workstation_enablement_attestation,
    verify_workstation_enablement_record_file,
    write_enablement_attestation_record,
)

_AUDIT_JSON = "hunyuan-admission-audit.json"
_PREFLIGHT_JSON = "hunyuan-enablement-preflight.json"


@dataclass(frozen=True)
class G9WorkstationBundleResult:
    preflight_bundle_ok: bool
    workstation_record_verify_ok: bool
    g9_workstation_bundle_ok: bool
    workstation_evidence_ready: bool
    record_path: Path
    attestation: WorkstationEnablementAttestation
    issues: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "preflight_bundle_ok": self.preflight_bundle_ok,
            "workstation_record_verify_ok": self.workstation_record_verify_ok,
            "g9_workstation_bundle_ok": self.g9_workstation_bundle_ok,
            "workstation_evidence_ready": self.workstation_evidence_ready,
            "record_path": str(self.record_path),
            "attestation": self.attestation.to_dict(),
            "issues": list(self.issues),
        }


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _python_env() -> dict[str, str]:
    env = os.environ.copy()
    src = str(_repo_root() / "src")
    existing = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = src if not existing else f"{src}{os.pathsep}{existing}"
    return env


def _run_preflight_bundle(record_dir: Path) -> bool:
    result = subprocess.run(
        [sys.executable, "scripts/hunyuan_preflight_bundle.py", "--record-dir", str(record_dir)],
        cwd=_repo_root(),
        env=_python_env(),
        check=False,
    )
    return result.returncode == 0


def run_g9_workstation_bundle(
    *,
    record_dir: Path | None = None,
    skip_weight_warm: bool = False,
) -> G9WorkstationBundleResult:
    """Run admission preflight bundle plus workstation enablement record verify."""
    directory = (record_dir or Path(".")).resolve()
    directory.mkdir(parents=True, exist_ok=True)
    record_path = directory / DEFAULT_ENABLEMENT_RECORD

    preflight_ok = _run_preflight_bundle(directory)
    attestation = run_workstation_enablement_attestation(
        record_dir=directory,
        skip_weight_warm=skip_weight_warm,
    )
    write_enablement_attestation_record(record_path, attestation)
    verify_issues = verify_workstation_enablement_record_file(record_path)

    issues: list[str] = []
    if not preflight_ok:
        issues.append("hunyuan_preflight_bundle failed")
    issues.extend(verify_issues)

    record_verify_ok = not verify_issues
    bundle_ok = preflight_ok and record_verify_ok
    return G9WorkstationBundleResult(
        preflight_bundle_ok=preflight_ok,
        workstation_record_verify_ok=record_verify_ok,
        g9_workstation_bundle_ok=bundle_ok,
        workstation_evidence_ready=attestation.ok,
        record_path=record_path,
        attestation=attestation,
        issues=tuple(issues),
    )


def format_g9_workstation_bundle_report(result: G9WorkstationBundleResult) -> str:
    lines = [
        "hunyuan_g9_workstation_bundle_ok=True",
        f"preflight_bundle_ok={result.preflight_bundle_ok}",
        f"workstation_record_verify_ok={result.workstation_record_verify_ok}",
        f"g9_workstation_bundle_ok={result.g9_workstation_bundle_ok}",
        f"workstation_evidence_ready={result.workstation_evidence_ready}",
        f"record_path={result.record_path}",
        f"audit_record={result.record_path.parent / _AUDIT_JSON}",
        f"enablement_preflight_record={result.record_path.parent / _PREFLIGHT_JSON}",
    ]
    for issue in result.issues:
        lines.append(f"issue={issue}")
    return "\n".join(lines) + "\n"


def g9_workstation_bundle_json(result: G9WorkstationBundleResult) -> str:
    return json.dumps(result.to_dict(), indent=2, sort_keys=True) + "\n"
