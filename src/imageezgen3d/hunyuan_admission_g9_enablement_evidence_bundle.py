from __future__ import annotations

import json
import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .hunyuan_admission_g9_enablement_evidence_bundle_record import (
    DEFAULT_ADMISSION_G9_ENABLEMENT_EVIDENCE_BUNDLE_RECORD,
    attestation_from_bundle,
    verify_admission_g9_enablement_evidence_bundle_record_file,
    write_admission_g9_enablement_evidence_bundle_record,
)
from .hunyuan_neural_enablement_artifact_parity import (
    verify_admission_g9_enablement_evidence_bundle_evidence_artifact_parity,
)
from .hunyuan_g9_enablement_evidence_bundle import (
    G9EnablementEvidenceBundleResult,
    run_g9_enablement_evidence_bundle,
)

_AUDIT_JSON = "hunyuan-admission-audit.json"
_PREFLIGHT_JSON = "hunyuan-enablement-preflight.json"


@dataclass(frozen=True)
class AdmissionG9EnablementEvidenceBundleResult:
    admission_preflight_ok: bool
    admission_g9_enablement_evidence_ok: bool
    g9_enablement_evidence_ready: bool
    g9_enablement_preflight_ok: bool
    parity_ok: bool
    record_dir: Path
    bundle_record_path: Path
    g9_enablement_evidence: G9EnablementEvidenceBundleResult
    issues: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "admission_preflight_ok": self.admission_preflight_ok,
            "admission_g9_enablement_evidence_ok": self.admission_g9_enablement_evidence_ok,
            "g9_enablement_evidence_ready": self.g9_enablement_evidence_ready,
            "g9_enablement_preflight_ok": self.g9_enablement_preflight_ok,
            "parity_ok": self.parity_ok,
            "record_dir": str(self.record_dir),
            "bundle_record_path": str(self.bundle_record_path),
            "g9_enablement_evidence": self.g9_enablement_evidence.to_dict(),
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


def run_admission_g9_enablement_evidence_bundle(
    *,
    record_dir: Path | None = None,
    skip_weight_warm: bool = False,
    live_probe: bool = False,
    space_url: str | None = None,
    sample_path: Path | None = None,
    hosted_neural: bool = False,
    hosted_neural_status_file: Path | None = None,
    hosted_neural_status_text: str | None = None,
    hosted_neural_sample: str | None = None,
    hosted_neural_space_url: str | None = None,
    require_hosted_neural: bool = False,
) -> AdmissionG9EnablementEvidenceBundleResult:
    """Run admission preflight bundle plus G9 enablement evidence capstone."""
    directory = (record_dir or Path(".")).resolve()
    directory.mkdir(parents=True, exist_ok=True)

    admission_ok = _run_preflight_bundle(directory)
    g9_result = run_g9_enablement_evidence_bundle(
        record_dir=directory,
        skip_weight_warm=skip_weight_warm,
        live_probe=live_probe,
        space_url=space_url,
        sample_path=sample_path,
        hosted_neural=hosted_neural,
        hosted_neural_status_file=hosted_neural_status_file,
        hosted_neural_status_text=hosted_neural_status_text,
        hosted_neural_sample=hosted_neural_sample,
        hosted_neural_space_url=hosted_neural_space_url,
        require_hosted_neural=require_hosted_neural,
    )

    issues: list[str] = []
    if not admission_ok:
        issues.append("hunyuan_preflight_bundle failed")
    issues.extend(g9_result.issues)

    bundle_ok = admission_ok and g9_result.g9_enablement_preflight_ok
    bundle_record_path = directory / DEFAULT_ADMISSION_G9_ENABLEMENT_EVIDENCE_BUNDLE_RECORD

    evidence_payload = json.loads(
        g9_result.record_path.read_text(encoding="utf-8")
    )
    base_result = AdmissionG9EnablementEvidenceBundleResult(
        admission_preflight_ok=admission_ok,
        admission_g9_enablement_evidence_ok=bundle_ok,
        g9_enablement_evidence_ready=g9_result.g9_enablement_evidence_ready,
        g9_enablement_preflight_ok=g9_result.g9_enablement_preflight_ok,
        parity_ok=g9_result.parity_ok,
        record_dir=directory,
        bundle_record_path=bundle_record_path,
        g9_enablement_evidence=g9_result,
        issues=tuple(issues),
    )
    write_admission_g9_enablement_evidence_bundle_record(
        bundle_record_path,
        attestation_from_bundle(
            admission_preflight_ok=base_result.admission_preflight_ok,
            admission_g9_enablement_evidence_ok=base_result.admission_g9_enablement_evidence_ok,
            g9_enablement_evidence_ready=base_result.g9_enablement_evidence_ready,
            g9_enablement_preflight_ok=base_result.g9_enablement_preflight_ok,
            parity_ok=base_result.parity_ok,
            issues=base_result.issues,
            evidence_payload=evidence_payload,
        ),
    )

    verify_issues = verify_admission_g9_enablement_evidence_bundle_record_file(
        bundle_record_path
    )
    if verify_issues:
        issues = list(base_result.issues) + verify_issues

    bundle_parity_issues = (
        verify_admission_g9_enablement_evidence_bundle_evidence_artifact_parity(
            bundle_payload=json.loads(bundle_record_path.read_text(encoding="utf-8")),
            evidence_payload=evidence_payload,
        )
    )
    if bundle_parity_issues:
        issues = list(issues) + bundle_parity_issues

    bundle_ok_final = bundle_ok and not verify_issues and not bundle_parity_issues
    parity_ok_final = (
        g9_result.parity_ok and not verify_issues and not bundle_parity_issues
    )
    final_result = AdmissionG9EnablementEvidenceBundleResult(
        admission_preflight_ok=admission_ok,
        admission_g9_enablement_evidence_ok=bundle_ok_final,
        g9_enablement_evidence_ready=g9_result.g9_enablement_evidence_ready,
        g9_enablement_preflight_ok=g9_result.g9_enablement_preflight_ok,
        parity_ok=parity_ok_final,
        record_dir=directory,
        bundle_record_path=bundle_record_path,
        g9_enablement_evidence=g9_result,
        issues=tuple(issues),
    )
    write_admission_g9_enablement_evidence_bundle_record(
        bundle_record_path,
        attestation_from_bundle(
            admission_preflight_ok=final_result.admission_preflight_ok,
            admission_g9_enablement_evidence_ok=final_result.admission_g9_enablement_evidence_ok,
            g9_enablement_evidence_ready=final_result.g9_enablement_evidence_ready,
            g9_enablement_preflight_ok=final_result.g9_enablement_preflight_ok,
            parity_ok=final_result.parity_ok,
            issues=final_result.issues,
            evidence_payload=evidence_payload,
        ),
    )
    return final_result


def format_admission_g9_enablement_evidence_bundle_report(
    result: AdmissionG9EnablementEvidenceBundleResult,
) -> str:
    lines = [
        "hunyuan_admission_g9_enablement_evidence_bundle_ok=True",
        f"admission_preflight_ok={result.admission_preflight_ok}",
        f"admission_g9_enablement_evidence_ok={result.admission_g9_enablement_evidence_ok}",
        f"g9_enablement_evidence_ready={result.g9_enablement_evidence_ready}",
        f"g9_enablement_preflight_ok={result.g9_enablement_preflight_ok}",
        f"parity_ok={result.parity_ok}",
        f"record_dir={result.record_dir}",
        f"bundle_record_path={result.bundle_record_path}",
        f"audit_record={result.record_dir / _AUDIT_JSON}",
        f"enablement_preflight_record={result.record_dir / _PREFLIGHT_JSON}",
        f"g9_enablement_evidence_record={result.g9_enablement_evidence.record_path}",
    ]
    for issue in result.issues:
        lines.append(f"issue={issue}")
    return "\n".join(lines) + "\n"


def admission_g9_enablement_evidence_bundle_json(
    result: AdmissionG9EnablementEvidenceBundleResult,
) -> str:
    return json.dumps(result.to_dict(), indent=2, sort_keys=True) + "\n"
